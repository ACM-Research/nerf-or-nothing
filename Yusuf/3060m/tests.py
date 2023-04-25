import subprocess
import time
import GPUtil
import csv
import os

# define the datasets to use for the trials

# define the number of trials to run for each dataset
num_trials = 5
n_runs = 3500

# define the path to the run.py script
run_script = "C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/scripts/run.py"

# define the path to the data directory
data_dir = "C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/ngp_data/data/nerf/utd-data/proc-output/"

datasets = []
#fill datasets array from immediate subdirs of data dir
dataset = os.listdir(data_dir)
for d in dataset:
    if os.path.isdir(os.path.join(data_dir, d)):
        datasets.append(d)
print(datasets)
#exit()
# define the path to the output directory
output_dir = "output"

# create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# create the gpu_utilization.csv file


# loop over each dataset and run multiple trials
for dataset in datasets:
    
    for i in range(num_trials):
        utilization_file = os.path.join(output_dir, f"gpu_utilization_{dataset}_{i}.csv")
        with open(utilization_file, 'w', newline='') as csvfile:
            csvfile.write("time, gpu_id, gpu_load, gpu_free_mem, gpu_used_mem\n")
        # lossfile = os.path.join(output_dir, f"loss_{dataset}_{i}.csv")
        # with open(lossfile, 'w', newline='') as csvfile:
        #     csvfile.write("time, loss\n")
        # define the command to run
        cmd = f"python C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/instant-ngp/scripts/run.py --scene {data_dir + dataset} --n_steps {n_runs}"


        # define the environment variables

        # define the path to the output file
        #output_file = f"{output_dir}/{dataset}/{dataset}_trial_{i}.txt"

        # start the timer
        start_time = time.time()
        
        # run the command and collect the gpu utilization as its running
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            while True:
                print(proc.stdout.readline().decode('utf-8'))
                # check if the process is still running
                if proc.poll() is not None:
                    break

                # check if the process is using any gpus
                gpus = GPUtil.getGPUs()
                if len(gpus) > 0:
                    # write the gpu utilization to the file
                    with open(utilization_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        for gpu in gpus:
                            writer.writerow([time.time() - start_time, gpu.id, gpu.load, gpu.memoryFree, gpu.memoryUsed])
                    #get the loss from the output of subprocess. it is at the end of this line: Training:  13%|██████▌                                          | 3993/30000 [02:16<14:51, 29.19steps/s, loss=0.000547]
                    # with open(lossfile, 'a', newline='') as csvfile:
                    #     writer = csv.writer(csvfile, delimiter=',')
                    #     out = proc.stdout.readline().decode('utf-8').split("=")[-1].strip()
                    #     writer.writerow([time.time() - start_time, out])

                # sleep for 100ms
                time.sleep(0.1)

        # wait for the process to finish
        proc.wait()
