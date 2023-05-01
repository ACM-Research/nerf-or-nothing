# Vanilla NeRF and Mip-Nerf

Both of these methods are old, and their flaws are extremely pronounced. The results are inaccurate and distorted, not fit for an immersive environment. To view the output, use the ns-viewer command in nerfstudio with the respective config.yml files. To view more descriptive results of the two runs, read the respective MethodDescription.pdf.

## How to train a model:

- colmap processing 

``ns-process-data [images/video/polycam] --data {data path to source folder/video} --output-dir {PROCESSED_DATA_DIR}``


- train:

``ns-train [mipnerf/vanilla-nerf] --data [PROCESSED_DATA_DIR]``

-view 

''ns-viewer --load-config {outputs/.../config.yml}''
