# Data 

The data in this file is sourced from the USGS Messerich et al. data set. The raw DEM as ArcInfo grid files have been extracted from their directory structure and the accompanying geographic information provided with the data placed into `dem.json` the filename and date of collection being of particular importance. The full output of hte tool using the input dems is included as `dem_gdal_ful.json` from `find -name *e00 -exec gdalinfo {} -json \; > dem_gdal_full.json` with some slight cleanup into an array.

The projections in the accompanying ArcInfo files contain project and extent information that matches what is included in these files. This information can be easily viewed interactivly by using the binaries included with the GDAL library distribution, e.g. `gdalinfo raw/msh00_83.e00`.

As an initial exploratory visualization task we can create hillshades of all of the dems and stich them together into an mp4 to understand our expectations.

Using the large scale, full extent DEM, merge all the changing sets together

Create the individual images
`find -name "*e00" -exec  gdaldem hillshade {} {}.map.png \;`
Stitch them together into a mp4
`ffmpeg -framerate 1 -i %d.png output.mp4`
