import pandas as pd
import re
import datetime as dt
import numpy as np

my_dir = "C:\\Users\\marinara.marcato\\Data"

def import_ethogram(base_dir):
    df = pd.read_csv(("%s\\Ethogram\\20-02-17_Ethogram-Researchers-FormResponses.csv" % base_dir), parse_dates = ['Timestamp', 'Data Collection Date'])
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

df_summary = import_summary(my_dir)
df_training = import_training(my_dir)   
df_ethogram = import_ethogram(my_dir)

# adding stuff to df_ethogram

# creating a dictionary with key = Code and value = Name
map_name = dict(df_summary['Info'][['Code', 'Name']].values)
map_sex = dict(df_summary['Info'][['Code', 'Sex']].values)
# mapping the dictionary with the column 'Code' to create column 'Name
df_ethogram['Name'] = df_ethogram['Dog code'].map(map_name)
df_ethogram['Sex'] = df_ethogram['Dog code'].map(map_sex)
df_ethogram['Litter'] = df_ethogram['Name'].str[:1]
# creating a dictionary with key = Name and value = Status
map_status = pd.Series(df_training['Training Outcome']['Status'].values, index=df_training['Info']['Name']).to_dict()
df_ethogram['Status'] = df_ethogram['Name'].map(map_status)
df_ethogram.set_index(['Name'], inplace = True)

# changing the order of the columns
cols = df_ethogram.columns.tolist()
cols = cols[:2] + cols[-5:] + cols[2:-5]
df_ethogram = df_ethogram[cols]

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
                    ts = re.findall("\d\d:\d\d", time)
                    #print(ts)
                    d = d + dt.datetime.strptime(ts[1], "%M:%S") - dt.datetime.strptime(ts[0], "%M:%S")
                    print(d)
                else:
                    d = d + dt.timedelta(0,1)
            return(d.total_seconds())

        if method == 'count':
            c = len(times.split(";"))
            return(c)

# short_vocalization = number of short bark events
df_ethogram['Short Barks Count'] = df_ethogram['Short Barks'].apply(lambda x: process(x, 'count'))

# cont_vocalization = number of continuous bark events
df_ethogram['Continuous Barks Duration'] = df_ethogram['Continuous Barks'].apply(lambda x: process(x, 'duration'))
df_ethogram['Continuous Barks Count'] = df_ethogram['Continuous Barks'].apply(lambda x: process(x, 'count'))

# no_winning = number of winning events
df_ethogram['Whines Duration'] = df_ethogram['Whines'].apply(lambda x: process(x, 'duration'))
df_ethogram['Whines Count'] = df_ethogram['Whines'].apply(lambda x: process(x, 'count'))

df_ethogram['Shakes Count']  = df_ethogram['Shakes'].apply(lambda x: process(x, 'count'))

df_ethogram['Jumps Count']  = df_ethogram['Jumps'].apply(lambda x: process(x, 'count'))

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
 'Crate-Behaviours [Sniffing/Exploring ]',
 'Crate-Behaviours [Attention Seeking]',
 'Crate-Behaviours [Digging]',
 'Crate-Behaviours [Licking/Mouthing]',
 'Crate-Behaviours [Whining]',
 'Crate-Behaviours [Barking]',
 'Isolation-Response [Time oriented]',
 'Isolation-Response [Exploration]',
 'Isolation-Response [Unsettled/Locomotion]',
 'Isolation-Response [Whining]',
 'Isolation-Response [Barking]',
 ]
 
for col in cols:
    df_ethogram[col] = df_ethogram[col].str[:1]

for col in cols:
    print(df_ethogram[col].head(5))

#need to number encode Crate-Response, Walking-Distractibility
vars_crate = {'Relaxed/Indifferent':1,
 'Uneasy but cooperative':2,
 'Anxious':3 ,
 'Extremely Anxious': 4}
vars_walk_dist = {'Hardly distracted':1,'Somewhat distracted':2,  'Mostly distracted':3}

df_ethogram['Crate-Response'] = df_ethogram['Crate-Response'].map(vars_crate)
df_ethogram['Walking-Distractibility'] = df_ethogram['Walking-Distractibility'].map(vars_walk_dist)

for (dog, date) in df_ethogram[df_ethogram.duplicated(subset = ['Dog code', 'Data Collection Date'])].loc[:,('Dog code', 'Data Collection Date')].drop_duplicates().values:
    print(df_ethogram[(df_ethogram['Dog code'] == dog) & \
        (df_ethogram['Data Collection Date'] == date)].mean())

df_ethogram.groupby(['Dog code', 'Data Collection Number']).mean()

cols = df_ethogram.columns
#save to csv file
df_ethogram.to_csv('E:\\Study\\Ethogram\\20-02-17_Ethogram.csv')

