# script to process data in output dir
import pandas as pd
import os

data_dir = "C:/Users/thewa/Desktop/projects/computational_neuroscience/AI_ML/neRF/ngp_data/data/nerf/utd-data/proc-output/"
out_dir = "output"
# get average of gpu load, gpu free mem, gpu used mem columns for each trial 0-4
# output to text file
datasets = []
# fill datasets array from immediate subdirs of data dir
dataset = os.listdir(data_dir)
for d in dataset:
    if os.path.isdir(os.path.join(data_dir, d)):
        datasets.append(d)


# gpu utilization processing
def proc_gpu():

    # loop over each dataset and run multiple trials
    for dataset in datasets:
        for i in range(5):
            gpu_utilization_file = os.path.join(
                out_dir, f"gpu_utilization_{dataset}_{i}.csv")
            with open(gpu_utilization_file, 'r') as csvfile:
                df = pd.read_csv(csvfile)
                # print(df)
                # print(df[' gpu_load'].mean())
                # print(df[' gpu_free_mem'].mean())
                # print(df[' gpu_used_mem'].mean())

                # write to text file
                gpu_utilization_outfile = os.path.join(
                    out_dir, f"gpu_utilization_{dataset}_{i}.txt")
                with open(gpu_utilization_outfile, 'w') as txtfile:
                    txtfile.write(f"time: {df['time'].iloc[-1]}\n")
                    txtfile.write(f"gpu_load: {df[' gpu_load'].mean()}\n")
                    txtfile.write(
                        f"gpu_free_mem: {df[' gpu_free_mem'].mean()}\n")
                    txtfile.write(
                        f"gpu_used_mem: {df[' gpu_used_mem'].mean()}\n")


def proc_loss():

    # loop over each dataset and run multiple trials
    for dataset in datasets:
        i = 0
        # get all csvs with the words loss and dataset name
        # write to text file final loss for each csv
        for f in os.listdir(out_dir):
            if f.startswith(f"loss_{dataset}") and f.endswith(".csv"):
                loss_file = os.path.join(out_dir, f)
                with open(loss_file, 'r') as csvfile:
                    # print(csvfile)
                    df = pd.read_csv(csvfile)
                    # print(df)
                    # print(df[' time'].iloc[-1])
                    # print(df[' loss'].iloc[-1])

                    # write to text file
                    loss_outfile = os.path.join(
                        out_dir, f"loss_{dataset}_{i}.txt")
                    i += 1
                    with open(loss_outfile, 'w') as txtfile:
                        txtfile.write(f"loss: {df['loss'].iloc[-1]}\n")


# bringing it all together

def proc_all():

    # generate a csv file for each data set with the data collected from the text files
    # each row will be a trial
    # then after the trials, there will be rows for the average,std deviation, min and max, of each column

    # get all text files in output dir
    files = []
    gpu_files = []
    loss_files = []
    for f in os.listdir("output"):
        if f.endswith(".txt"):
            files.append(f)
    # split files into gpu and loss files
    for f in files:
        if f.startswith("gpu") and f.endswith(".txt"):
            gpu_files.append(f)
        elif f.startswith("loss") and f.endswith(".txt"):
            loss_files.append(f)
    # create dictionary with key as dataset and value as list of values for each trial
    #print(files, gpu_files, loss_files)
    compiled_data = {}
    for f in gpu_files:
        # print(f)
        dataset = f.split("_")[2]
        # print(dataset)
        with open(os.path.join(out_dir, f), 'r') as txtfile:
            #print(txtfile)
            lines = txtfile.readlines()

            if dataset not in compiled_data:
                compiled_data[dataset] = [[lines[0].split(":")[1], lines[1].split(
                    ":")[1], lines[2].split(":")[1], lines[3].split(":")[1]]]
            else:
                compiled_data[dataset].append([lines[0].split(":")[1], lines[1].split(":")[
                                              1], lines[2].split(":")[1], lines[3].split(":")[1]])
    # print(compiled_data)

    # add loss data to compiled_data dictionary at corresponding trial index
    for f in loss_files:
        # print(f)
        dataset = f.split("_")[1]
        # print(dataset)
        with open(os.path.join(out_dir, f), 'r') as txtfile:
            #print(txtfile)
            lines = txtfile.readlines()

            if dataset not in compiled_data:
                compiled_data[dataset] = [[lines[0].split(":")[1]]]
            else:
                compiled_data[dataset][int(f.split("_")[2].split(".")[0])].append(
                    lines[0].split(":")[1])
    # print(compiled_data)

    # loop over each dataset and write data to csv file
    for dataset in compiled_data:
        # print(compiled_data[dataset])
        df = pd.DataFrame(compiled_data[dataset], columns=[
                          'time', 'gpu_load', 'gpu_free_mem', 'gpu_used_mem', 'loss'])
        # each row is a trial
        # split columns for each row, convert the values to floats, then get the mean, std, min, and max
        # print(df)
        df['time'] = df['time'].astype(float)
        df['gpu_load'] = df['gpu_load'].astype(float)
        df['gpu_free_mem'] = df['gpu_free_mem'].astype(float)
        df['gpu_used_mem'] = df['gpu_used_mem'].astype(float)
        df['loss'] = df['loss'].astype(float)
        # print(df)
        avg = df.mean()
        std = df.std()
        minimum = df.min()
        maximum = df.max()
        # print(avg, std, minimum, maximum)
        # write entire dataframe to csv file
        # in the last rows write the avg, std, min, and max
        df.to_csv(os.path.join(out_dir, f"compiled_data_{dataset}.csv"))
        with open(os.path.join(out_dir, f"compiled_data_{dataset}.csv"), 'a') as csvfile:
            csvfile.write("avg,std,min,max\n")
            csvfile.write(
                f"{avg['time']},{avg['gpu_load']},{avg['gpu_free_mem']},{avg['gpu_used_mem']},{avg['loss']}\n")
            csvfile.write(
                f"{std['time']},{std['gpu_load']},{std['gpu_free_mem']},{std['gpu_used_mem']},{std['loss']}\n")
            csvfile.write(
                f"{minimum['time']},{minimum['gpu_load']},{minimum['gpu_free_mem']},{minimum['gpu_used_mem']},{minimum['loss']}\n")
            csvfile.write(
                f"{maximum['time']},{maximum['gpu_load']},{maximum['gpu_free_mem']},{maximum['gpu_used_mem']},{maximum['loss']}\n")
        
if __name__ == "__main__":
    proc_gpu()
    proc_loss()
    proc_all()
