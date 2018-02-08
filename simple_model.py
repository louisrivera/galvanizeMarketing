import numpy as np
import pandas as pd

df = pd.read_pickle('new_files/test.pkl')

# remove if enroll_to_start is negative for now
df = df[(df['enroll_to_start']>-1) | (df['enroll_to_start'].isnull())]
df = df[~df.campus.isnull()]
df = df[(df['take_sent_to_start']>-1) | (df['take_sent_to_start'].isnull())]
df = df[(df['take_to_start']>-1) | (df['take_to_start'].isnull())]
df = df[(df['days_until_start']>-1) | (df['days_until_start'].isnull())]
df = df[(df['lead_to_app_days']>-1)| (df['lead_to_app_days'].isnull())]
df = df[(df['app_to_take_days']>-1)| (df['app_to_take_days'].isnull())]
df = df[(df['take_to_enr_days']>-1)| (df['take_to_enr_days'].isnull())]

df_apps = pd.DataFrame(df[pd.notnull(df['day of application created date'])])

# temporary
# df_apps = df.dropna(subset=['application created date','day of application created date'], how='any')


df_comavg = df_apps.groupby(['campus','product']).mean(numeric_only=False)
df_commed = df_apps.groupby(['campus','product']).median(numeric_only=False)
df_comcnt = df_apps.groupby(['campus','product']).count()
# (df['days_until_start']//np.timedelta64(1,'W')).astype(int)

def stage(row,weeks):
    """
    Return's stage that each row currently based on weeks until start date
    ex) stage(col,25) --> 'App'
    """
    if row['days_until_start'] < (weeks*7):
        return  "Not Applied"
    elif row['enroll_to_start'] >= (weeks*7):
        return  "Enrolled"
    elif np.isnan(row['take_sent_to_start']):
        return  "Closed"
    elif row['take_sent_to_start'] < (weeks*7):
        return  "Applied"
    elif np.isnan(row['take_to_start']):
        return  "Closed"
    elif row['take_to_start'] < (weeks*7):
        return  "Takehome"
    elif np.isnan(row['interview1']) and row['enroll_to_start'] > 0:
        return  "Applied"
    elif row['interview1'] < (weeks*7):
        return 'interview1'
    elif np.isnan(row['interview2']) and row['enroll_to_start'] > 0:
        return  "Closed"
    elif row['interview2'] < (weeks*7):
        return 'interview2'
    elif np.isnan(row['enroll_to_start']):
        return  "Closed"
    elif row['interview2'] > (weeks*7): #adding this for the undertermined time
        return 'interview2'
    return 'Applied'

    # if row['days_until_start'] > (weeks*7):
    #     return 'NA'
    # elif (row['days_until_start'] < (weeks*7)) & (row['take_sent_to_start'] > (weeks*7)):
    #     if row['direct_app'] == 1:
    #         return 'direct'
    #     else:
    #         return 'lead'
    # elif (row['take_sent_to_start'] < (weeks*7)) & (row['take_to_start'] > (weeks*7)):
    #     return 'take_home_sent'
    # elif row['take_to_start'] > (weeks*7):
    #     return 'take_home_returned'
    # elif row['enroll_to_start'] > (weeks*7):
    #     return 'enrolled'
    # else:
    #     return 'closed'


    # df_apps['wk{}_status'.format(weeks)] = 'closed'
    # df_apps.loc[(df_apps['days_until_start'] > weeks*7) & (df_apps['direct_app'] == 1),'wk{}_status'.format(weeks)] = 'direct'
    # df_apps.loc[(df_apps['days_until_start'] > weeks*7) & (df_apps['direct_app'] == 0),'wk{}_status'.format(weeks)] = 'lead'
    # df_apps.loc[(df_apps['take_to_start'] > weeks*7) & (df_apps['days_until_start'] < weeks*7),'wk{}_status'.format(weeks)] = 'take_home'
    # df_apps.loc[(df_apps['days_until_start'] > weeks*7) & (df_apps['direct_app'] == 1),'wk{}_status'.format(weeks)] = 'enrolled'

for i in range(25,-1,-1):
    df_apps['wk{}_status'.format(i)] = (df_apps.apply(lambda row: stage(row,i),axis=1))


# df_apps[df_apps['days_until_start'] > 35]
df_apps.to_csv('new_files/simple_model.csv') #check
df_apps.to_pickle('new_files/simple_model.pkl')


if __name__ == '__main__':
    # print(df.head())
    # print(df_comavg.head())
    # print('-------------------')
    # print(df_comcnt.head())
    pass
