#        This script takes raw csv files as they are in Google Sheets:
#        'Ethogram - Researchers.csv' and 'Data Collection - Dogs.csv' 
#        It merges them to create 'YYYY-MM-DD_Ethogram-Researchers.csv'
################################    Imports     ################################

import pandas as pd
import re
import datetime as dt
import numpy as np

################################    Setup     ################################

# Directory where to find Ethogram and Dogs csv files
dir_raw = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\0_raw"
# Directory where to save the Processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"

################################    Functions     ################################

def import_ethogram(base_dir):
    df = pd.read_csv("{}\\Ethogram - Researchers.csv".format(base_dir))
    # changes column order
    df = df[['Dog code', 'Data Collection Number', 'Data Collection Date'] 
             + df.columns.to_list()[2:-2]]
    # drop rows that Marinara assessed 
    df = df[~df['Assessor'].isin(['Marinara'])]    
    # encodes assessors
    df['Assessor'] = df['Assessor'].map({'Hazel': 'A', 'Con' : 'B'})
    # replace codes input incorrectly 
    df['Dog code'].replace(['11-01-IM'], ['11-01-LM'], inplace = True)
    return df

def import_dogs(base_dir):
    df = pd.read_csv("{}\\Data Collection - Dogs.csv".format(base_dir), \
        usecols=['Code', 'Name', 'Breed', 'Sex', 'DOB', 'DOA', 'Source', 'PR Sup', 'Status', 'End Date'] ) 
    # creating a columns for Litter
    df['Litter'] = df['Name'].str[:1]
    return(df)

def process(times, method):
    if times in ['NA', 'Na', 'na', 'n/a', 'n\a', 'NaN', np.nan, 'nan']:
        return(None)
    else:
        if method == 'duration':    
            d = dt.timedelta(0,0)
            #print(times)
            for time in times.split(";"):
                #print(time)
                if "-" in time:
                    ts = re.findall("\d\d:\d\d", time)
                    #print(ts)
                    d = d + dt.datetime.strptime(ts[1], "%M:%S") - dt.datetime.strptime(ts[0], "%M:%S")
                    #print(d)
                else:
                    d = d + dt.timedelta(0,1)
            return(d.total_seconds())

        if method == 'count':
            c = len(times.split(";"))
            return(c)

def calculate_behaviours(df):
    # short_vocalization = number of short bark events
    df['Short Barks Count'] = df['Short Barks'].apply(lambda x: process(x, 'count'))

    # cont_vocalization = number of continuous bark events
    df['Continuous Barks Duration'] = df['Continuous Barks'].apply(lambda x: process(x, 'duration'))
    df['Continuous Barks Count'] = df['Continuous Barks'].apply(lambda x: process(x, 'count'))

    # no_winning = number of winning events
    df['Whines Duration'] = df['Whines'].apply(lambda x: process(x, 'duration'))
    df['Whines Count'] = df['Whines'].apply(lambda x: process(x, 'count'))
    df['Shakes Count']  = df['Shakes'].apply(lambda x: process(x, 'count'))
    df['Jumps Count']  = df['Jumps'].apply(lambda x: process(x, 'count'))
    return(df)

def categories2numbers(df):
    # Task 1: delete text from ordinal variables
    # list of column names that need to have text dropped
    cols = ['Familiarisation-Response [Oriented to Handler]',
            'Familiarisation-Response [Exploration]',
            'Familiarisation-Response [Waiting]',
            'Call Back-Response',
            'Walking-Pull on leash',
            'Walking-Pull strength',
            'Walking-Initiative',
            'Standing-Response',
            'Sitting-Response',
            'Lying-Response',
            'Lying-Settled',
            'Body check-Response',
            'Distractions-Pull on leash',
            'Distractions-Pull strength',
            'Kong-Concentration-Response ',
            'Kong-Retrieve-Response to stimulus',
            'Kong-Retrieve-Response to assessor',
            'Kong-Retrieve-Back',
            'Dog-Response',
            'Dog-Call Back Response',
            'Crate-Entering',
            'Crate-Behaviours [Relaxing]',
            'Crate-Behaviours [Sniffing/Exploring]',
            'Crate-Behaviours [Attention Seeking]',
            'Crate-Behaviours [Digging]',
            'Crate-Behaviours [Licking/Mouthing]',
            'Crate-Behaviours [Whining]',
            'Crate-Behaviours [Barking]',
            'Isolation-Response [Time oriented]',
            'Isolation-Response [Exploration]',
            'Isolation-Response [Unsettled/Locomotion]',
            'Isolation-Response [Whining]',
            'Isolation-Response [Barking]']

    for col in cols:
        df[col] = df[col].str[:1]

    # Task 2: Number encode ordinal variables that didn't have numbering in original ethogram questions
    vars_crate = {'Relaxed/Indifferent':1, 'Uneasy but cooperative':2,
                    'Anxious':3 , 'Extremely Anxious': 4}
    vars_walk_dist = {'Hardly distracted':1, 'Somewhat distracted':2,
                        'Mostly distracted':3}
    vars_petting = {'Never' :1, 'Sometimes':2, 'Always': 3}
    

    df['Crate-Response'] = df['Crate-Response'].map(vars_crate)
    df['Walking-Distractibility'] = df['Walking-Distractibility'].map(vars_walk_dist)
    df_ethogram['Petting-Holding dog'] =df_ethogram['Petting-Holding dog'].map(vars_petting)
    
    return(df)


################################    Main Start     ################################

# importing and processing ethogram dataframe
df_ethogram = import_ethogram(dir_raw)
df_ethogram = calculate_behaviours(df_ethogram)
df_ethogram = categories2numbers(df_ethogram)

# to be developed:
    # drop the columns to keep the same assessor in two data collections
    #for (code, dc) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Number'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
        #print(code, date)
        #df_ethogram[df_ethogram['Dog code'] == code & df_ethogram['Data Collection Number']!= dc, 'Assessor' ]
# exploring any duplicates
print('Show duplicates')
for (dog, date) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Date'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
    print('\n',dog, date)
    #print(df_ethogram[(df_ethogram['Dog code'] == dog) & (df_ethogram['Data Collection Date'] == date)].mean())
        
# importing dogs information
df_dogs = import_dogs(dir_raw)
# merging ethogram and dogs dataframes
df = pd.merge(df_dogs, df_ethogram,  right_on  = 'Dog code', left_on = 'Code', how = 'right')
# drop column 'Dog code' because it is the same as 'Code'

df.drop(columns = 'Dog code', inplace = True)
# changing the order of the columns
df = df[['Name','Code','Data Collection Number', 'Data Collection Date',
    'Assessor', 'Breed', 'Sex', 'Litter', 'Source', 'PR Sup', 'DOB', 'DOA', 
    'End Date', 'Status'] + df.columns.to_list()[14:]]
  
#save to csv file
df.to_csv('{}\\2021-05-03_Ethogram-Researchers.csv'.format(dir_pro), index = False)

################################      Main End       ################################
