"""merage three sources files after they are converted to data frame CSV files

"""

import pandas as pd
import json
import os

##files required for merge and their file paths
source_file_folder = os.getcwd() + '//source_files'
transition_file_folder = os.getcwd()+ '//transition_files'
output_file_folder = os.getcwd()+ '//output_files'
radiology_file = os.path.join(source_file_folder,'ris.csv')
dicom_file = os.path.join(transition_file_folder,'dicom_json.csv')
pathology_file = os.path.join(transition_file_folder,'pathology_report.csv')
output_file = os.path.join(output_file_folder,'imaginary_partner_patients_newid.txt')
new_identifier_file = os.path.join(output_file_folder, 'indentifier_lookup.csv')
##open files and get dataframes required for merge
df_radiology = pd.read_csv (radiology_file, header=0)
df_dicom = pd.read_csv (dicom_file, header=0)
df_pathology = pd.read_csv (pathology_file, header=0)
df_identifier_tbl = pd.read_csv (new_identifier_file, header=0)

##define dictionary keys
dict_keys = ["patient_uid","sex","date_of_birth","studies", "rad", "patho"]
dict_rad_keys = ["side", "date", "opinion"]
dict_patho_keys = ["date", "opinion"]
# patient details: tuple of key, value pair of the dictionary
patient_details = []

#extract the unique patient id
patient_list = df_dicom[df_dicom.columns[0]].unique()

print("Starting")
with open(output_file, 'w') as file:
    for patient in patient_list:        
        
        patient_demographic = \
        df_radiology[df_radiology[df_radiology.columns[0]] == patient]
        
        ##add patient_uid, sex and date_of_birth
        ##set default value
        new_id = df_identifier_tbl[
            df_identifier_tbl[df_identifier_tbl.columns[0]] == patient].iloc[0,1]
        vals = [new_id, "F", ""]
        if patient_demographic.shape[0] >0:
            ##get demographics information
            row = patient_demographic.iloc[0, 0:3]
            ## change patient id to the format 1.2.3.4 from 1-2-3-4
            revised_id = new_id.replace('-','.')
            dob = str(row[2])
            ## modify date of birth to the format yyyy.mm.dd from
            ## yyyymmdd
            dob = dob[0:4] +'.' +dob[4:6]+'.' +dob[6:]
            vals = [revised_id, row[1], dob]

        ##get studies from dicom, only unique accesion number will be included
        study_list = df_dicom[df_dicom['patient_id'] == patient].iloc[:,1].unique()
        studies = []
        rad_list = []
        for study in study_list:
            studies.append(str(study))

        vals.append(studies)

        ##add radiology report information
        uni_study_list = study_list        
        sides =['L', 'R']
        rad_vals = []
        for study in uni_study_list:
            record = df_radiology.loc[(df_radiology["pat_id"] == patient) & (df_radiology["id"] == study)]
            if record.shape[0]>0:
                ##each record in radiology report present Left and Right sides
                for i in range(0, record.shape[0]):
                    for j in range(0,2):            
                    #rad_details.append((dict_rad_keys[0], sides[i]))
                        dos = str(record.iloc[i, 6])
                        dos = dos[0:4] +'.' +dos[4:6]+'.' +dos[6:]
                        rad_vals.append([sides[j], dos, record.iloc[i,4+j]])                        
            else:
                rad_vals.append([sides[0],"",""])
                rad_vals.append([sides[1],"",""])
                
        rad_details =[]
        
        for rad_val in rad_vals:
            for rad_key, rv in zip(dict_rad_keys, rad_val):
                rad_details.append((rad_key, rv))
            rad_dict = dict(rad_details)
            rad_list.append(rad_dict)
            
        vals.append(rad_list)        
        
        ##add pathology, this file only contains 6 records
        patho_vals = []
        patho_details=[]
        patho_list = []
        for study in study_list:
            patho_record = df_pathology[(df_pathology["patient_id"]==patient) & (df_pathology["study_id"] == study)]
            if patho_record.shape[0]>0:
                for i in range(0, patho_record.shape[0]):
                    dop = str(patho_record.iloc[i,2])
                    dop = dop[0:4] +'.' +dop[4:6]+'.' +dop[6:]
                    patho_vals.append([dop, patho_record.iloc[i,3]])

            else:
                patho_vals.append(["",""])

        for patho_val in patho_vals:
            for patho_key, pv in zip(dict_patho_keys, patho_val):
                patho_details.append((patho_key, pv))
            patho_dict = dict(patho_details)
            patho_list.append(patho_dict)

        vals.append(patho_list)
                        
        #add tuple pair of key and value to patient_details                                                 
        for pos, key in enumerate(dict_keys):
            patient_details.append((key, vals[pos])) 
        ##create dictionary
        patient_dict = dict(patient_details)
        ##write json obj to file
        file.write(json.dumps(patient_dict))
        file.write('\n')

print("Merge files with new identifier completed")
        

     
    

