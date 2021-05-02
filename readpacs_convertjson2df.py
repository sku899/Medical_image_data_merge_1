""" read pacs.json.csv
    convert read row to JSON
    extract data by keys
    save the extract in data frame csv file

"""

import csv
import pandas as pd
import json
import os



# define the source file and output file
source_file_name = 'pacs.json.csv'
source_file_folder = os.getcwd() + '//source_files'
source_file = os.path.join(source_file_folder,source_file_name)
output_file_name = 'dicom_json.csv'
output_file_folder = os.getcwd() + '//transition_files'
output_file = os.path.join(output_file_folder,output_file_name)
print("Strating...")     
with open(source_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    column_names =[ 'patient_id', 'accession_number', 'date_of_study']
    tags = ['00100020','00080050','00080020']
    dicom_data = []
    for row in csv_reader:
        if line_count >1:
            #for test purpose, to check 2 records then break
            pass
        
        json_string = ", ".join(row)
        #print(json_string)
        json_object = json. loads(json_string)
        temp =[]         
        for pos, tag in enumerate(tags):
            val = ''.join(json_object[tag]['Value']) #convert list to string
            temp.append(val)
            
        dicom_data.append(temp)
        line_count += 1
    # cross check to make sure every line is processed    
    print(f'Processed {line_count} lines.')
    # create dataframe and save as csv file
    df = pd.DataFrame(dicom_data, columns = column_names)
    df.to_csv(output_file, index = False, header=True)
print("Convert pacs.json.csv to JSON completed") 
