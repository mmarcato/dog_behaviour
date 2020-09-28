import pandas as pd
my_dir = "C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\dfs"
df = pd.read_csv('%s\\21-03-10_Ethogram-Trainers.csv' % my_dir)

################################     Duplicates       ################################
# define a subset to find duplicate combinations of Dog, Data Collection and Assessor
subset = ['Dog code', 'Data Collection Number', 'Assessor']
# print the duplicates considering the subsets
print(df[df.duplicated(subset = subset)].loc[:,subset].drop_duplicates().values)
# drop duplicates considering the subset while keeping the last occurence
df.drop_duplicates(subset = subset,\
    keep = 'last', inplace = True, ignore_index = True)

################################     Data Types       ################################
# visualise columns per data type
# Im not sure why similar variables are classified differently, maybe because of NAs?
# Start and Finish times are objects
pd.set_option('display.max_colwidth', 0)
d = df.columns.to_series().groupby(df.dtypes).groups
print(pd.DataFrame({'Type': d.keys(), 'Variables': d.values()} ))


#### new import_summary for 'Data Collection - Summary.csv' for when I need it =)
def import_summary(base_dir):
    df = pd.read_csv("{}\\Data Collection - Summary.csv".format(base_dir), header = [0,1], \
        true_values= ['Done'], false_values=['Missing'] )
        
    #print(df.columns)
    a = df.columns.get_level_values(0)
    b = df.columns.get_level_values(1)

    df.columns = [a.to_series().mask(lambda x: x.str.contains('Unnamed')).ffill(), b]
    df.rename(columns = {'Data Collection 1' : 'DC1', \
                            'Data Collection 2' : 'DC2', \
                                'Questionnaire':'Quest' }, inplace = True)
    #print(df.columns)
    
    df.set_index([('Info','Name')], inplace = True, drop = False)
    return(df)


## old version of import_summary using read_excel, not working anymore because of some package version 
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