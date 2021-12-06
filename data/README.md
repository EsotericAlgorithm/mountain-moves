# Data Transformation


## Contents
The data in this file is sourced from the USGS Messerich et al. data set. This data is contained in the `raw` directory in the original ArcInfo format.

The `map` directory contains several intermediate steps including:
- `geotiffs`, transformed from ArcInfo files via GDAL
- `hillshades`, an intermediate step to verify visually the content of each DEM. This is after the merge step.
- `meshes`, the output of `tin-terrain` applied to each of the merged GeoTIFFs DEMs.


## Transformation Steps

The raw DEM as ArcInfo grid files have been extracted from their directory structure and the accompanying geographic information provided with the data placed into `dem.json` the filename and date of collection being of particular importance. The full output of the tool using the input dems is included as `dem_gdal_full.json` from `find -name *e00 -exec gdalinfo {} -json \; > dem_gdal_full.json`. The output was transformed by hand to meet the needs of `python-render` and is replicated in the animation directory (`../python-render`).

The projections in the accompanying ArcInfo files contain project and extent information that matches what is included in these files. This information can be easily viewed interactivly by using the binaries included with the GDAL library distribution, e.g. `gdalinfo raw/msh00_83.e00`.


### Hillshades 
As part of the exploratory work initial hillshades are created stitched together 
Using the large scale, full extent DEM, merge all the changing sets together

Create the individual images
`find -name "*e00" -exec  gdaldem hillshade {} {}.map.png \;`
Stitch them together into a mp4
`ffmpeg -framerate 1 -i %d.png output.mp4`


#### Cleanup

The file `cleanup.py` makes some assumptions about directory structure and shells out to GDAL. It performs the following steps in summary:
1. Fetch all eligible files based on a naming convention
2. Merge all DEMs with the base DEM (the earliest, largest one) using `gdal_merge`
3. Create hillshades (not needed but helpful for debugging)
4. Output each DEM as a geotiff for later processing.


### Final Transformation to OBJs
Create dense OBJs from the GeoTIFFs with `tin-terrain` and the instructions outline on https://github.com/heremaps/tin-terrain.

1. Translate all the GeoTIFFs from the previous step using gdalwarp into NAD83. Outlined in `Projections` section on the `tin-terrain` documentation.
2. Process each GeoTIFF with [tin-terrain](https://github.com/heremaps/tin-terrain) using the dense method (`--method dense`).
