import pandas as pd
import re
import datetime as dt
import numpy as np

my_dir = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\dfs"

def import_ethogram(base_dir):
    df = pd.read_csv("{}\\Ethogram - Trainers.csv".format(base_dir))
    return df

def import_dogs(base_dir):
    df = pd.read_csv("{}\\Data Collection - Dogs.csv".format(base_dir), \
        usecols=['Code','Name', 'Breed', 'Sex', 'DOB', 'DOA', 'Source', 'PR Sup', 'Status', 'End Date'] )
    return(df)

def categories2numbers(df):
    # ethogram trainers column names
    # list of columns that need to have text dropped
    cols = ['Familiarisation-Response [Oriented to Handler]',
    'Familiarisation-Response [Exploration]',
    'Familiarisation-Response [Waiting]',
    'Call Back-Response',
    'Walking-Distractibility',
    'Walking-Pull on leash',
    'Walking-Pull strength',
    'Walking-Initiative',
    'Standing-Response',
    'Sitting-Response',
    'Lying-Response',
    'Lying-Settled',
    'Body check-Table',
    'Body check-Response',
    'Distractions-Pull on leash',
    'Distractions-Pull strength',
    'Distractions-Human',
    'Kong-Presentation-Response',
    'Kong-Interaction-Response to stimulus',
    'Kong-Interaction-Response to handler',
    'Kong-Interaction-Back',
    'Kong-Return-Handler',
    'Dog-Response',
    'Dog-Call Back Response',
    'Crate-Entering',
    'Crate-Behaviours [Settled]',
    'Crate-Behaviours [Sniffing/Exploring ]',
    'Crate-Behaviours [Actively Seeking Attention]',
    'Crate-Behaviours [Digging]',
    'Crate-Behaviours [Nudging Crate]',
    'Crate-Behaviours [Pawing]',
    'Crate-Behaviours [Whining]',
    'Crate-Behaviours [Barking]',
    'Crate-Self-Modulation',
    'Crate-Stress',
    'Petting-Handler-Stimulus',
    'Petting-Handler-Holding dog',
    'Petting-Confidence-During',
    'Petting-Responsiveness-After',
    'Isolation-Response [Time oriented]',
    'Isolation-Response [Exploration]',
    'Isolation-Response [Unsettled/Pacing]',
    'Isolation-Response [Whining]',
    'Isolation-Response [Barking]',
    'Reunion-Response',
    'Noise-Confidence',
    ]
    
    for col in cols:
        df[col] = df[col].str[:1]
    return(df)

################################    Main Start     ################################
    
# importing and processing ethogram dataframe
df_ethogram = import_ethogram(my_dir)
df_ethogram = categories2numbers(df_ethogram)
df_ethogram.shape

# to be developed:
    # subsetting columns accounding to text pattern
    # cols = [s for s in df_ethogram.columns if "Time (MM:SS)" in s]

    # this is how we can identify duplicate rows
    #for (dog, date) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Date'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
    #    print(df_ethogram[(df_ethogram['Dog code'] == dog) & \
    #        (df_ethogram['Data Collection Date'] == date)].mean())
    
# this is how we can take a mean of the duplicate rows
# df_ethogram.groupby(['Dog code', 'Data Collection Number']).mean()

# importing dogs information
df_dogs = import_dogs(my_dir)
# creating a columns for Litter
df_dogs['Litter'] = df_dogs['Name'].str[:1]

# merging ethogram and dogs dataframes
df = pd.merge(df_dogs, df_ethogram,  right_on  = 'Dog code', left_on = 'Code', how = 'right')
# drop column Dog code because it is the same as Code
df.drop(columns = 'Dog code', inplace = True)
# changing the order of the columns
df = df[['Name','Code','Data Collection Number', 'Assessor',
 'Breed', 'Sex', 'Litter', 'Source', 'PR Sup', 'DOB', 'DOA', 
 'Data Collection Date', 'End Date', 'Status', 'Timestamp'] 
  + df.columns.to_list()[15:]]
#save to csv file
df.to_csv('%s\\21-03-11_Ethogram-Trainers.csv' % my_dir , index = False)

################################      Main End       ################################
