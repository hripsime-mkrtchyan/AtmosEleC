import csv
import os
import re
import pandas as pd
import numpy as np
from functools import partial
from functions_zooni import trim_hours_to_match_dd, split_and_fill
#from functions_zooni import calculate_iqr
from functions_zooni import expand_row
#from functions_zooni import replace_none_t11
from functions_zooni import replace_with_most_frequent, replace_with_most_frequent2, transform_day_type, main_transformation
#from functions_zooni import normalize_dd
#from functions_zooni import split_and_fill
from functions_zooni import adjust_dd_group, adjust_hh_group# standardize_year,
from functions_zooni import aggregate_group, most_frequent_values_for_length

input_dirs =[]
data_list = []
input_dirs1 =[]
all_data_list = []
dfs =[]
collected_data = []

#______________

filenumber = ['1','2','3','4','5','6','7']
ijk =0

hour_list = ['0h','1h','2h','3h','4h','5h','6h','7h','8h','9h','10h','11h','12h',
             '13h','14h','15h','16h','17h','18h','19h','20h','21h', '22h','23h']

# hour_lists = [['0h','1h','2h'],['3h','4h','5h'],['6h','7h','8h'],['9h','10h','11h'],
#              ['12h','13h','14h'],['15h','16h','17h'],['18h','19h','20h'],
#              ['21h', '22h','23h']]

main_temp = '../Lerwick_7days_data/middle_files_7days/'
output_path = '../Lerwick_7days_data/middle_files_7days/merged'
os.makedirs(output_path, exist_ok=True)

dir_lists = ['dir1','dir2','dir3','dir4','dir5','dir6','dir7']
            #0       1       2      3      4     5      6  
#_____________


fl_path = main_temp +dir_lists[ijk]
csv_files = [file for file in os.listdir(fl_path) if file.endswith('.csv')]
for csv_file in csv_files:
    #print(csv_file)
   #if csv_file == 'LP30S007.csv': #29S016 # LP29S005
       
        for iii in range(0,7):  
            #print('______________')
            

            main_path = main_temp+dir_lists[iii]                    
            file_path = os.path.join(main_path, csv_file)
            print(file_path)
            if os.path.isfile(file_path):
                df_start = pd.read_csv(file_path)
                # Replace None with empty strings for consistent handling
                #df_start.fillna('', inplace=True)                
                # Removing rows where 15h, 16h, or 17h is empty or contains only spaces
               # df = df_start[~(df_start[hour_lists[iii][0]].astype(str).str.strip() == '') & ~(df_start[hour_lists[iii][1]].astype(str).str.strip() == '') & ~(df_start[hour_lists[iii][2]].astype(str).str.strip() == '')]

                ######################################################################
                # open below if and close the rest after it to find out 999 values in df['MM']
                # if df['MM'].astype(str).eq('999').any():
                #     print(file_path)
                ######################################################################             
                
                df = df_start.copy()

                # Apply the transformation using .loc
                df.loc[:, 'T11'] = df['T11'].apply(transform_day_type)
                #df = main_transformation(df) # type-i hamar a naxord codic mnacac
                

            dfs.append(df)
        
        # Concatenate the data collected from different directories horizontally
        if dfs:
            merged_df = pd.concat(dfs, axis=1)
            merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
            #merged_df = merged_df.sort_values(['MM', 'DD', 'YYYY']).reset_index(drop=True)
            collected_data.append(merged_df)

        # Combine all collected data into a single DataFrame
        final_df = pd.concat(collected_data, ignore_index=True)
        
        # Reorder the columns to have the desired order
        metadata_columns = ['filename', 'YYYY', 'MM', 'DD', 'task', 'T11']
        hour_columns = [f"{i}h" for i in range(24)]
        iqr_columns = [f"IQR_{i}h" for i in range(24)]
        final_columns = metadata_columns + hour_columns + iqr_columns
        #print(final_columns)
        #____________________________________________________________________________
        # # Flatten the column names and ensure the correct order
        # final_df.columns = pd.Index([col.split('_')[0] if col in metadata_columns else col for col in final_df.columns])
        # final_df = final_df.groupby(level=0, axis=1).first()
        #____________________________________________________________________________

            # Ensure all expected columns are present
        for col in final_columns:
            if col not in final_df.columns:
                final_df[col] = np.nan
        # Save the final DataFrame to a CSV file
        #final_df = final_df[final_columns] # 20/06/2025
        merged_file_path = os.path.join(output_path, 'merged_' + csv_file)
        final_df.to_csv(merged_file_path, index=False)
        # print(f"{csv_file}")
        #----------------------------------------
        #empty the dataFrames
        df = pd.DataFrame()
        df_aggregated = pd.DataFrame()
        df_result = pd.DataFrame()
        merged_df = pd.DataFrame()
        df_main = pd.DataFrame()
        dfs = []
        final_df = pd.DataFrame()
        collected_data =[]

     
    
