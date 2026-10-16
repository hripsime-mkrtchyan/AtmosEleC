#creating seperate files
import csv
import pandas as pd
import numpy as np
import os

flname = 0
#dir_lists = ['0h2h','3h5h','6h8h','9h11h','12h14h','15h17h','18h20h','21h23h']
filenumber = ['1','2','3','4','5','6','7']
ijk =6

input_final = '../Lerwick_7days_data/middle_files_7days'+'/day_'+filenumber[ijk]+'_results.csv'

output_file_dir='../Lerwick_7days_data/middle_files_7days/dir'+filenumber[ijk]
os.makedirs(output_file_dir, exist_ok=True)
print(output_file_dir)

df = pd.read_csv(input_final)
print(df['filename'])
# Group the data by the 'ID' column
grouped = df.groupby('filename')

# Save each group to a separate file
for name, group in grouped:
    file_name = f"{name}.csv"
    dir_file = output_file_dir +'/'+ file_name
    group.to_csv(dir_file, index=False)
    print(f"Saved file: {file_name}")