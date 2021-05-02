"""This file is used to create plots


"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##files required for merge and their file paths
source_file_folder = os.getcwd()+ '//source_files'
radiology_file = os.path.join(source_file_folder,'ris.csv')

##open files and get dataframes required for merge
df_radiology = pd.read_csv (radiology_file, header=0)
col_names = df_radiology.columns;
#column names = pat_id, pat_sex, pat_dob, id,	outcome_l, outcome_r, date
##year age
df_radiology.sort_values(by=col_names[2], inplace=True, ascending=False)
year_born = df_radiology[col_names[2]]
year_list = (year_born).unique()
ages = 2020-df_radiology['pat_dob']//10000
df_radiology['ages'] = ages
##plt age distribution
df_radiology.groupby('ages')['pat_id'].nunique().plot(kind = 'bar', color=plt.cm.Paired(np.arange(len(df_radiology))))
plt.xlabel('Age')
plt.ylabel('Number of patients')
plt.title('Patient Age Distrubution')
unique_patient_id = df_radiology[col_names[0]].unique()
print(unique_patient_id.size)
##plt case per paitient 
plt.figure()
ax = df_radiology.groupby('pat_id')['id'].nunique().plot(kind='bar')
ax.set_xticks(range(0,80, 5))
ax.set_xticklabels(range(1,80, 5))
plt.xlabel('Patient id')
plt.ylabel('Number of cases per patient')
plt.title('Number of cases per patient')
dups_pid = df_radiology.pivot_table(index=['pat_id'],aggfunc='size')
dups_pid.to_csv('transition_files/repeated_id.csv', index = True, header=True)
#print(dups_pid)
##
##plt case distribution
plt.figure()
df_radiology.groupby('ages')['id'].nunique().plot(kind = 'bar', color=plt.cm.Paired(np.arange(len(df_radiology))))
plt.title('Cases Distribution Across Age Group')
plt.ylabel('Number of Caces Per Age Group')
##plt radiologist opinions
fig, axes = plt.subplots( ncols=2)

axl=df_radiology.groupby(['ages','outcome_l']).size().unstack().plot(kind = 'bar', stacked=True, ax=axes[0])
axes[0].legend(loc='best')
axl.set_title('Radiologist Opinion on Left Side', fontsize=10)
axl.set_ylabel('Opinion/Scale')
axr = df_radiology.groupby(['ages','outcome_r']).size().unstack().plot(kind = 'bar', stacked=True, ax=axes[1])
axes[1].legend(loc='best')
##plt.title('Radiologist Opinion on Left Side Across Age Group')
axr.set_ylabel('')
axr.set_title('Radiologist Opinion on Right Side', fontsize=10)


plt.show()


