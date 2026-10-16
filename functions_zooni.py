import pandas as pd
import numpy as np
import re
from collections import Counter
import ast

hour_lists = [['0h','1h','2h'],['3h','4h','5h'],['6h','7h','8h'],['9h','10h','11h'],
             ['12h','13h','14h'],['15h','16h','17h'],['18h','19h','20h'],
             ['21h', '22h','23h']]

iqr = [['IQR_0h','IQR_1h','IQR_2h'],['IQR_3h','IQR_4h','IQR_5h'],['IQR_6h','IQR_7h','IQR_8h'],
       ['IQR_9h','IQR_10h','IQR_11h'],['IQR_12h','IQR_13h','IQR_14h'],['IQR_15h','IQR_16h','IQR_17h'],
       ['IQR_18h','IQR_19h','IQR_20h'],['IQR_21h', 'IQR_22h','IQR_23h']]


# Function to flatten nested lists within the value field
def flatten_value_field(data, id, filename):
    flattened_data = []

    def process_entry(entry, parent_task=None, parent_task_label=None):
        if entry['task'] == 'T16':
            return  # Skip this entry

        if isinstance(entry['value'], list):
            for sub_entry in entry['value']:
                if sub_entry.get('task') == 'T16':
                    continue  # Skip this sub-entry
                
                flat_entry = {
                    'id': id,
                    'filename': filename,
                    'task': parent_task if parent_task else entry['task'],
                    'task_label': parent_task_label if parent_task_label else entry['task_label'],
                    'sub_task': sub_entry.get('task', None),
                    'sub_task_label': sub_entry.get('task_label', None),
                    'value': sub_entry.get('value', None),
                }
                flattened_data.append(flat_entry)
                # Recursive call to handle deeper nested lists
                if isinstance(sub_entry.get('value', None), list):
                    process_entry(sub_entry, parent_task=sub_entry.get('task'), parent_task_label=sub_entry.get('task_label'))
        else:
            flat_entry = {
                'id': id,
                'filename': filename,
                'task': entry['task'],
                'task_label': entry['task_label'],
                'sub_task': None,
                'sub_task_label': None,
                'value': entry['value'],
            }
            flattened_data.append(flat_entry)

    for entry in data:
        process_entry(entry)

    return flattened_data
#######################

# Function to flatten nested lists within the value field
def flatten_value_DayType(data, id, filename):
    flattened_data = []

    def process_entry(entry, parent_task=None, parent_task_label=None):
        # if entry['task'] == 'for skipping':
        #     return  # Skip this entry

        if isinstance(entry['value'], list):
            for sub_entry in entry['value']:
                # if sub_entry.get('task') == 'skiiping task':
                #     continue  # Skip this sub-entry
                
                flat_entry = {
                    'id': id,
                    'filename': filename,
                    'task': parent_task if parent_task else entry['task'],
                    'task_label': parent_task_label if parent_task_label else entry['task_label'],
                    'sub_task': sub_entry.get('task', None),#before 21/06/2025  # sub_entry.get('task'),
                    'sub_task_label':  sub_entry.get('task_label', None),#sub_entry.get('task_label'),
                    'value': sub_entry.get('value', None),
                }
                flattened_data.append(flat_entry)
                # Recursive call to handle deeper nested lists
                if isinstance(sub_entry.get('value', None), list):#, list):
                    process_entry(sub_entry, parent_task=sub_entry.get('task'), parent_task_label=sub_entry.get('task_label'))
        else:
            flat_entry = {
                'id': id,
                'filename': filename,
                'task': entry['task'],
                'task_label': entry['task_label'],
                'sub_task': None,#entry.get('task'),
                'sub_task_label':  None,
                'value': entry['value'],
            }
            flattened_data.append(flat_entry)

    for entry in data:
        process_entry(entry)

    return flattened_data


######
def clean_string(value):
    if pd.isna(value):
        return value
    # If value is a float or int, return as is
    if isinstance(value, (int, float)):
        return value
    # Convert the value to string first
    value_str = str(value)
    # Use regex to remove non-numeric characters except minus sign and decimal point
    cleaned_value = re.sub(r'[^0-9.-]', '', value_str)
    # Remove leading and trailing non-numeric characters
    #cleaned_value = re.sub(r'^\D+|\D+$', '', cleaned_value)
    return cleaned_value

