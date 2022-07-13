################################    Imports     ################################

import pandas as pd
import re
import datetime as dt
import numpy as np

################################    Setup     ################################

# Directory where to find Ethogram and Dogs csv files
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"
# Directory where to save the Processed file
dir_ana = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\2_analysis"
date = '2021-06-08'
# import ethogram scored by researcher 
data = pd.read_csv('{}\\{}_Ethogram-Trainers.csv'.format(dir_pro, date))


# print dogs with duplicated rows
print(data.shape)
print(data.groupby('Data Collection Number').size())
print(data.loc[data.duplicated(['Code', 'Data Collection Date', 'Assessor']), 
            ['Name', 'Data Collection Number']])


################################   Intra-rater    ################################
intra_rater = data[data.duplicated(['Code', 'Data Collection Date', 'Assessor'], keep = False)]
intra_rater.sort_values(by = ['Code', 'Assessor', 'Data Collection Date'])\
    .to_csv('{}\\{}_Ethogram-Trainers_Intra-Rater.csv'.format(dir_ana, date), index = False)

################################   Inter-rater    ################################
inter_rater = data[data.duplicated(['Code', 'Data Collection Date'], keep = False) &
                        ~ data.duplicated(['Code', 'Data Collection Date', 'Assessor'])]
# dropping dogs ethograms without duplicated data
inter_rater[inter_rater.duplicated(['Code', 'Data Collection Date'], keep = False)]\
    .sort_values(by = ['Code', 'Data Collection Date', 'Assessor'])\
    .to_csv('{}\\{}_Ethogram-Trainers_Inter-Rater.csv'.format(dir_ana, date), index = False)

inter_rater.shape

# remove duplicates
data = data.drop_duplicates(subset = ['Code', 'Data Collection Number'], 
                keep = 'last', ignore_index = True)
print(data.shape)
# there should be DC1 - 75 and DC2 - 51, according to Data Collection - Data
print(data.groupby('Data Collection Number').size())

################################   DC1 - Litter   ################################
# creating new dataframe dc1 containing data collection 1 
dc1 = data[data['Data Collection Number'] == 1]
dc1.to_csv('{}\\{}_Ethogram-Trainers-DC1.csv'.format(dir_ana, date), index = False)
# checking the number of dogs in each litter
dc1.groupby('Litter').size()
# removing litter with only one dog
dc1_litter = dc1[~ dc1.Litter.isin(['L', 'Q', 'V', 'Z'])]
dc1_litter.to_csv('{}\\{}_Ethogram-Trainers-DC1-Litter.csv'.format(dir_ana, date), index = False)


################################   DC2 - Litter   ################################
# creating new dataframe dc2 containing data collection 2 
dc2 = data[data['Data Collection Number'] == 2]
dc2.to_csv('{}\\{}_Ethogram-Trainers-DC2.csv'.format(dir_ana, date), index = False)

# checking the number of dogs in each litter
print(dc2.groupby('Litter').size())
# removing litter with only one dog
dc2_litter = dc2[~ dc2.Litter.isin(['L', 'T', 'A'])]
dc2_litter.to_csv('{}\\{}_Ethogram-Trainers-DC2-Litter.csv'.format(dir_ana, date), index = False)


################################  DCs - Temporal  ################################
# retrieving name of dogs with dc1 and dc2
dog1 = data.loc[data['Data Collection Number'] == 1, 'Name']
dog2 = data.loc[data['Data Collection Number'] == 2, 'Name']
# list of dogs with dc1 and dc2
dogs = list(set(dog1) & set(dog2))
dcs = data[data['Name'].isin(dogs)]
dcs.to_csv('{}\\{}_Ethogram-Trainers-DCS.csv'.format(dir_ana, date), index = False)