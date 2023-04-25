import glob
import os
import pandas as pd

# Set the path of the CSV files
csv_path = 'compiled/'

# Use a wildcard to get all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_path, '*.csv'))

# get the dataset name from the file name: split(_)[2]
# use the dataset name as a row of its own in the dataframe to identify the dataset when concatenating
# concatenate
# write to csv file
# create a list of dataframes
df_list = []
for f in csv_files:
    df = pd.read_csv(f)
    df['dataset'] = f.split('_')[2].split('.')[0]
    df_list.append(df)
# concatenate the list of dataframes
df = pd.concat(df_list, ignore_index=True)
# write to csv file
df.to_csv('compiled.csv')