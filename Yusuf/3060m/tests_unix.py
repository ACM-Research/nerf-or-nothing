import time
import GPUtil
import csv
import os
import pexpect

# define the datasets to use for the trials
datasets = ["fox"]

# define the number of trials to run for each dataset
num_trials = 5

# define the path to the run.py script
run_script = "C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/scripts/run.py"

# define the path to the data directory
data_dir = "mnt/c/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/ngp_data/data/nerf/"

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
        lossfile = os.path.join(output_dir, f"loss_{dataset}_{i}.csv")
        with open(lossfile, 'w', newline='') as csvfile:
            csvfile.write("time, loss\n")
        # define the command to run
        cmd = f"python /mnt/c/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/instant-ngp/scripts/run.py --scene {data_dir + dataset} --n_steps 3000"


        # define the environment variables

        # define the path to the output file
        #output_file = f"{output_dir}/{dataset}/{dataset}_trial_{i}.txt"

        # start the timer
        start_time = time.time()
        
        # run the command and collect the gpu utilization as its running
        with pexpect.spawn(cmd, timeout=None, encoding='utf-8') as proc:
            while True:
                # check if the process is still running
                if proc.isalive() is False:
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
                    with open(lossfile, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        try:
                            proc.expect(pexpect.EOF)
                            out = proc.before
                            writer.writerow([time.time() - start_time, out])
                        except pexpect.TIMEOUT:
                            pass

                # sleep for 100ms
                time.sleep(0.1)

        # wait for the process to finish
        proc.wait()
