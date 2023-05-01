# NerFacto: 
https://docs.nerf.studio/en/latest/nerfology/methods/nerfacto.html	


## What is Nerfacto?
Nerfacto is created by Nerfstudio as a combination of other NeRFmethods, with features such as camera pose refinement, per image appearance conditioning, proposal sampling,  scene contraction, and hash encoding. Pose refinement backpropagates loss gradients to the input pose calculations, to correct errors in predicted camera poses with scenes from devices such as phones. Rather than using a uniform sampler, NeRFacto uses a piecewise sampler, sample distributed based on distance  from the camera, increasing more with each sample. The proposal sampler uses 2 density functions to consolidate sample locations to regions of scenes that help most with the final render (i.e at intersections of rays), outputting a coarse density field.



## How to train a model: [^1]

- colmap processing 

``ns-process-data [images/video/polycam] --data {data path to source folder/video} --output-dir {PROCESSED_DATA_DIR}``



- train (with NeRFacto):

``ns-train nerfacto --data [PROCESSED_DATA_DIR]``

### Note on training:

Between the different types of datasets, the scenes taken by standard 4k camera, vs. 360 camera, there was failure to convert the video footage of 360 video into COLMAP feature matching. 360 screen footage is processed through the equirectangular mode from nerftstudio's process-data. Phone footage is pre-processed through KIRI Engine, which means it's already pretrained.

Note: *if folder of output model trained is needed to move, edit ''config.yml'' to match new folder datapath, otherwise model will be unable to be reopened via ``ns-viewer``*


## Overall Immersion Rating

NeRFacto's strength is its general proficiency for any scenario, and it is a quick method compared to standard vanilla NeRF. Within that, NeRFacto is recommended with standard perspective projection cameras, as with 360 footage, the length of processing data is significantly long (with ns-process-data equirectangular). So the optimal type of dataset to work with NeRFacto is a standard perspective camera.  

[^1]: follow [Nerfstudio's installation tutorial](https://docs.nerf.studio/en/latest/quickstart/installation.html) and (if needed) [COLMAP installation](https://colmap.github.io/install.html#linux)
