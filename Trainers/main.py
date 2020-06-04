import pandas as pd
import re
import datetime as dt
import numpy as np

my_dir = "C:\\Users\\marinara.marcato\\Data\\Ethogram\\Trainers"


def import_ethogram(base_dir):
    df = pd.read_csv(("%s\\20-06-03_Ethogram-Trainers-FormResponses.csv" % base_dir), parse_dates = ['Timestamp', 'Data Collection Date'])
    return df

def import_summary(base_dir):
    dfs = pd.read_excel('%s\\Data Collection.xlsx' % base_dir, header = [0,1], sheet_name= ['Summary', 'Data', 'Measurements', 'Training'])
    for key in list(dfs.keys()):
        dfs.get(key).set_index([('Info','Name')], inplace = True, drop = False)
        dfs.get(key).loc[: , ('Info', 'Intake')].fillna(method = 'ffill', inplace = True)
        dfs.get(key).rename(columns = {'Data Collection 1' : 'DC1', 'Data Collection 2' : 'DC2' }, inplace = True)
    
    
    # return Measurements 
    return pd.concat({'Info': dfs['Summary']['Info'],
                'DC1': dfs['Summary']['DC1'].join(dfs['Data']['DC1'].drop(['Date'], axis = 1)),
                'DC2': dfs['Summary']['DC2'].join(dfs['Data']['DC2'].drop(['Date'], axis = 1)),
                'Quest':dfs['Summary']['Questionnaire']},
                 axis = 1 )

def import_training(base_dir):
    df = pd.read_excel('%s\\Data Collection.xlsx' % base_dir, header = [0,1], sheet_name= ['Training'])
    return df['Training']

def add_info(df, df_training, df_summary):
    # adding information from df_training and df_summary to df_ethogram

    # creating a dictionary with key = Code and value = Name
    map_name = dict(df_summary['Info'][['Code', 'Name']].values)
    map_sex = dict(df_summary['Info'][['Code', 'Sex']].values)
    # mapping the dictionary with the column 'Code' to create column 'Name
    df['Name'] = df['Dog code'].map(map_name)
    df['Sex'] = df['Dog code'].map(map_sex)
    df['Litter'] = df['Name'].str[:1]
    # creating a dictionary with key = Name and value = Status
    map_status = pd.Series(df_training['Training Outcome']['Status'].values, index=df_training['Info']['Name']).to_dict()
    df['Status'] = df['Name'].map(map_status)
    df.set_index(['Name'], inplace = True)

    # changing the order of the columns
    cols = df.columns.tolist()
    cols = cols[:2] + cols[-5:] + cols[2:-5]
    df = df[cols]
    return df

def process(times, method):
    if times in ['NA', 'Na', 'na', 'n/a', 'n\a', 'NaN', np.nan, 'nan']:
        return(None)
    else:
        if method == 'duration':    
            d = dt.timedelta(0,0)
            print(times)
            for time in times.split(";"):
                #print(time)
                if "-" in time:
                    ts = re.findall('\d\d:\d\d', time)
                    #print(ts)
                    d = d + dt.datetime.strptime(ts[1], "%M:%S") - dt.datetime.strptime(ts[0], "%M:%S")
                    print(d)
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
    'Crate-Behaviours [Whining]',
    'Crate-Behaviours [Barking]',
    'Crate-Behaviours [Pawing]',
    'Crate-Behaviours [Nudging Crate]',
    'Crate-Stress',
    'Crate-Self-Modulation',
    'Petting-Handler-Stimulus',
    'Petting-Handler-Holding dog',
    'Petting-Confidence - During',
    'Petting-Responsiveness - After',
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

    for col in cols:
        print(df[col].head(5))
    return(df)

def categories2numbers_mapping(df):
    #need to number encode Crate-Response, Walking-Distractibility, Petting-Holding dog
    vars_crate = {'Relaxed/Indifferent':1,
    'Uneasy but cooperative':2,
    'Anxious':3 ,
    'Extremely Anxious': 4}
    vars_walking = {'Hardly distracted':1,'Somewhat distracted':2,  'Mostly distracted':3}
    vars_petting = {'Never' :1, 'Sometimes':2, 'Always': 3}

    df['Crate-Response'] = df['Crate-Response'].map(vars_crate)
    df['Walking-Distractibility'] = df['Walking-Distractibility'].map(vars_walking)
    df['Petting-Holding dog'] =df['Petting-Holding dog'].map(vars_petting)
    return(df)

# importing dataframes
df_summary = import_summary(my_dir)
df_training = import_training(my_dir)   
df_ethogram = import_ethogram(my_dir)

# processing dataframes
df_ethogram = add_info(df_ethogram, df_training, df_summary)
df_ethogram = categories2numbers(df_ethogram)

# subsetting columns accounding to text pattern
# cols = [s for s in df_ethogram.columns if "Time (MM:SS)" in s]
# this is how we can identify duplicate rows
#for (dog, date) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Date'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
#    print(df_ethogram[(df_ethogram['Dog code'] == dog) & \
#        (df_ethogram['Data Collection Date'] == date)].mean())
#
# this is how we can take a mean of the duplicate rows
# df_ethogram.groupby(['Dog code', 'Data Collection Number']).mean()


#save to csv file
df_ethogram.to_csv('%s\\20-06-04_Ethogram.csv' % my_dir )


