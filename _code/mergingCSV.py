import os
import pandas as pd


## to merge multiple csv  files with same structure
directory = "../datasets/arzEn/"

csv_files = [file for file in os.listdir(directory) if file.endswith(".csv")]

df_list = [pd.read_csv(os.path.join(directory, file)) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)


merged_df.to_csv("../datasets/arzEn.csv", index=False)

print(merged_df.head())