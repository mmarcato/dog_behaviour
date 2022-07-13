################################    Imports     ################################

import pandas as pd
import re
import datetime as dt
import numpy as np

################################    Setup     ################################

# Directory where to find Ethogram and Dogs csv processed files
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"
# Directory where to save the files ready for analysis  
dir_ana = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\2_analysis"
date = '2021-05-03'
# import ethogram scored by researcher 
data = pd.read_csv('{}\\{}_Ethogram-Researchers.csv'.format(dir_pro, date))


# print dogs with duplicated rows
print(data.shape)
print(data.groupby('Data Collection Number').size())
# Assessor A scored 07-01-LG (Goober), DC1 twice
# Assessor B scored 11-02-IM (Meeko), DC2 twice 
print(data.loc[data.duplicated(['Code', 'Data Collection Date', 'Assessor']), 
            ['Name', 'Data Collection Number']])


################################   Intra-rater    ################################
intra_rater = data[data.duplicated(['Code', 'Data Collection Date', 'Assessor'], keep = False)]
intra_rater.to_csv('{}\\{}_Ethogram-Researchers_Intra-Rater.csv'.format(dir_ana, date), index = False)

################################   Inter-rater    ################################
inter_rater = data[data.duplicated(['Code', 'Data Collection Date'], keep = False)]
inter_rater.drop_duplicates(['Code', 'Data Collection Date', 'Assessor'], keep = False)
inter_rater.to_csv('{}\\{}_Ethogram-Researchers_Inter-Rater.csv'.format(dir_ana, date), index = False)


# remove duplicates
data = data.drop_duplicates(subset = ['Code', 'Data Collection Number'], 
                keep = 'last', ignore_index = True)
print(data.shape)
#there should be DC1 - 57 and DC2 - 48
print(data.groupby('Data Collection Number').size())

################################   DC1 - Litter   ################################
# creating new dataframe dc1 containing data collection 1 
dc1 = data[data['Data Collection Number'] == 1]
dc1.to_csv('{}\\{}_Ethogram-Researchers-DC1.csv'.format(dir_ana, date), index = False)
# checking the number of dogs in each litter
print(dc1.groupby('Litter').size())
# removing litter with only one dog
dc1_litter = dc1[(dc1.Litter != 'L') & (dc1.Litter != 'T') & (dc1.Litter != 'Z')]
dc1_litter.to_csv('{}\\{}_Ethogram-Researchers-DC1-Litter.csv'.format(dir_ana, date), index = False)


################################   DC2 - Litter   ################################
# creating new dataframe dc2 containing data collection 2 
dc2 = data[data['Data Collection Number'] == 2]
dc2.to_csv('{}\\{}_Ethogram-Researchers-DC2.csv'.format(dir_ana, date), index = False)

# checking the number of dogs in each litter
print(dc2.groupby('Litter').size())
# removing litter with only one dog
dc2_litter = dc2[(dc2.Litter != 'L') & (dc2.Litter != 'T') & (dc2.Litter != 'Z')]
dc2_litter.to_csv('{}\\{}_Ethogram-Researchers-DC2-Litter.csv'.format(dir_ana, date), index = False)


################################  DCs - Temporal  ################################
# retrieving name of dogs with dc1 and dc2
dog1 = data.loc[data['Data Collection Number'] == 1, 'Name']
dog2 = data.loc[data['Data Collection Number'] == 2, 'Name']
# list of dogs with dc1 and dc2
dogs = list(set(dog1) & set(dog2))
dcs = data[data['Name'].isin(dogs)]
dcs.to_csv('{}\\{}_Ethogram-Researchers-DCS.csv'.format(dir_ana, date), index = False)