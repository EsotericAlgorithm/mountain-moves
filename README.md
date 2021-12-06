# Rendering a Series of Digital Elevation Models of Mt.St.Helens

## Introduction
This repository implements a technique to animate digital elevation models transformed into meshes and linear interpolated in elevation across the time domain. The process is static and uses a mesh without any simplification. As a test bed, the DEMs, as ArcInfo files, created by USGS Messerich et al. 2008 [[1]](#[1]) as part of the 2004-2007 dome building of Mt.St.Helens. This is not an especially novel method, and is referred to as shape keying or morph target animation. There is an implementation in most computer graphics toolsets, such as [Blender](https://docs.blender.org/manual/en/latest/animation/shape_keys/index.html) and [Maya](https://knowledge.autodesk.com/support/maya-lt/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/MayaLT/files/Blend-Shape-deformer-Setting-keys-for-blend-shapes-htm.html).

The files were converted to GeoTIFFs and an appropriate projection using GDAL [[8]](#[8]), they were then convereted to dense objs using tin-terrain [[9]](#[9]). Finally, the objs were loaded as keyframes and interpolated between the meshes for rendering in PyVista [[10]](#[10]). The transformations steps are outlined in the [`data`](data/) directory and the interpolation steps in [`python-render`](python-render/).

As a sanity check at the start of the process hillshades were generated from the GeoTIFFs:

![Hillshape example](/data/map/hillshades/21.png)

[The final result is available on YouTube](https://www.youtube.com/watch?v=Mc_HcEEyKuk):

[![Final result of DEM animation](https://img.youtube.com/vi/Mc_HcEEyKuk/0.jpg)](https://www.youtube.com/watch?v=Mc_HcEEyKuk)

## Other Visualization Work
There have been a handful of great visualizations of the Mt.St.Helens dome building event constructed from a combination of periodic digital elevation models and photogrammetry from optical monitoring techniques.

- [USGS Dome Growth Timelapse (likely the Brutus location mentioned in Salazar et al. 2016)](https://www.usgs.gov/media/videos/time-lapse-images-mount-st-helens-dome-growth-2004-2008) [[13]](#[13])

- [USGS Dome Growth rendered from collected DEMs](https://www.usgs.gov/media/videos/time-series-dome-glacier-growth-mount-st-helens-wa) [[12]](#[12])

- [NASA JPL Visualization from 2004-09-24 to 2004-10-14 with temperature](https://photojournal.jpl.nasa.gov/archive/visualizations/PIA15004_MSH_DomeMorph_576.mov) [[11]](#[11])


## Background

Digital elevation models prior to 2000 were generally expensive. There has been an explosion of work that due to the decrease is costs of point cloud and aerial data collection along with the wide-spread availability and accessibility of photogrammetry techniques. In particular this has allowed for more fine-grained examination of short temporal events for both research and public safety purposes. While this work uses the data collected by the USGS (Messerich et al. 2008) [[1]](#[1]) the methods available in the past five years have significantly reduced costs leading to broader deployment usage. Some examples of interest include extensions of this data set to understand the seismic-drive morphology changes (Salzer et al. 2016) [[7]](#[7]). The measurement to a previously unavailable level of detail in the Holuhraun Eruption in Iceland (Müller et al. 2017) [[2]](#[2]). The monitoring and dissemination of public safety information for volcanic hazards (Diefenbach 2018) [[6]](#[6]). The modeling and visualizing erosion monitoring for lahar remobilization after hurricanes (Walter et al. 2018) [[3]](#[3]). Areas of degassing around fumaroles near the La Fossa cone (Müller et al. 2021) [[5]](#[5]).

The majority this work is focused on quantitivative measures of models or data collection methodology. All of this work could be complimented with research in ceffective visualizations of the physical growth and the underlying physical processes driving change. While not explored in this visualization, the different models that explain dome growth in near surface contexts (top kilometer near surface) would be an area of possible future study. 

## Conclusions and Future Work

In the case of this work the Salzer results contradict the method of motion visualized in the resultant video where the changes are gradual shifts in structure, but instead are shown to be large movements (in excess of 40 cm in an event) correlated with the seismic events. 

The gradual nature of the change between DEMs, especially over longer time periods, is misleading. Simplistic changes such as interpolating with a cspline led to nearly identical results visually and artifacting I was not able to resolve. Combining optical techniques to identify features and creating vector fields from the movement of those features would likely lead to better bulk component movement registration. Several methods for future exploration on applied data sets are possible through structure from motion and multiview stereo techniques especially the overlap of laser-derived DEMs and optical datasets (Carrivick et al. 2016) [[4]](#[4]).

Attempts to use color to explain movement as the interpolated displacement gradient effectively showed movement, but created an impression of significant change in particular regions so was excluded. The gradient used a naive calculation over all verticies as well resulting in a length rendering period. Similarly, finding a way to isolate particular features and color them to display the aggregate nature of flow may allow some ability to display the elasticity of the medium which I do not believe to be accurately represented in the visualization.

Perhaps most obviously, the visualization could be interactive. I fought with scaling issues when loading the meshes into a WebGL context that I could not readily resolve. While the dimensionality is high, even without mesh simplification interactive use would be possible. The selection of a dense object interpretation of the DEM made interpolation straight-forward but would be complicated by mesh simplification with a 1:1 map between points is not maintained. There is a signifcant body of research on mapping mesh to mesh and it is a similar problem to optical flow techniques used in matching graphs. This could be trivial solved with larger photogrammetry models by mapping a mesh to a structured grid that minimizes error, but would likely have instances of pathological errors unless the sampling rate was an order of magnitude than the change of interest (purley speculation).

This implementation is incredibly memory intensive and did not make an attempt to store the mesh intermediates (`Frame` in the code). A more dense interpretation could be achieved through storing the only the differences. The existing implementation is naive and operates on all changed vertices resulting in a generation time of around a half a second per frame.

Ultimately, effective communication of scientific results is hard technically due the volume of data and the aesthetic search space being near infinite. Geoscience and new paradigms of data gathering present more data for different kinds of visualization.


## References
<a id="[1]">[1]</a> J. A. Messerich, S. P. Schilling, and R. A. Thompson, “Digital Elevation Models of the Pre-Eruption 2000 Crater and 2004–07 Dome-Building Eruption at Mount St. Helens, Washington, USA,” 2008. https://pubs.usgs.gov/of/2008/1169/ (accessed Nov. 21, 2021).

<a id="[2]">[2]</a> D. Müller et al., “High-Resolution Digital Elevation Modeling from TLS and UAV Campaign Reveals Structural Complexity at the 2014/2015 Holuhraun Eruption Site, Iceland,” Frontiers in Earth Science, vol. 5, p. 59, 2017, doi: 10.3389/feart.2017.00059.

<a id="[3]">[3]</a> T. R. Walter, J. Salzer, N. Varley, C. Navarro, R. Arámbula-Mendoza, and D. Vargas-Bracamontes, “Localized and distributed erosion triggered by the 2015 Hurricane Patricia investigated by repeated drone surveys and time lapse cameras at Volcán de Colima, Mexico,” Geomorphology, vol. 319, pp. 186–198, Oct. 2018, doi: 10.1016/j.geomorph.2018.07.020.

<a id="[4]">[4]</a> J. L. Carrivick, Structure from Motion in the Geosciences, 1st ed. Wiley Blackwell, 2016.

<a id="[5]">[5]</a> D. Müller, S. Bredemeyer, E. Zorn, E. De Paolo, and T. R. Walter, “Surveying fumarole sites and hydrothermal alteration by unoccupied aircraft systems (UAS) at the La Fossa cone, Vulcano Island (Italy),” Journal of Volcanology and Geothermal Research, vol. 413, p. 107208, May 2021, doi: 10.1016/j.jvolgeores.2021.107208.

<a id="[6]">[6]</a> A. Diefenbach, “Use of UASs (‘Drones’) in 2018 at Kīlauea and Beyond.” https://www.usgs.gov/media/videos/use-uass-drones-2018-k-lauea-and-beyond (accessed Nov. 21, 2021).

<a id="[7]">[7]</a> J. T. Salzer, W. A. Thelen, M. R. James, T. R. Walter, S. Moran, and R. Denlinger, “Volcano dome dynamics at Mount St. Helens: Deformation and intermittent subsidence monitored by seismicity and camera imagery pixel offsets,” Journal of Geophysical Research: Solid Earth, vol. 121, no. 11, pp. 7882–7902, 2016, doi: 10.1002/2016JB013045.

<a id="[8]">[8]</a> GDAL/OGR contributors, GDAL/OGR Geospatial Data Abstraction software Library. Open Source Geospatial Foundation, 2021. [Online]. Available: https://gdal.org

<a id="[9]">[9]</a> A. Partl and M. Seeger, tin-terrain. HERE Technologies. [Online]. Available: https://github.com/heremaps/tin-terrain

<a id="[10]">[10]</a> C. B. Sullivan and A. Kaszynski, “PyVista: 3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK),” Journal of Open Source Software, vol. 4, no. 37, p. 1450, May 2019, doi: 10.21105/joss.01450.

<a id="[11]">[11]</a> V. Realmuto, Growth of the Mount St. Helens Lava Dome, September 24-October 14, 2004. Accessed: Nov. 23, 2021. [Online Video]. Available: https://photojournal.jpl.nasa.gov/archive/visualizations/PIA15004_MSH_DomeMorph_576.mov

<a id="[12]">[12]</a> Time-series of dome & glacier growth at Mount St. Helens, WA, (32 2011). Accessed: Nov. 05, 2021. [Online Video]. Available: https://www.usgs.gov/media/videos/time-series-dome-glacier-growth-mount-st-helens-wa

<a id="[13]">[13]</a> Time-lapse images of Mount St. Helens dome growth 2004-2008, (Dec. 31, 2007). Accessed: Nov. 12, 2021. [Online Video]. Available: https://www.usgs.gov/media/videos/time-lapse-images-mount-st-helens-dome-growth-2004-2008
