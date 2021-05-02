""" read lims.txt
    save the extract in data frame csv file

"""

import csv
import pandas as pd
import os

def find_char_positions(string, target_ch):
    # This function find all positions of char '|' in a string
    # return a list of all positions
    return [i for i, ch in enumerate(string) if ch == target_ch]


# define the source file and output file
source_file_name = 'lims.txt'
source_file_folder = os.getcwd() + '//source_files'
source_file = os.path.join(source_file_folder,source_file_name)
output_file_name = 'pathology_report.csv'
output_file_folder = os.getcwd() + '//transition_files'
output_file = os.path.join(output_file_folder,output_file_name)

patho_data =[]
prefix_list = ['PID','OBR','OBX']
column_names = ["patient_id", "study_id",  "date_of_pathology", "pathology" ]
temp = []
print("Starting...")               
with open(source_file) as txt_file:
    txt_reader = csv.reader(txt_file)
    line_count = 0
    for row in txt_reader:
        patho_string = ''.join(row)
        prefix = patho_string[0:3]
        if prefix in prefix_list:                
            vl_pos = find_char_positions(patho_string, '|')
            pos = prefix_list.index(prefix)        
            if pos == 0: #patient_id                 
                temp.append(patho_string[vl_pos[2]+4:vl_pos[3]])
            elif pos == 1:
                temp.append(patho_string[vl_pos[2]+1:vl_pos[3]])
                d = patho_string[vl_pos[6]+1:vl_pos[7]] #date_of_pathology
                temp.append(d)
            elif pos == 2:
                temp.append(patho_string[vl_pos[4]+1:vl_pos[5]])
                if len(temp) == len(column_names):
                    patho_data.append(temp)
                else:
                    print("error")                    
                temp = []

df = pd.DataFrame(patho_data, columns = column_names)
df.to_csv(output_file, index = False, header=True)
print("Convert lims.txt to dataframe completed") 
        
        
        


