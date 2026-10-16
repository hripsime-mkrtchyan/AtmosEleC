# this code is for seperating from file the data. You should run the next code to get whole data 
#next code is 2nd_stage.py

import pandas as pd
import json
import csv
from ripsi_function_zooni_Y import flatten_value_DayType, fig_name, count_items, is_numerical
#import re

parsed_data = []
results = []

filenumber = ['1','2','3','4','5','6','7']

ijk =1

initial_file_dictionary = '../Lerwick_7days_data/data_7days'

#output_json="export_2730/processed/output_012_corrected.csv"
output_directory = '../Lerwick_7days_data/middle_files_7days'

output_final = output_directory +'/'+'day_'+filenumber[ijk]+'_results.csv'
#output_final = output_directory +'/day_'+filnames[ijk]+'.csv'
file_path = initial_file_dictionary +'/day-'+filenumber[ijk]+'-classifications.csv'


list_column = {'classification_id',	'user_name', 'user_id',	'user_ip',
               'workflow_id',	'workflow_name',	'workflow_version',	
               'created_at',	'gold_standard',	'expert','	metadata',	
               'annotations',	'subject_data',	'subject_ids' 
               }


#T9 date
#T11 day type
#T12 multiplier
#T7  "Gradient in open" records for hours
#T26 all "Gradient in Open" records
#T31  hours which have T7 records
#T13  Is the "Deflexion" column empty?
#T15 Deflexion hours
#T17 all deflexion values for T15 hours
#T18 Deflextion date

replacements = {
        'T11': 'day type',
    }


ignore_task = {'T16','',''} #t16 rectangle # t41 is sheet type(we may not need this as the sheets should be the same type)
sub_task_columns = [ 'T9','T11', 'T12', 'T7', 'T26', 'T31', 'T13', 'T15', 'T17', 'T18'] #t13 deflextion a
df_outcome = pd.DataFrame(columns=['id', 'filename',sub_task_columns])#sub_task_columns column which we need to extract

#df = pd.read_csv(file_path)#, delimiter='\t', header=None, names=['id', 'data'])
# Open the file in read mode
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    columns = next(reader)#first line
    main_df = pd.DataFrame(columns=columns)
    for row in reader: #reading by lines
        line_df = pd.DataFrame([row], columns=columns)        
        figure_name = fig_name(line_df['subject_data'])
        figName_df = pd.DataFrame(figure_name, columns=['Filename'])     
        main_df = pd.concat([line_df, figName_df], axis=1)#main_df = pd.concat([main_df, line_df], ignore_index=True)# Append the row DataFrame to the main DataFrame in each iteration
        parsed_data = []
        for index, row in main_df.iterrows():
            if pd.notna(row['annotations']):
                try:
                    json_data = json.loads(row['annotations'])
                    # for entry in json_data:
                    #     if entry.get('task') == 'T41':
                    #         val = entry.get('value', '')
                    #         if val == '"Gradient in Open" column has all rows filled with data':
                    #             entry['value'] = 11
                    #         elif val == '"Gradient in Open" column has only some rows filled with data':
                    #             entry['value'] = 22
                    #         elif val == '"Gradient in Open" column is empty':
                    #             entry['value'] = 33
                    #     #print("T41 entry before appending:", entry)
                    parsed_data.append({'subject_ids': row['subject_ids'], 'annotations': json_data, 'Filename':row['Filename']})
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for row {index}: {e}")



# Flatten the parsed data using the flatten_value_field function from hripsi_functions
 
            flattened_data = []
            
            for item in parsed_data:
                id = item['subject_ids']
                data = item['annotations']
                figname=item['Filename']
                #flattened_items = flatten_value_field(data, id, figname) with old function
                flattened_items = flatten_value_DayType(data, id, figname)
                flattened_data.extend(flattened_items)
         

            # Convert to DataFrame
            flattened_df = pd.DataFrame(flattened_data)
            filtered_df = flattened_df[flattened_df['sub_task'].notna()]
            filtered_df = filtered_df.copy()
            filtered_df['unique_id'] = filtered_df.groupby(['id', 'filename', 'task']).cumcount()
            
            # Pivot table creation with the unique identifier to handle duplicates
            pivot_table = filtered_df.pivot_table(
                index=["id", "filename", "task", "unique_id"], 
                columns="sub_task", 
                values="value", 
                aggfunc=lambda x: ' '.join(str(v) for v in x)
            )
            
            # Remove the unique identifier from the index and reset it
            pivot_table = pivot_table.reset_index().drop(columns=['unique_id'])
            
            # # Combine rows with the same id, filename, and task
            combined_df = pivot_table.groupby(['id', 'filename', 'task'], as_index=False).agg(lambda x: '//'.join(x.dropna().astype(str)))
            

            # Split rows based on the separator "//"
            separated_rows = []
            for _, row in combined_df.iterrows():
                max_splits = max(len(str(row[col]).split('//')) if pd.notna(row[col]) else 1 for col in combined_df.columns[3:])
                for i in range(max_splits):
                    new_row = row.copy()
                    for col in combined_df.columns[3:]:
                        if pd.notna(new_row[col]) and isinstance(new_row[col], str):
                            values = new_row[col].split('//')
                            new_row[col] = values[i] if i < len(values) else ''
                    separated_rows.append(new_row)

            separated_df = pd.DataFrame(separated_rows)

            # Ensuring T42 is after T9
            columns_order = ['id', 'filename'] +sub_task_columns
            # Add any missing columns from the data to the ordered list
            columns_order += [col for col in separated_df.columns if col not in columns_order]
 
                        # Handle missing columns
            for col in columns_order:
                if col not in separated_df.columns:
                    separated_df[col] = None

            # Reorder the columns
            separated_df = separated_df[columns_order]
            
            #pivot_table = flattened_df.pivot_table(index=["id", "filename"], columns="sub_task", values="value", aggfunc=lambda x: ' '.join(str(v) for v in x))
            # Reset index to turn MultiIndex into columns
           
            results.append(separated_df)
            del pivot_table
            del flattened_df


combined_df = pd.concat(results, ignore_index=True)
combined_df = combined_df.drop('T16', axis=1)
combined_df = combined_df.sort_values(by=['id'])

combined_df.to_csv(output_final, index=False) # we should save filtered_df this is for a test

    
    
    
    
    
    
    
    