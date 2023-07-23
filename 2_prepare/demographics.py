#                                        Imports                                     #

import pandas as pd
import re
import datetime as dt
import numpy as np

#------------------------------------------------------------------------------------#
#                                        Setup                                       #
#------------------------------------------------------------------------------------#
# Date when the file was created
date = '2021-06-08'

# Directory where to find the Demographics processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"
# Directory where to save the Demographics file ready for analysis  
dir_ana = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\2_prepare"

# Select the demographics data to import 
data = pd.read_csv('{}\\{}_Demographics.csv'.format(dir_pro, date), 
            usecols = ['Code', 'Name', 'DOB',  'Sex', 'Breed', 'Source', 'DOA','PR Sup', 'Coat Colour',  'Status', 'Label', 'End Date', 'Age at Start', 'Duration'], 
            parse_dates= ['DOA', 'DOB', 'End Date'], dayfirst = True)

# checking size and categories
print(data.shape)
print(data.groupby('Status').size())

# filtering out 'in Training' Status
data = data[data['Status'] != 'in Training']

# checking size and categories
print(data.shape)
print(data.groupby('Status').size())

#------------------------------------------------------------------------------------#
#                           Save Dataframe to file ready for Analysis                         #
#------------------------------------------------------------------------------------#

data.to_csv('{}\\{}_Demographics-Outcome.csv'.format(dir_ana, date), index = False)

