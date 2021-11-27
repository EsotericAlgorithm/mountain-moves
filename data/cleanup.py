import sys
import shutil
import os
import json




def read_in_dems(description_file, directory):
    # Get eligible files 
    files = []
    with open(description_file) as json_file:
        meta = json.load(json_file)
        files = [x['filename']+'.e00' for x in meta]
    potentials = [x for x in os.listdir("raw") if 'e00' in x]
    assert len(files) == len(potentials)
    # Filter out the first DEM which is the base
    # dangerous assumption
    return list(filter(lambda x: not x.startswith("1_"), potentials))

def create_dem(input_dem_file, base_dem_file, output_dem_file, output_directory="map"):
    try:
        os.mkdir('map')
    except FileExistsError:
        pass
    output = os.path.join(output_directory, output_dem_file)

    print(f"gdal_merge.py {base_dem_file} {input_dem_file} -o {output}\n")
    os.system(f"gdal_merge.py {base_dem_file} {input_dem_file} -o {output}")

    print(f"gdaldem hillshade map/out.tif {input_dem_file.split('_')[0] + '.png'}\n")
    os.system(f"gdaldem hillshade map/out.tif {input_dem_file.split('_')[0] + '.png'}")

    print("deleting map/out.tif\n")
    shutil.copy('map/out.tif', f"map/{input_dem_file.split('_')[0]}.tif")
    os.remove('map/out.tif')

    
candidates = read_in_dems('dem.json', 'raw')
for candidate in candidates:
    create_dem('raw/'+candidate, 'raw/1_msh00_83.e00', "out.tif")
