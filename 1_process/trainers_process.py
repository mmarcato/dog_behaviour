#
#         This script takes csv raw files as they are in Google Sheets:
#         'Ethogram - Trainer.csv' and 'Data Collection - Dogs.csv' 
#         It merges them to create 'YYYY-MM-DD_Ethogram-Trainers.csv'
#         Drops the text of some variables
#

################################    Imports     ################################
import pandas as pd
import re
import datetime as dt
import numpy as np

################################    Setup     ################################

# Directory where to find Ethogram, Dogs and Data csv files
dir_raw = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\0_raw"
# Directory where to save the Processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"

date = '2021-06-08'

################################    Functions     ################################

def import_ethogram(base_dir):
    df = pd.read_csv("{}\\Ethogram - Trainers.csv".format(base_dir))
    # select columns that contain "Time ("
    cols = df.columns[df.columns.str.contains("Time \(")]
    # replace "." with :
    df.loc[:,cols] = df.loc[:,cols].replace(to_replace= "\.", value = ":", regex = True)
    # encodes assessors
    df['Assessor'] = df['Assessor'].map({'Allyce': 'A', 'Susan Turtle' : 'B',
                        'Susan Turtle ' : 'B', 'SusanTurtle' : 'B'})
    # replacing dog codes input incorrectly
    df['Dog code'].replace(['11-27-IL', '01-14-OL', '01-12-LN'], ['11-27-II', '01-14-LO', '01-12-LO'], inplace = True)   
    # 12-03-LM should be 12-02-LM
    df.iloc[118,1] = '12-02-LM'
    # 10-11-LJ should be 10-12-LJ
    df.iloc[91,1] = '10-12-LJ'

    # replacing NA/Inaudible with np.nan
    df.replace('NA/Inaudible', np.nan, inplace = True)
    
    return df

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

def import_dogs(base_dir):
    df = pd.read_csv("{}\\Data Collection - Dogs.csv".format(base_dir), \
        usecols=['Code','Name', 'Breed', 'Sex', 'DOB', 'DOA', 'Source', 'PR Sup', 
                    'Status', 'End Date'] )
    # creating a columns for Litter
    df['Litter'] = df['Name'].str[:1]
    return(df)

################################    Main Start     ################################
    
# importing and processing ethogram dataframe
df_ethogram = import_ethogram(dir_raw)
# transform categories to ordinal list by dropping text
df_ethogram = categories2numbers(df_ethogram)

# importing dogs information
df_dogs = import_dogs(dir_raw)

# merging ethogram and dogs dataframes
df = pd.merge(df_dogs, df_ethogram,  right_on  = 'Dog code', left_on = 'Code', how = 'right')
# drop column Dog code because it is the same as Code
df.drop(columns = 'Dog code', inplace = True)


### print missing data
# importing the data tab as a dataset to make sure that I found all the ethograms
data = pd.read_csv("{}\\Data Collection - Data.csv".format(dir_raw), skiprows = 1)
print('\znDogs listed as having an ethogram, but no ethogram was found')
print('DC1:', list(set(data.loc[data['Trainer-Ethogram'] =='Done', 'Code'].values) 
                        - set(df_ethogram['Dog code'].unique())))
print('DC2:', list(set(data.loc[data['Trainer-Ethogram.1'] =='Done', 'Code'].values) 
                        - set(df_ethogram['Dog code'].unique())))

### print duplicates
print('\nDogs with duplicate ethograms')
print(df[df.duplicated(subset = ['Code', 'Data Collection Date'])] \
                .loc[:,('Name', 'Data Collection Number')].drop_duplicates())

# to be developed - deal with duplicates:
    #print(df_ethogram[(df_ethogram['Dog code'] == dog) & (df_ethogram['Data Collection Date'] == date)].mean())
    
    # subsetting columns accounding to text pattern
    # cols = [s for s in df_ethogram.columns if "Time (MM:SS)" in s]

        # this is how we can identify duplicate rows
        #for (dog, date) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Date'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
        #    print(df_ethogram[(df_ethogram['Dog code'] == dog) & \
        #        (df_ethogram['Data Collection Date'] == date)].mean())   
    # this is how we can take a mean of the duplicate rows
    # df_ethogram.groupby(['Dog code', 'Data Collection Number']).mean()


# changing the order of the columns
df = df[['Name','Code','Data Collection Number', 'Data Collection Date',
    'Assessor', 'Breed', 'Sex', 'Litter', 'Source', 'PR Sup', 'DOB', 'DOA', 
    'End Date', 'Status'] + df.columns.to_list()[15:]]
    
#save to csv file
df.to_csv('{}\\{}_Ethogram-Trainers.csv'.format(dir_pro, date) , index = False)


################################      Main End       ################################

