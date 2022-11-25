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
pd.set_option('display.max_rows', None)

################################    Setup     ################################

# Directory where to find Ethogram, Dogs and Data csv files
dir_raw = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\0_raw"
# Directory where to save the Processed file
dir_pro = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\0_data\\1_process"

date = '2022-11-16'

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
    # replacing dog codes input written incorrectly (original code does not exist)
    df['Dog code'].replace(['11-27-IL', '01-14-OL', '01-12-LN'],\
                            ['11-27-II', '01-14-LO', '01-12-LO'], inplace = True)   
    # 12-03-LM should be 12-02-LM
    df.iloc[118,1] = '12-02-LM'
    # 10-11-LJ should be 10-12-LJ
    df.iloc[91,1] = '10-12-LJ'

    # replacing NA/Inaudible with np.nan
    df.replace('NA/Inaudible', np.nan, inplace = True)
    
    return df

def import_dogs(base_dir):
    df = pd.read_csv("{}\\Data Collection - Dogs.csv".format(base_dir), \
        parse_dates= ['DOA', 'DOB', 'End Date'], dayfirst = True, 
        usecols=['Code','Name', 'Breed', 'Sex', 'Source', 'Litter', 
                    'DOB', 'DOA', 'End Date', 'Status', 'Working'] )  #'PR Sup',
    print('Columns in Dog dataframe: \n', df.columns.tolist())
    print('Shape of Dog dataframe: \n', df.shape)

    # calculating duration of training
    df['Duration'] = df['End Date'] - df['DOA']

    # defining training outcome
    df.Status.replace({"CD" : "AD"}, inplace = True)
    df['Outcome'] = np.select( [df['Status'] == 'in Training',
                            df['Status'] == 'W', 
                            df['Status'] == 'GD', 
                            df['Status'] == 'AD'], 
                            [np.nan, 'Fail', 'Success', 'Success'])

    return(df)

def import_summary(base_dir):
    # base_dir = dir_raw
    df = pd.read_csv("{}\\Data Collection - Summary.csv".format(base_dir), 
            header = 1, parse_dates = ['Date', 'Date.1'],  dayfirst = True)
    df = df[['Code', 'Date', 'Date.1', 'BT Start', 'BT Start.1', 'BT Duration', 'BT Duration.1']]
    df.columns = ['Code', 'BT Date-1', 'BT Date-2', 'BT Start-1', 'BT Start-2', 'BT Duration-1', 'BT Duration-2']

    df = pd.wide_to_long(df, ["BT Date", "BT Start", "BT Duration"], sep = "-", j="DC", i='Code')

    print('Columns in Summary dataframe: \n', df.columns.tolist())
    print('Shape of Summary dataframe: \n', df.shape)
    return(df)

