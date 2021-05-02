""" Shift dates by days

"""

import datetime
import string
import os
import random
import pandas as pd

##files required for merge and their file paths
source_file_folder = os.getcwd()+ '//source_files'
transition_file_folder = os.getcwd()+ '//transition_files'
output_file_folder = os.getcwd()+ '//output_files'
ext_file = '.csv'
radiology_file_name = 'ris'
pathology_file_name =  'pathology_report'
dicom_file_name = 'dicom_json'
radiology_file = os.path.join(source_file_folder ,radiology_file_name + ext_file)
pathology_file = os.path.join(transition_file_folder,pathology_file_name + ext_file)
dicom_file = os.path.join(transition_file_folder,dicom_file_name + ext_file)
##open files and get dataframes required for merge

source_files = [dicom_file, pathology_file, radiology_file]
output_files = [os.path.join(output_file_folder, dicom_file_name + '_lookup' + ext_file),
                os.path.join(output_file_folder, pathology_file_name + '_lookup' + ext_file),
                os.path.join(output_file_folder, radiology_file_name + '_lookup' + ext_file)
                ]
col_names = [['date_of_study'], ['date_of_pathology'], ['pat_dob', 'date']]
print("Starting...")
for source_file, output_file, column_names in zip(source_files, output_files, col_names):
    df = pd.read_csv (source_file, header=0)
    for col_name in column_names:
        print(col_name)
        date_list = df[col_name]                                       
        new_dates = []
        for d in date_list:
            d_datetime_obj =  datetime.datetime.strptime(str(d), '%Y%m%d')
            days = random.randint(365, 5*365 )
            new_date = d_datetime_obj + datetime.timedelta(days=days)
            new_date_string = str(new_date.year) + \
                              str(new_date.month).rjust(2, '0') + \
                                  str(new_date.day).rjust(2, '0')
            new_dates.append(new_date_string)

        df["new_"+col_name ] = new_dates
    df.to_csv(output_file, index = False, header=True)

print("Jitter dates have been completed")







