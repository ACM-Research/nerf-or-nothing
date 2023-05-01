@echo off
for /D %%d in (*) do (
    pushd "%%d"
    python "C:\Users\thewa\Desktop\projects\computational_neuroscience\AI_ML\neRF\Instant-NGP-for-RTX-3000-and-4000/scripts/colmap2nerf.py" --colmap_matcher exhaustive --run_colmap --aabb_scale 32
    popd
)