##########################################
# Description:
# This script downloads all available waves of the Census Household Pulse Survey,
# binds them together into a “long” format, and produces a plot of the % feeling anxious most days.
# Adapted from the R code by Sophie Hill (9/12/21; updated 5/30/22).
##########################################

import os
import re
import glob
import shutil
import requests
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import pyarrow
import fastparquet

##########################################
# Set file path
##########################################
my_file_path = "../data/puf_data"


##########################################
# Move files from download folder to new folder
##########################################
downloads_folder = r"C:\Users\brevi\Downloads"
destination_folder = r"C:\Users\brevi\PycharmProjects\CS150\covid-19-mental-health-project\puf_data"

target_folders_to_10 = [f"HPS_Week0{i}_PUF_CSV.zip" for i in range(1,10)]

#print(target_folders_to_10)

target_folders_rest = [f"HPS_Week{i}_PUF_CSV.zip" for i in range(10,64)]

#print(target_folders_rest)

target_folders = target_folders_to_10 + target_folders_rest
#print(target_folders)

# First initializing copy over list with 202 files
filenames_to_copy_over = [f"pulse2020_puf_0{i}.csv" for i in range(1,10)]
#print(filenames_to_copy_over)
filenames_to_copy_over += [f"pulse2020_puf_{i}.csv" for i in range(10,21)]
#print(filenames_to_copy_over)

# Now adding 2021 files
filenames_to_copy_over += [f"pulse2021_puf_{i}.csv" for i in range(21, 41)]
#print(filenames_to_copy_over)

# Now 2022 files
filenames_to_copy_over += [f"pulse2022_puf_{i}.csv" for i in range(41, 51)]
#print(filenames_to_copy_over)

# Now 2023 files
filenames_to_copy_over += [f"pulse2023_puf_{i}.csv" for i in range(51, 64)]
#print(filenames_to_copy_over)

# Making lists into a dictionary
folder_and_file_dict = dict(zip(target_folders, filenames_to_copy_over))
print(folder_and_file_dict)

##### HELPER FUNCTION
# Now copying files over

# for zip_name, filename in folder_and_file_dict.items():
#     zip_path = os.path.join(downloads_folder, zip_name)
#     print(f"Zip path: {zip_path}, Filename: {filename}")
#
#     if os.path.exists(zip_path):
#         print("PATH EXISTS")
#         with zipfile.ZipFile(zip_path, "r") as zip_ref:
#             if filename in zip_ref.namelist():
#                 zip_ref.extract(filename, path=destination_folder)
#                 print(f"Extracted {filename} from {zip_name}to {destination_folder}")
#
#     else:
#         print(f"Zip file {zip_name} does not exist")


##########################################
# Select the raw CSV files (ignore weight files/data dictionaries)
##########################################
# List all CSV files in the directory
file_list = [os.path.basename(f) for f in glob.glob(os.path.join(my_file_path, "*.csv"))]
# Exclude files with "repwgt" in the filename
file_list = [f for f in file_list if "repwgt" not in f]

##########################################
# Bind all CSV files together into one DataFrame
##########################################
dfs = []
for f in file_list:
    file_path = os.path.join(my_file_path, f)
    print(f"Reading {f}...")
    df = pd.read_csv(file_path)
    dfs.append(df)




hps = pd.concat(dfs, ignore_index=True).dropna(axis=1, how='any')


# Save combined data to a parquet file (an efficient storage format)
hps.to_parquet("hps_.parquet")
print("Combined data saved to hps_combined.parquet")

##########################################
# Quick look at the data
##########################################
print(hps.head())
print("WEEK counts:")
print(hps['WEEK'].value_counts())
print("Column names:")
print(hps.columns.tolist())
print("ANXIOUS counts:")
print(hps['ANXIOUS'].value_counts())

##########################################
# Process data and create a plot
##########################################
# Select relevant columns and create a new variable based on ANXIOUS
df = hps[['WEEK', 'ANXIOUS']].copy()


def compute_anxious(x):
    if x < 0:
        return None  # equivalent to NA in R
    elif x in [1, 2]:
        return 0
    elif x in [3, 4]:
        return 1
    else:
        return None


df['anxious_mostdays'] = df['ANXIOUS'].apply(compute_anxious)

# Group by WEEK and calculate the mean (ignoring missing values)
grouped = df.groupby('WEEK', as_index=False)['anxious_mostdays'].mean()
# Multiply by 100 to convert to percentage
grouped['mean_anxious_mostdays'] = grouped['anxious_mostdays'] * 100

##########################################
# Plot the results using matplotlib
##########################################
plt.figure(figsize=(8, 6))
plt.plot(grouped['WEEK'], grouped['mean_anxious_mostdays'], marker='o')
plt.xlabel("Week")
plt.ylabel("")
plt.ylim(0, 40)
plt.title("% feeling anxious most days")
plt.suptitle("Unweighted (due to laziness)", y=0.94)
plt.figtext(0.5, 0.01, "Source: Census Household Pulse survey", wrap=True, ha="center", fontsize=10)
plt.tight_layout()
plt.show()
