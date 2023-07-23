
#------------------------------------------------------------------------------------#
#                                        Imports                                     #
#------------------------------------------------------------------------------------#

import pandas as pd
import seaborn as sns
import re
import datetime as dt
import numpy as np
#------------------------------------------------------------------------------------#
#                                        Setup                                       #
#------------------------------------------------------------------------------------#
# First Step: Import demographics data 
# Directory where to find 'Data Collection - Dogs.csv' file from Google Drive
dir_raw = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\0_raw"
# Select the demographics data to import 
data = pd.read_csv('{}\\Data Collection - Dogs.csv'.format(dir_raw), 
            usecols = ['Code', 'Name', 'Sex', 'Litter', 'DOB', 'Breed', 'Source', 'DOA','PR Sup', 'Coat Colour',  
            'Status', 'End Date', 'DC1', 'DC2'], 
            parse_dates= ['DOA', 'DOB', 'End Date', 'DC1', 'DC2'], dayfirst = True)

# Final Step: Export the dataframe as demographics data in processed folder
# Directory where to save the Demographics processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"
# Date when the file was created
date = '2021-06-08'

pd.set_option('display.max_rows', 150)

#------------------------------------------------------------------------------------#
#                           EDA - Exploratory Data Analysis                          #
#------------------------------------------------------------------------------------#

# Checking category types
for col in [ 'Sex', 'Breed', 'Source', 'PR Sup', 'Coat Colour',  'Status']:
    print('\nColumn Name & Types:', col, data.groupby(col).size())

# Checking if dogs from same Litter have the same Breed, Source and DOB (develop this into function?)
data.sort_values(['Litter', 'DOB'])[['Litter','Name', 'Breed', 'Source', 'DOB']].style.hide_index()
data.sort_values(['Litter', 'DOB'])[['Litter','Name', 'Breed', 'Source', 'DOB']].to_csv('{}\\Litters.csv'.format(dir_pro), index = False)

# Creating new variable 'Age at Start' 
# https://stackoverflow.com/questions/51918024/python-timedelta64-convert-days-to-months
data['Age at Start'] = (data['DOA']-data['DOB'])/np.timedelta64(1, 'M')
data['Age at Start'].plot.hist()

# Creating new variable 'Duration' 
# https://stackoverflow.com/questions/51918024/python-timedelta64-convert-days-to-months
data['Duration'] = (data['End Date'] - data ['DOA'])/np.timedelta64(1, 'M')
data['Duration'].plot.hist()

# Create new variable 'Outcome' with two categories, 'Success' and 'Fail'
data['Outcome'] = np.select( [
                            data['Status'] == 'W', 
                            data['Status'] == 'in Training',
                            data['Status'] == 'GD', 
                            data['Status'] == 'AD'
                            ], 
                            ['Fail', np.nan, 'Success', 'Success'])

print(data.groupby('Outcome').size())
# 27% failure rate (27 fails/104 total with outcome)

# Number of months dogs trainer before being withdrawn
data.loc[data['Outcome'] == 'Fail', 'Duration'].describe()
data.loc[data['Outcome'] == 'Fail', ['Duration', 'Name', 'DOA', 'End Date']].sort_values(by = 'Duration')
ax = sns.histplot(data.loc[data['Outcome'] == 'Fail', 'Duration'])
ax.set(xlabel = 'Duration [Months]', 
            ylabel = 'Dogs [Count]', 
                title='Training Duration for Dogs that Failed Training')


#------------------------------------------------------------------------------------#
#                           EDA - for Behaviour test in DC1 & DC2                           #
#------------------------------------------------------------------------------------#

# creating new dataframes for analysis
dc1 = data.loc[~data['DC1'].isnull() , ['Name', 'Sex', 'Breed', 'DOB', 'DC1'] ]
dc2 = data.loc[~data['DC2'].isnull() , ['Name', 'Sex', 'Breed', 'DOB', 'DC2'] ]

# N =  number of dogs
print('DC1: ',dc1['Name'].shape[0])
print('DC2: ',dc2['Name'].shape[0]-1) # I don't know why Mara is here 
# double check
#dc1['Name', 'DC1']
#dc1['Name', 'DC2']

# Sex
print('\n\nDC1', dc1.groupby('Sex').size())
print('\nDC2', dc2.groupby('Sex').size())

# Breed
print('\n\nDC1', dc1.groupby('Breed').size())
print('\nDC2', dc2.groupby('Breed').size())

# calculating age at DC1 and DC1 in months
# https://stackoverflow.com/questions/51918024/python-timedelta64-convert-days-to-months
dc1['DC1-Age'] = (dc1.DC1 - dc1.DOB)/np.timedelta64(1, 'M')
dc1['DC1-Age'].describe()
dc2['DC2-Age'] =(dc2.DC2 - dc2.DOB)/np.timedelta64(1, 'M')
dc2['DC2-Age'].describe()

#------------------------------------------------------------------------------------#
#                           Save Dataframe to Processed file                         #
#------------------------------------------------------------------------------------#
print(data.shape)
data.to_csv('{}\\{}_Demographics.csv'.format(dir_pro, date), index = False)
