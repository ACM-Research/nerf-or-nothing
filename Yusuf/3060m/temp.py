import subprocess
# define the path to the run.py script
run_script = r"C:\Users\thewa\Desktop\projects\computational_neuroscience\AI_ML\neRF\scripts\run.py"

# define the path to the data directory
data_dir = r"C:\Users\thewa\Desktop\projects\computational_neuroscience\AI_ML\neRF\ngp_data\data\nerf"

n_runs = 1000

cmd = r"python C:/Users/thewa\Desktop/projects/computational_neuroscience/AI_ML/neRF/instant-ngp/scripts/run.py --scene C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/ngp_data/data/nerf/fox --n_steps 30000"

proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