######
def fig_name1(subject_data):
    fig_n = []
    for entry in subject_data:
       flat_entry = {
           'id': id,  # Include the id in each entry
           'Filename': entry['Filename'],
           
           }
       fig_n.append(flat_entry)
    return fig_n

def fig_name2(subject_data):
    fig_n = []
    for entry in subject_data:  # Use .items() to get both the id and the entry
        if 'Filename' in entry:   
            flat_entry = {
                #'id': id,  # Include the id in each entry
                'Filename': entry['Filename'],
            }
            fig_n.append(flat_entry)
    return fig_n

def fig_name3(subject_data):
    if not isinstance(subject_data, dict):
        raise ValueError("subject_data should be a dictionary")
    
    filenames = []
    for entry in subject_data.values():  # Use .values() to get the entries directly
        if 'Filename' in entry:
            filenames.append(entry['Filename'])
    return filenames

def fig_name(cell_data):
    filenames = []
    
    # Split the cell data into individual lines
    #lines = cell_data.strip().split('\n')
    
    for line in cell_data:
        # Skip the last 3 symbols and extract the last 12 symbols
        if len(line) > 15:  # Ensure the line is long enough
            filename = line[-15:-7]  # Slice to get the last 12 symbols, skipping the last 3
            filenames.append(filename)
    
    return filenames


#----------------------
#2nd stage

# def split_values(value):
#     # Split by ';' or ':' and filter out empty strings
#     return [part for part in re.split(r'[;:]', value) if part]

def normalize_dd(value):
# Remove brackets if they exist and split by semicolon
    #return value.strip('[]').split(';')
    #or below
    if pd.isna(value) or value == "":
        return []  # Return an empty list if value is NaN
    return str(value).split(';')  # Split by semicolon
#---------------------------------
# def most_common_list(lists):
#     # Convert lists to tuples to make them hashable for Counter
#     tuple_lists = [tuple(lst) for lst in lists]
#     counter = Counter(tuple_lists)
#     most_common_tuple, _ = counter.most_common(1)[0]
#     # Convert the most common tuple back to a list
#     return list(most_common_tuple)

# def adjust_dd_group(group):
#     all_same = group['DD'].apply(lambda x: x == group['DD'].iloc[0]).all()
#     if not all_same:
#         most_common_dd = most_common_list(group['DD'])
#         group['DD'] = [most_common_dd] * len(group)
#     return group

#------------------------------------

# def fill_missing_years(df, filename_year):
#     df['MM_YYYY'] = df['MM_YYYY'].apply(lambda x: x if '-' in x else f'{x}-{filename_year}')
#     return df


# def most_common_list(lst):
#     lst = [tuple(sublist) for sublist in lst]  # Convert sublists to tuples to make them hashable
#     most_common = Counter(lst).most_common(1)[0][0]
#     return list(most_common)

# def adjust_dd_group(group):
#     # all_same = group['DD'].apply(lambda x: x == group['DD'].iloc[0]).all()
#     # if not all_same:
#     #     most_common_dd = most_common_list(group['DD'])
#     #     group['DD'] = [most_common_dd] * len(group)
#     if not group['DD'].apply(lambda x: x == group['DD'].iloc[0]).all():
#           most_common_dd = group['DD'].mode()[0]  # Use mode() to find the most common DD
#           group['DD'] = [most_common_dd] * len(group)
#     #print(f"Adjusted DD values:\n{group['DD']}")  # Debug: Print adjusted DD values
#     return group

#==========================
def most_frequent_values_for_length(col):
    # Count the occurrences of each unique list while preserving order
    list_counts = Counter(tuple(sublist) for sublist in col)
    # Find the list with the highest frequency
    most_common = list_counts.most_common(1)[0][0]
    return list(most_common)

def adjust_hh_group(group,iii):
    for k in range (0,3):
        all_same = group[hour_lists[iii][k]].apply(lambda x: x == group[hour_lists[iii][k]].iloc[0]).all()
        if not all_same:
            most_common_hh = most_common_list(group[hour_lists[iii][k]])
            group[hour_lists[iii][k]] = [most_common_hh] * len(group)
        return group


