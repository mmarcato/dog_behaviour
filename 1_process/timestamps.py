

#
#         This script takes csv raw files as they are in Google Sheets:
#         'Ethogram - Trainers.csv' and 'Data Collection - Dogs.csv' 
#         It merges them to create 'YYYY-MM-DD_Ethogram-Trainers.csv'
#         Drops the text of some variables
#

#------------------------------------------------------------------------------------#
#                                        Imports                                     #
#------------------------------------------------------------------------------------#
import pandas as pd
import re
import datetime as dt
import numpy as np
pd.set_option('display.max_rows', None)

#------------------------------------------------------------------------------------#
#                                        Setup                                       #
#------------------------------------------------------------------------------------#

# Directory where to find Ethogram, Dogs and Data csv files
dir_raw = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\0_raw"
# Directory where to save the Processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"

date = '2022-11-16'

#------------------------------------------------------------------------------------#
#                                      Functions                                     #
#------------------------------------------------------------------------------------#

df_res = pd.read_csv("{}\\2023-07-22_Ethogram-Researchers.csv".format(dir_pro))
df_tra = pd.read_csv("{}\\2022-11-16_Ethogram-Trainers.csv".format(dir_pro))

info = ['Name', 'Data Collection Number', 'Code', 'Data Collection Date', 'Assessor']
ts_res = list(df_res.columns[df_res.columns.str.contains("Time \(")])
ts_tra = list(df_tra.columns[df_tra.columns.str.contains("Time \(")])

df_tra = df_tra[info + ['BT Start', 'BT Duration'] + ts_tra].set_index(['Name', 'Data Collection Number']).sort_index()
df_res = df_res[info + ts_res].set_index(['Name', 'Data Collection Number']).sort_index()


df_res.Assessor.replace({'A':'C', 'B':'D'}, inplace = True)
df_tra.shape
df_res.shape

df = pd.concat([df_tra, df_res], axis = 0)
df.sort_index().to_csv('{}\\{}_Timestamps.csv'.format(dir_pro, date))



set1 = set(list(df_tra.columns[df_tra.columns.str.contains("Time \(")])) 
set2 = set(list(df_res.columns[df_res.columns.str.contains("Time \(")])) 
set1 - set2
set2 - set1


col_times = list(df_research.columns[df_research.columns.str.contains("Time \(")])
df_times = df_research[col_info + col_times].sort_values(by = ['Data Collection Date', 'Dog code', 'Assessor'], ascending = False)
df_times.to_csv('{}\\{}_Timestamps.csv'.format(dir_pro, date), index = False)
