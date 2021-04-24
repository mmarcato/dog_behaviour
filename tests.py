################################     Duplicates       ################################
import pandas as pd
my_dir = 'C:\\Users\\marinara.marcato\\Project\\Scripts\\dog_ethogram\\dfs'

def duplicates_to_csv (r_name, subset, p_name, df_dir = my_dir):
    '''
        description:
            imports dataframe r_name in df_dir   
            creates new dataframe with duplicates based on subsets
            saves that dataframe as p_name in df_dir
        variables:
            r_name = string raw dataframe file name
            subset = list, subset to find duplicates
            p_name = string, processed resulting dataframe file name
            df_dir = string, path to directory where dataframes are   
    '''
    df = pd.read_csv('{}\\{}.csv'.format(df_dir, r_name))
    # create and sort dataframe containing only duplicates considering the given subset
    df = df.loc[df.duplicated(subset = subset, keep = False)]
    df.sort_values(subset, inplace = True)
    # saves dataframe considering the given name and directory 
    df.to_csv('{}\\{}.csv'.format(df_dir, p_name), index = False)

duplicates_to_csv(r_name = '21-03-11_Ethogram-Trainers', 
                subset = ['Code', 'Data Collection Number', 'Assessor'], 
                p_name = '21-03-11_Ethogram-Trainers_Intra-Rater') 

duplicates_to_csv(r_name = '21-03-11_Ethogram-Trainers', 
                subset = ['Code', 'Data Collection Number'], 
                p_name = '21-03-11_Ethogram-Trainers_Inter-Rater')

duplicates_to_csv(r_name = '21-03-10_Ethogram-Researchers', 
                subset = ['Code', 'Data Collection Number', 'Assessor'], 
                p_name = '21-03-11_Ethogram-Researchers_Intra-Rater') 

duplicates_to_csv(r_name = '21-03-10_Ethogram-Researchers', 
                subset = ['Code', 'Data Collection Number'], 
                p_name = '21-03-11_Ethogram-Researchers_Inter-Rater')

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