#-------------------------
def most_common_list(dd_series):
    # Count the occurrences of each unique list while preserving order
    list_counts = Counter(tuple(sublist) for sublist in dd_series)
    # Find the list with the highest frequency
    most_common = list_counts.most_common(1)[0][0]
    return list(most_common)

# Function to adjust the 'DD' column within each group
def adjust_dd_group(group):
    all_same = group['DD'].apply(lambda x: x == group['DD'].iloc[0]).all()
    if not all_same:
        most_common_dd = most_common_list(group['DD'])
        group['DD'] = [most_common_dd] * len(group)
    return group


def count_items(cell):
    if pd.isna(cell):# or cell == "":
        return '' 
    else:
        return len(re.split(r'[;,:]', cell))#len(cell.split(';'))

def most_common_in_group(group):
    counter = Counter(group)
    most_common_string, _ = counter.most_common(1)[0]
    return most_common_string

def is_numerical(cell):
    if pd.isna(cell) or cell.strip() == '':
        return False
    # Use a regular expression to split by either ";" or ","
    items = re.split(r'[;,:]', cell)
    return all(item.isdigit() for item in items)

#------------after merging

# Function to aggregate and keep specific columns
def aggregate_group(group, iii):
   return pd.Series({
        'filename':group['filename'].iloc[0],
        'YYYY': group['YYYY'].iloc[0],
        'MM': group['MM'].iloc[0],#mode().iloc[0] if not group['MM'].mode().empty else np.nan,  
        'DD': group['DD'].iloc[0],
        'task': group['task'].iloc[0],#.mode().iloc[0] if not group['task'].mode().empty else np.nan,  
        'T11': group['T11'].mode().iloc[0] if not group['T11'].mode().empty else np.nan,        
        hour_lists[iii][0]: group[hour_lists[iii][0]].mode().iloc[0] if not group[hour_lists[iii][0]].mode().empty else np.nan,#.median(),
        hour_lists[iii][1]: group[hour_lists[iii][1]].mode().iloc[0] if not group[hour_lists[iii][1]].mode().empty else np.nan,#.median(),
        hour_lists[iii][2]: group[hour_lists[iii][2]].mode().iloc[0] if not group[hour_lists[iii][2]].mode().empty else np.nan,#.median(),
        iqr[iii][0]: calculate_iqr(group[hour_lists[iii][0]]),
        iqr[iii][1]: calculate_iqr(group[hour_lists[iii][1]]),
        iqr[iii][2]: calculate_iqr(group[hour_lists[iii][2]])
    })


#------------

# df['count'] = df['DD'].apply(count_items)
# per_task = df.groupby('task')['count'].apply(most_common_in_group)

def replace_with_most_frequent(strings):
    series = pd.Series(strings)
    non_nan_series = series.dropna()   
    if not non_nan_series.empty:
        counter = Counter(non_nan_series)
        most_common_string, _ = counter.most_common(1)[0]
        series_filled = series.fillna(most_common_string)
        return [most_common_string if s != most_common_string else s for s in series_filled]
    return strings


# # Function to replace NaN values with the most frequent (mode) value
# def replace_with_most_frequent(strings):
#     series = pd.Series(strings)
#     non_nan_series = series.dropna()  # Drop NaN values for mode calculation
#     if not non_nan_series.empty:
#         most_common_value = non_nan_series.mode().iloc[0]  # Calculate mode and take the first value if multiple
#         series_filled = series.fillna(most_common_value)
#         return [most_common_value if pd.isna(s) else s for s in series_filled]
#     return strings


