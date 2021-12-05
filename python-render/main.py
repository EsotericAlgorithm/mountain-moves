import pyvista as pv
import tempfile
import json
import os
import datetime
import argparse
from itertools import tee

class Frame:
    '''
    The mesh and associated information as rendered
    '''
    def __init__(self, start_obj, end_obj, date: datetime):
        '''
        Given a two Objs and a date returns the render
        intermediate mesh for that day
        '''
        self.date = date
        day_difference = (end_obj.date - start_obj.date).days
        if day_difference <=0:
            raise ValueError("end_obj is before start_obj")
        if date < start_obj.date:
            raise ValueError("Target frame date is before start_obj")
        if date > end_obj.date:
            raise ValueError("Target frame date is after end_obj")

        end_mesh = end_obj.mesh()
        start_mesh = start_obj.mesh()
        days_in_frame = (date - start_obj.date).days
        
        mesh_difference = end_mesh.points - start_mesh.points
        self.difference = mesh_difference/day_difference*days_in_frame
        
        self.mesh = start_mesh
        self.mesh.points = self.mesh.points + self.difference

    def _debug_plot(self, plot_obj):
        plot_obj.add_mesh(self.mesh)
        plot_obj.add_text(f"{self.date}", name="time-label")
       
        
class Movie:
    def __init__(self, meshset, size_x=1280,
                 size_y=720,
                 output_file="render.mp4",
                 frames_per_day=3,
                 cpos=(1, 1, 1)):
        self.size_x = size_x
        self.size_y = size_y
        self.output_file = output_file
        self._dataset = meshset
        self._ordered_obj_pairs = pairwise(self._dataset)
        self._plot = pv.Plotter(window_size=[size_x, size_y], line_smoothing=True)
        self._cpos = cpos
        self._frames_per_day = frames_per_day

    def render(self):
        self._plot.open_movie(self.output_file)
        # The first pair is the starting point and should be outside the render loop
        first, second = next(self._ordered_obj_pairs)
        frame = Frame(first, second, second.date)
        self._plot.add_mesh(frame.mesh)
        self._plot.set_position(self._cpos)
        self._plot.camera.focal_point = (-1.36022e+07, 5.81277e+06, 1553.45)
        self._plot.camera.roll = -90



        
        # For each mesh keyframe...
        for (start_obj, end_obj) in self._ordered_obj_pairs:
            for day in daterange(start_obj.date, end_obj.date):
                frame = Frame(start_obj, end_obj, day)
                self._plot.add_mesh(frame.mesh, 
                                    show_scalar_bar=False,
                                    cmap='terrain')
                self._plot.add_text(f"{day.strftime('%-d %B %Y')}",
                                    name="time-label",
                                    shadow=True,
                                    viewport=True,
                                    position=(0.7, 0.1))
                for _ in range(self._frames_per_day):
                    self._plot.write_frame()
        self._plot.close()

class Obj:
    """Obj and associated metadata"""
    def __init__(self, model_file, meta_data):
        self.filename = model_file
        self.date = datetime.datetime.strptime(meta_data['date'], "%Y_%m_%d")
        self.bounding_coordinates = meta_data['Bounding_Coordinates']
        self.min_alt = meta_data['min_alt']
        self.max_alt = meta_data['max_alt']

    def __repr__(self):
        return f"<Obj: file: {self.filename}>"

    def mesh(self):
        return pv.read(self.filename)

class MeshDataset:
    '''
    The ObjDataset contains meshes loaded from objs initialized from a directory
    with specified keyframes. The meshes are wrapped in an iterator 
    '''
    
    def __init__(self, obj_directory, obj_metadata="dem.json"):
        '''
        Loads all models .obj files from obj_directory. Expects a file `dem.json`
        which contains metadata on the obj files.
        '''
        self._model_dir = obj_directory
        self._metadata_file = os.path.join(obj_directory, obj_metadata)
        self.obj_files = []
        for maybe_obj_file in os.listdir(self._model_dir):
            if maybe_obj_file.lower().endswith('.obj'):
                self.obj_files.append(maybe_obj_file)
        self.obj_files = sorted(self.obj_files, key=lambda x: int(x.split('.')[0]))
        self.meta = None
        with open(self._metadata_file, 'r') as meta_file:
            self.meta = json.load(meta_file)

        if self.meta == None:
            raise ValueError("No metadata file found")
        if (lo := len(self.obj_files)) < (lm := len(self.meta)):
            raise ValueError(f"Not enough metadata, {lo} objs with {lm} meta entries")

        self.objs = []
        for obj in self.obj_files:
            new_obj = Obj(os.path.join(self._model_dir,  obj), self.meta[obj])
            self.objs.append(new_obj)

    def __iter__(self):
        yield from self.objs
        
    def __len__(self):
        return len(self.obj_files)

    def __repr__(self):
        return f"<MeshDataset: {len(self)} objs>"        
            

# Utils                         
def pairwise(iterable):
    '''
    Utility pulled from python3 doc to be backwards compatible with < python 3.10
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def daterange(start_date, end_date):
    '''
    Cleaner daterange iterator than what I wrote, adapted from
    https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
        '''
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate movie from sequence of objs')
    parser.add_argument('--models', '-m', default="models", help="model directory with objs (default: models")
    parser.add_argument('--output', '-o', default="out.mp4", help="name of output movie file")
    parser.add_argument('-x', default=-13597460, help="x pos of camera for rendering", type=int)
    parser.add_argument('-y', default=5812104, help="y pos of camera for rendering", type=int)
    parser.add_argument('-z', default=4928, help="z pos of camera for rendering", type=int)
    args = parser.parse_args()
    meshes = MeshDataset(args.models)
    movie = Movie(meshes, output_file = args.output, cpos=(args.x, args.y, args.z))
    movie.render()
