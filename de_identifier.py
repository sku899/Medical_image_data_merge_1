"""This file create new identifiers and produce a lookup table in CSV file
 

"""

import string
import os
import random
import pandas as pd

#define the file
transition_file_folder = os.getcwd()+ '//transition_files'
output_file_folder = os.getcwd()+ '//output_files'
dicom_file = os.path.join(transition_file_folder,'dicom_json.csv')
output_file = os.path.join(output_file_folder,'indentifier_lookup.csv')

##open files and get dataframes required for merge
df_dicom = pd.read_csv (dicom_file, header=0)

patient_id_list = df_dicom[df_dicom.columns[0]].unique()
# ptient details: tuple of key, value pair of the dictionary
new_ids = []
char_list = string.hexdigits[0:16]
fix_prefix = ''
last_dot = 0
id_pair =[]
print("Starting...")
for patient_id in patient_id_list:
    new_id = ""
    if "." in patient_id:
        sep_char ="."
        max_number = 9
        start_pos = last_dot + 1
    else:
        sep_char ="-"
        max_number = 15
        start_pos = 0

    
    if len(fix_prefix) == 0 and sep_char ==".":        
        for pos, ch in enumerate(patient_id):
            if ch == sep_char:
                fix_prefix = fix_prefix + ch
                last_dot = pos
            else:
                new_char = char_list[random.randint(0,max_number)]
                fix_prefix = fix_prefix + new_char
        fix_prefix = fix_prefix[0:last_dot+1]
        start_pos = last_dot + 1
      

    is_repeated = True
    while is_repeated:
        for ch in patient_id[start_pos:]:
            if ch == sep_char:
                new_id = new_id + ch
            else:
                new_char = char_list[random.randint(0,max_number)]
                new_id = new_id + new_char

        if sep_char == ".":
            new_id = fix_prefix + new_id
        if not (new_id in new_ids):
            is_repeated = False
            new_ids.append(new_id)
    #print(f'{patient_id}, new id is {new_id}')
    id_pair.append([patient_id, new_id])

#print(new_ids)
df = pd.DataFrame(id_pair, columns = ["original", "new"])
df.to_csv(output_file, index = False, header=True)
print("New Identifiers have been created")
            
                                 
            
            
            
