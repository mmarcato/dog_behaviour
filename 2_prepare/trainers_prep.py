################################    Imports     ################################

import pandas as pd
import re
import datetime as dt
import numpy as np

################################    Setup     ################################

# Directory where to find Ethogram and Dogs csv files
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"
# Directory where to save the Processed file
dir_ana = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\2_prepare"
date = '2022-07-22'
# import ethogram scored by researcher 
data = pd.read_csv('{}\\{}_Ethogram-Trainers.csv'.format(dir_pro, date))


# drop columns that are unused for behavioural analysis
print(data.shape)
cols = data.columns
time = list(cols[cols.str.contains("Time \(")])
comments = list(cols[cols.str.contains("Comments")])
behaviours = ['Jumps', 'Shakes', 'Stretches', 'Whines',
'Short Barks', 'Continuous Barks', 'Growls', 'Scratches',
'Grooms', 'Yawns', 'Lip Smacking']
# drop time and comments
data.drop(columns = time + comments + behaviours, inplace = True)
print(data.shape)


# print ethograms with duplicated rows
print(data.groupby('Data Collection Number').size())
print("Duplicates")
print(data.loc[data.duplicated(['Code', 'Data Collection Date']),
        ['Name', 'Code', 'Data Collection Number','Assessor']])


################################   Intra-rater    ################################
intra_rater = data[data.duplicated(['Code', 'Data Collection Date', 'Assessor'], keep = False)]
print("Size of intra-rater dataset")
print(intra_rater.shape)
# saving intra_rater to csv
intra_rater.sort_values(by = ['Code', 'Assessor', 'Data Collection Date'])\
.to_csv('{}\\{}_Ethogram-Trainers_Intra-Rater.csv'.format(dir_ana, date), index = False)

################################   Inter-rater    ################################
inter_rater = data[data.duplicated(['Code', 'Data Collection Date'], keep = False) & ~ data.duplicated(['Code', 'Data Collection Date', 'Assessor'], keep = 'first')]

print("Manually check if these dogs do not have a second assessment for their ")
# use code below
# data.loc[data.Code == '12-03-LM',['Code', 'Data Collection Date', 'Assessor']]
print(inter_rater[~inter_rater.duplicated(['Code', 'Data Collection Date'], keep = False)][['Code', 'Data Collection Date', 'Assessor']].sort_values(by = ['Code', 'Data Collection Date', 'Assessor']))

# dropping dogs ethograms without duplicated data
inter_rater = inter_rater[inter_rater.duplicated(['Code', 'Data Collection Date'], keep = False)]
print("Size of inter-rater dataset")
print(inter_rater.shape)

# saving inter_rater to csv
inter_rater.sort_values(by = ['Code', 'Data Collection Date', 'Assessor'])\
.to_csv('{}\\{}_Ethogram-Trainers_Inter-Rater.csv'.format(dir_ana, date), index = False)


################################   Duplicates   ################################
# remove duplicates, keep last instance
data = data.drop_duplicates(subset = ['Code', 'Data Collection Number'], 
            keep = 'last', ignore_index = True)

# there should be DC1 - 101 and DC2 - 61, according to Data Collection - Data
print(data.groupby('Data Collection Number').size())



################################  DCs - Temporal  ################################
# retrieving name of dogs with dc1 and dc2
dog1 = data.loc[data['Data Collection Number'] == 1, 'Name']
dog2 = data.loc[data['Data Collection Number'] == 2, 'Name']
# list of dogs with dc1 and dc2
dogs = list(set(dog1) & set(dog2))
dcs = data[data['Name'].isin(dogs)]
print("Size of dcs dataset")
print(dcs.shape)
# saving dcs to csv
dcs.to_csv('{}\\{}_Ethogram-Trainers-DCS.csv'.format(dir_ana, date), index = False)


################################   DC1 - Litter   ################################
# creating new dataframe dc1 containing data collection 1 
dc1 = data[data['Data Collection Number'] == 1]
dc1.to_csv('{}\\{}_Ethogram-Trainers-DC1.csv'.format(dir_ana, date), index = False)

# checking the number of dogs in each litter
litters = dc1.groupby('Litter').size() 
print("Litters with only one dog:")
print(litters[litters == 1].index)
# removing litter with only one dog
dc1_litter = dc1[~ dc1.Litter.isin(litters[litters == 1].index)]
print(dc1_litter.shape)
dc1_litter.to_csv('{}\\{}_Ethogram-Trainers-DC1-Litter.csv'.format(dir_ana, date), index = False)


################################   DC2 - Litter   ################################
# creating new dataframe dc2 containing data collection 2 
dc2 = data[data['Data Collection Number'] == 2]
dc2.to_csv('{}\\{}_Ethogram-Trainers-DC2.csv'.format(dir_ana, date), index = False)

# checking the number of dogs in each litter
litters = dc2.groupby('Litter').size() 
print("Litters with only one dog:")
print(litters[litters == 1].index)
# removing litter with only one dog
dc2_litter = dc2[~ dc2.Litter.isin(litters[litters == 1].index)]
dc2_litter.to_csv('{}\\{}_Ethogram-Trainers-DC2-Litter.csv'.format(dir_ana, date), index = False)