#def replace_with_most_frequent2(strings):
def replace_with_most_frequent2(strings):
    def extract_day_type(value):
        match = re.search(r'Day type (\d+[a-zA-Z]*)', value)
        return match.group(1)  if match else value
    # Convert the input list to a Pandas Series, treating 'None' string and None as NaN
    series = pd.Series(strings).replace({'None': pd.NA, None: pd.NA,'': pd.NA})
    # Drop NaN values from the series to focus on non-null values
    non_nan_series = series.dropna()
    # Initialize fill_value
    fill_value = None
    
    if not non_nan_series.empty:
        # Filter values that start with 'Day type'
        #day_type_values = [item for item in non_nan_series if str(item).startswith('Day type') and item != 'It is not clear']
        day_type_values = [extract_day_type(item) for item in non_nan_series if str(item).startswith('Day type') and item != 'It is not clear']
        if day_type_values:
            # If there are values starting with 'Day type', find the most frequent one
            day_type_counter = Counter(day_type_values)
            fill_value, _ = day_type_counter.most_common(1)[0]

    # # Ensure fill_value is set, otherwise raise an error
    if fill_value is None:
        #raise ValueError("No 'Day type'")
        return series#.tolist()

    # Fill NaN values in the series with the determined fill value
    series_filled = series.apply(lambda x: extract_day_type(x) if pd.notna(x) and x != 'It is not clear' else fill_value)
    #series_filled = series.fillna(fill_value)        
    return series_filled#.tolist()
    #return series.tolist()


# def transform_day_type(series):
#     def extract_day_type(value):
#         if isinstance(value, str):
#             # Updated regex pattern to match both variations
#             pattern = r'Day type (\d+[a-zA-Z]*)'
#             match = re.search(pattern, value)
#             if match:
#                 # Return only the first matched day type
#                 return match.group(1)
#         return value  # Return the original value if it's not a string
    
#     return series.apply(extract_day_type)

def transform_day_type(value):
    if isinstance(value, str):
        if re.match(r'0a', value) or re.match(r'0a or 0b or 0c', value):
            return '0'
        elif re.match(r'1a or 1b or 1c', value):
            return '1'
        elif re.match(r'2a or 2b or 2c', value):
            return '2'       
        elif value == 'It is not clear':
            return 'Undefined'
        elif value == 'Empty':
            return 'Undefined'
         
    return value

def replace_undefined(series):
    return series.fillna('Undefined').replace(['None', 'Undefined'], 'Undefined')

def most_frequent(series):
    #return series.mode()[0] if not series.mode().empty else 'Undefined'
    filtered_series = series.dropna().replace(['None', ' '], pd.NA).dropna()
    if filtered_series.empty:
        return 'Undefined'
    return filtered_series.mode()[0] if not filtered_series.mode().empty else 'Undefined'

def main_transformation(df):
    df = df.copy()  # Work on a copy to avoid SettingWithCopyWarning
    
    # Replace None/NaN/Undefined in T11 with 'Undefined'
    df['T11'] = replace_undefined(df['T11'])
    
    t14_count = (df['task'] == 'T14').sum()
    t15_count = (df['task'] == 'T15').sum()
    t43_count = (df['task'] == 'T43').sum()
    t12_count = (df['task'] == 'T12').sum()
    t13_count = (df['task'] == 'T13').sum()

    if t14_count >= 2:
        most_common_14 = most_frequent(df.loc[df['task'] == 'T14', 'T11'])
        df['task'] = 'T14'
        df['T11'] = df.apply(lambda row: most_common_14 if row['T11'] != most_common_14 else row['T11'], axis=1)

    if t15_count >= 2 and t43_count >= 1:
        #combined_tasks = df[df['task'].isin(['T15', 'T43'])]
        most_common_t15 = most_frequent(df.loc[df['task'] == 'T15', 'T11'])       
        df.loc[df['task'].isin(['T15', 'T43']), 'T11'] = most_common_t15
        df.loc[~df['task'].isin(['T15', 'T43']), 'task'] = 'T15'
        df.loc[~df['task'].isin(['T15', 'T43']), 'T11'] = most_common_t15

    if t12_count >= 2 and t13_count >= 2:
        most_common_t12 = most_frequent(df.loc[df['task'] == 'T12', 'T11'])
        most_common_t13 = most_frequent(df.loc[df['task'] == 'T13', 'T11'])
        df.loc[df['task'] == 'T12', 'T11'] = most_common_t12
        df.loc[df['task'] == 'T13', 'T11'] = most_common_t13
        df.loc[~df['task'].isin(['T12', 'T13']), 'T11'] = 'Undefined'

    if (df['task'] == 'Undefined').sum() > 3:
        print(f"File path: {df.file_path}")
    
    return df

#-----------------

############################################################
def most_frequent_day_number(series):
    return series.mode()[0] if not series.mode().empty else 'qwerty'