def categories2numbers(df):
    # ethogram trainers column names
    # list of columns that need to have text dropped
    cols = [
    'Familiarisation-Response [Oriented to Handler]', 
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
        df[col] = df[col].str[:1].astype(float)
        
    # scaling features that start at zero, so all of them start at 1
    for col in ['Dog-Response', 'Dog-Call Back Response', 'Petting-Responsiveness-After', 'Reunion-Response']:
        df[col] = df[col] + 1

    return(df)

def feature_extraction(var, df):
    return(pd.DataFrame({
        var + '_mean' : df.mean(axis = 1),
        var + '_prod' : df.prod(axis = 1)
        }))

def feature_engineering(df):
    # df = df_ethogram
    # list(df_ethogram.columns)
    print("Shape before feature engineering", df.shape)

    # familiarisation
    df = df.join(feature_extraction('S-Familiarisation-Handler', 
        df[['Familiarisation-Response [Oriented to Handler]', 
            'Familiarisation-Response [Waiting]']]))

        
    # walking pull on leash (walking, distraction)
    df = df.join(feature_extraction('S-Walking-Pull', 
                df[['Walking-Pull on leash', 'Walking-Pull strength']]))

    df = df.join(feature_extraction('S-Distractions-Pull',
            df[['Distractions-Pull on leash','Distractions-Pull strength']]))

    # difference between distractions and walking pull
    df['S-Walking-Distractions-Pull_mean'] = df['S-Distractions-Pull_mean'] - df['S-Walking-Pull_mean']
    df['S-Walking-Distractions-Pull_prod'] = df['S-Distractions-Pull_prod'] - df['S-Walking-Pull_prod']
    

    # obedience
    df = df.join(feature_extraction('S-Obedience', 
        df[['Standing-Response', 'Sitting-Response', 'Lying-Response']]))

    # body check 
    # df = df.join(feature_extraction('S-Sensitivity', 
    #     df[['Body check-Table','Body check-Response']].join(df['Body check-General [Licks]'].replace(['Yes', 'No'], [-1,0])).join(
    #         df['Body check-General [Mouths]'].replace(['Yes', 'No'], [-2,0]))
    #     ))
    df['S-Sensitivity_mean'] = df[['Body check-Table','Body check-Response']].mean(axis = 1)
    # .join(
    #         df['Body check-General [Licks]'].replace(['Yes', 'No'], [-1,0])).join(
    #         df['Body check-General [Mouths]'].replace(['Yes', 'No'], [-2,0]))


    # tea towel -> yes and nos into numbers by taking the mean considering the level of response
    df_towel = pd.DataFrame([df['Tea Towel-First Response [Indifferent]'].replace(['Yes', 'No'], [0,1]),
    df['Tea Towel-First Response [Change from Neutral]'].replace(['Yes', 'No'], [2,0]),
    df['Tea Towel-First Response [Turns head]'].replace(['Yes', 'No'], [3,0]),
    df['Tea Towel-First Response [Attempts to/Removes towel by moving]'].replace(['Yes', 'No'], [4,0]),
    df['Tea Towel-First Response [Attempts to/Removes towel with mouth]'].replace(['Yes', 'No'], [5,0]),
    df['Tea Towel-First Response [Plays]'].replace(['Yes', 'No'], [6,0])])
    df['S-Tea Towel-First Response' ] = df_towel.mean(axis = 0)

    df_towel = pd.DataFrame([df['Tea Towel-Second Response [Indifferent]'].replace(['Yes', 'No'], [0,1]),
    df['Tea Towel-Second Response [Change from Neutral]'].replace(['Yes', 'No'], [2,0]),
    df['Tea Towel-Second Response [Turns head]'].replace(['Yes', 'No'], [3,0]),
    df['Tea Towel-Second Response [Attempts to/Removes towel by moving]'].replace(['Yes', 'No'], [4,0]),
    df['Tea Towel-Second Response [Attempts to/Removes towel with mouth]'].replace(['Yes', 'No'], [5,0]),
    df['Tea Towel-Second Response [Plays]'].replace(['Yes', 'No'], [6,0])])
    df['S-Tea Towel-Second Response' ] = df_towel.mean(axis = 0)

    # distractions -> add dog distraction?
    df = df.join(feature_extraction('S-Distractions-First Response', 
        df[['Distractions-First Response [Teddy]', 'Distractions-First Response [Human]',
            'Distractions-First Response [Car]', 'Distractions-First Response [Food]']]))
    df = df.join(feature_extraction('S-Distractions-Second Response', 
        df[['Distractions-Second Response [Teddy]', 'Distractions-Second Response [Human]',
            'Distractions-Second Response [Car]','Distractions-Second Response [Food]']]))

    # df['S-Distractions-Difference_mean'] = df['S-Distractions-Second Response_mean'] - df['S-Distractions-First Response_mean']
    # df['S-Distractions-Difference_prod'] = df['S-Distractions-Second Response_prod'] - df['S-Distractions-First Response_prod']
    
    df_distractions = pd.DataFrame({
    'Teddy' : df['Distractions-Second Response [Teddy]'] - df['Distractions-First Response [Teddy]'],
    'Human' : df['Distractions-Second Response [Human]'] - df['Distractions-First Response [Human]'],
    'Car' : df['Distractions-Second Response [Car]'] - df['Distractions-First Response [Car]'],
    'Food': df['Distractions-Second Response [Food]'] - df['Distractions-First Response [Food]']})
    df['S-Distractions-Difference_mean'] = df_distractions.mean(axis = 1)
    
    # kong
    df = df.join(feature_extraction('S-Kong-Response',
        df[['Kong-Presentation-Response','Kong-Interaction-Response to stimulus',
        'Kong-Interaction-Back','Kong-Return-Handler']]))

    # dog
    df = df.join(feature_extraction('S-Dog-Distraction',
            df[['Dog-Response', 'Dog-Call Back Response']]))    
    
    # call back (after familiarisation, after dog)
    df = df.join(feature_extraction('S-Call-Response', 
            df[['Call Back-Response', 'Dog-Call Back Response']]))
    df['S-Familiarisation-Dog-Call'] = df['Call Back-Response'] - df['Dog-Call Back Response']   # calculate difference


    # crate
    df = df.join(feature_extraction('S-Crate-Response', 
            df[['Crate-Entering', 'Crate-Self-Modulation', 
                'Crate-Stress']].join(abs(df['Crate-Behaviours [Settled]']-5)))) # settled reverse
    df = df.join(feature_extraction('S-Crate-Stimulus', 
            df[['Crate-Behaviours [Sniffing/Exploring ]','Crate-Behaviours [Digging]',
                'Crate-Behaviours [Nudging Crate]', 'Crate-Behaviours [Pawing]']]))
    df = df.join(feature_extraction('S-Crate-Handler', 
            df[['Crate-Behaviours [Actively Seeking Attention]', 
            'Crate-Behaviours [Whining]', 'Crate-Behaviours [Barking]']]))

    # petting
    df = df.join(feature_extraction('S-Petting-Stimulus-During', 
            df[['Petting-Handler-Stimulus', 'Petting-Confidence-During']]))
    df = df.join(feature_extraction('S-Petting-Engagement-During',
            df[['Petting-Handler-Holding dog', 'Petting-Confidence-During']]))
    df = df.join(feature_extraction('S-Petting-After',
            df[['Petting-Handler-Holding dog', 'Petting-Responsiveness-After']]))

    # isolation
    df = df.join(feature_extraction( 'S-Isolation-Handler',
        df[['Isolation-Response [Time oriented]', 
            'Isolation-Response [Whining]', 
            'Isolation-Response [Barking]']]))

    df['S-Isolation-Stimulus'] = df['Isolation-Response [Exploration]'] - df['Isolation-Response [Unsettled/Pacing]']

    # sociability/ friendliness
    df = df.join(feature_extraction('S-Sociability', 
        df[['Petting-Confidence-During', 
        'Petting-Responsiveness-After', 'Reunion-Response']]))

    print("Shape after feature engineering", df.shape)
    return(df)

################################    Main Start     ################################
    
# importing dogs information
df_dogs = import_dogs(dir_raw)
# importing data collection summary information
df_summary = import_summary(dir_raw)


# importing and processing ethogram dataframe
df_ethogram = import_ethogram(dir_raw)
df_ethogram = categories2numbers(df_ethogram)
df_ethogram = feature_engineering(df_ethogram)

# merging ETHOGRAM and DOGS dataframes
df = pd.merge(df_dogs, df_ethogram,  right_on  = 'Dog code', left_on = 'Code', how = 'right')
# drop column Dog code because it is the same as Code
df.drop(columns = 'Dog code', inplace = True)

# merging ETHOGRAM and SUMMARY dataframes
df = pd.merge(df, df_summary, left_on = ["Code", "Data Collection Number"], 
                right_on = ["Code", "DC"], how = 'left')
# drop these columns because the corrected/revised data comes from summary
df.drop(columns = ["Data Collection Date", "Video Start Time (HH:MM:SS)"], inplace = True)

# changing the order of the columns, removing Timestamp as it does not matter
df = df[['Name','Code','Data Collection Number', 'BT Date', 'Assessor', 
    'Breed', 'Sex', 'Litter', 'Source', 'DOB', 'DOA', 'End Date', 'Duration',
    'Status', 'Outcome', 'Working', 'BT Start', 'BT Duration'] + df.columns.to_list()[16:-3]]
# rename BT Date to Data Collection Date
df.rename(columns = {"BT Date" :"Data Collection Date" }, inplace = True)

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


#save to csv file
df.to_csv('{}\\{}_Ethogram-Trainers.csv'.format(dir_pro, date) , index = False)


################################      Main End       ################################


#############################      Troubleshooting       ################################

# # check the time difference between trainers ethogram and data collection summary
# dt_ethogram = pd.to_datetime(df['Data Collection Date'] + ' ' + df['Video Start Time (HH:MM:SS)'], infer_datetime_format=True, dayfirst = True, yearfirst = False)
# dt_summary = pd.to_datetime(df['BT Date'] + df['BT Start'], format="%d/%m/%Y%H:%M:%S")
# dts = pd.DataFrame({'ethogram': dt_ethogram,
#                     'summary': dt_summary})
# dts['difference'] = dts.summary - dts.ethogram
# dts.sort_values("summary")

### print missing data
# importing the data tab as a dataset to make sure that I found all the ethograms
# data = pd.read_csv("{}\\Data Collection - Data.csv".format(dir_raw), skiprows = 1)
# print('Dogs listed as having an ethogram, but no ethogram was found')
# print('DC1:', list(set(data.loc[data['Trainer-Ethogram'] =='Done', 'Code'].values) - set(df_ethogram.loc[df_ethogram['Data Collection Number'] == 1,'Dog code'].unique())))
# print('DC2:', list(set(data.loc[data['Trainer-Ethogram.1'] =='Done', 'Code'].values) - set(df_ethogram.loc[df_ethogram['Data Collection Number'] == 2,'Dog code'].unique())))
# len(data.loc[data['Trainer-Ethogram.1'].str.contains('Done', na = False), 'Code'])
# len(df_ethogram.loc[df_ethogram['Data Collection Number'] == 2,'Dog code'].unique())

