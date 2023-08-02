# WS - Dog Ethograms
This file explains the structure of this folder and outlines the content and source of each file as appropriate.

- Researchers: Files for data analysis and results taking the researchers ethogram into account.
- Trainers: Files for data analysis and results taking the trainers ethogram into account.


## Folders
### Data
Folder 0_data
- 0_data/0_raw: Files can be downloaded from Google Drive and updated in the folder. Files with a date are processed raw dataset, generated by running 'main.py'.
    - 'Data Collection - Dogs.csv': download [Data Collection>Dogs tab](https://docs.google.com/spreadsheets/d/1MwhWauU9U89bbZK-eoz1BFMO7p3cIqMnTTXPB2WkL3o/edit#gid=993745027) as a .csv file. 

    - 'Ethogram - Trainers.csv': download [Ethogram - Trainers (Responses)](https://docs.google.com/spreadsheets/d/1IUK12D-nC8imw1Y_BZKgA1dA6QIRN2WNogR6R3bwN_E/edit#gid=872369725) tab 'Manually Processed' as a csv file and rename it. Main processing done:
    Replace start and finish times using regex find (\d)[.](\d) -> replace with $1:$2.

    - 'Ethogram - Researchers.csv': download [Ethogram - Researchers (Responses)](https://docs.google.com/spreadsheets/d/1bcR8bqIKm2PmWiVrwY-AphL5xfJllIdnVQwonuXwcpg/edit#gid=1480887842) form responses as a csv file and rename it. 

- 0_data/1_process: 
    - 'YY-MM-DD_Ethogram-Trainers.csv': Processed version of the 'Ethogram - Researchers.csv'. Duplicates: Check whether no missing data and give preference to keep the last occurence as we were changing the form.

- 0_data/2_prepare:     
        - *Intra-rater realibility:* Same video and assessor.
        - *Inter-rater realibility:* Same video different assessors.

    - 'YY-MM-DD_Ethogram-Researchers.csv'. Processed version of the 'Ethogram - Researchers.csv'. Duplicates: Check whether no missing data and give preference to keep the last occurence as we were changing the form.    
        - *Intra-rater realibility:* Same video and assessor.
        - *Inter-rater realibility:* Same video different assessors.

### Process
Folder 1_process: works with datasets in folder '0_data/0_raw', namely: 
    - demographics.py
    - timestamps.py: 
    - researchers.py:
        - Imports 'Data Collection - Dogs.csv' and 'Ethogram - Researchers'
        - Functions: combines two dataset and assigns numbers to categorical variables in ethogram.
        - Exports 'YY-MM-DD_Ethogram-Researchers.csv' to '0_data/1_process'

    - trainers.py: works with datasets in folder '0_data/0_raw', namely: 
        - Imports 'Data Collection - Dogs.csv' and 'Ethogram - Trainers'
        - Functions: combines two dataset and assigns numbers to categorical variables in ethogram.
        - Exports 'YY-MM-DD_Ethogram-Trainers.csv' to '0_data/1_process'


### Results
Data analysis results for working success prediction.