def most_frequent_hour_values(df, hour_columns):
    most_frequent_values = {}
    for col in hour_columns:
        all_values = [val for sublist in df[col].astype(str).str.split(';').tolist() for val in sublist]
        most_frequent_values[col] = pd.Series(all_values).mode()[0]
    return most_frequent_values

def trim_hours_to_match_dd(row, hour_columns):#, most_frequent_values):
          
    list_dd = row['DD']#.split(';')
    most_frequent_dd = most_frequent_day_number(pd.Series(list_dd))
    dd_length = len(list_dd)      
    # Split and trim/pad hour columns
    for hour in hour_columns:
        hour_value = row[hour]
        # if pd.isna(hour_value):
        #     split_hour = [np.nan] * dd_length
        # else:
        split_hour = str(hour_value).split(';')
        #
        if len(split_hour) > dd_length:
            split_hour = split_hour[:dd_length]
        elif len(split_hour) < dd_length:
            split_hour.extend([np.nan] * (dd_length - len(split_hour)))
        # Join back into a string and update the row
        row[hour] = ';'.join(map(str, split_hour))    
        row['most_frequent_DD'] = most_frequent_dd
    return row


# Function to create a temporary DataFrame from a row
def expand_row(row, hour_columns):
    # Split 'DD' into a list
    day_number = row['DD']
    count_dd = len(day_number)
    #tasks = replace_with_most_frequent2(row['T11'])
    # Create a dictionary for the temporary DataFrame
    data = {
        'task': [row['task']] * count_dd,
        'T11': [row['T11']] * count_dd,#tasks*count_dd,
        'MM': [row['MM']] * count_dd,
        'YYYY': [row['YYYY']] * count_dd,
        'DD': day_number,
        'filename': [row['filename']] * count_dd
    }
    # Add hour columns to the data dictionary
    for hour in hour_columns:
        data[hour] = row[hour].split(';')
    return pd.DataFrame(data)

def calculate_iqr(series):
    return series.quantile(0.75) - series.quantile(0.25)





#________________________________________
invalid_month_count =0
def month_to_int(month):
    """Convert month in different formats to integer."""
    global invalid_month_count
    month = month.strip().lower()
    month_mapping = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6,
        '07': 7, '08': 8, '09': 9, '10': 10, '11': 11, '12': 12
    }
    #return month_mapping.get(month[:3], 1)  # Default to 1 (January) if not found
    #return month_mapping.get(month[:3], 999) # Default to 999 if not found
    if month[:3] not in month_mapping:
        invalid_month_count += 1
        return 999  # Default to 999 if not found
    return month_mapping[month[:3]]
# def standardize_month(month):
#     if len(month) <= 2 :
#         month = str(int(month)) 
#         return month#.zfill(2)  # Ensure it is two digits
#     if len(month) > 2: 
#         return month_to_int(month)
def standardize_month(month):
    global invalid_month_count
    # Convert integer month to string
    if isinstance(month, int):
        return str(month)
    month = month.strip()
    if month == 0:
        return 0
    # Convert string month to integer month
    if month.isdigit():
        return str(int(month))
    # Convert month name to integer month
    if len(month) <= 2 :
        #month = str(int(month)) 
        #return month
        try:
            return str(int(month))
        except ValueError:
            invalid_month_count += 1
            return '999'  
    if len(month) > 2: 
        return str(month_to_int(month))



#----------------------------------------

def split_and_fill(value, default_year):
    if not isinstance(value, str):
        value = str(value)
        #return pd.NA, pd.NA
    if '-' in value:
        parts = value.split('-')
    elif '/' in value:
        parts = value.split('/')
    else:
        parts = [value] 
    # if len(parts) == 2:
    #     return standardize_month(parts[0]), default_year#parts[1]
    # elif len(parts) == 1:
    #     return standardize_month(parts[0]), default_year
    # return pd.NA, pd.NA
    month = standardize_month(parts[0])
    return month, default_year
#____________________________



def standardize_year(year):
    year = str(year)
    if len(year) == 2:
        if year.startswith('9'):
            return '19' + year
    elif len(year) == 3:
        return '1' + year  # Assuming 3-digit years start with '1'
    elif len(year) == 4:
         return year


