import numpy as np
import pandas as pd
import datetime as dt

# CONVERTERS
# con_appsco = {'Number1':f,'Number2':f, 'Number3':f}



# CSV to DATAFRAME
df_lead16 = pd.read_csv('original_files/LeadtoApp2016.csv',parse_dates=[2,5])
df_lead17 = pd.read_csv('original_files/LeadtoApp2017.csv',parse_dates=[2,5])
df_immapp = pd.read_csv('original_files/ImmersiveApplicants.csv',parse_dates=[0,6,7,8,9,10])
df_notenr = pd.read_csv('original_files/NotEnrolled.csv', encoding = "ISO-8859-1" )
df_enroll = pd.read_csv('original_files/EnrolledAllTIme.csv', encoding = "ISO-8859-1")
df_appsco = pd.read_csv('original_files/ApplicantsWithScorecard.csv',parse_dates=[0,1])
df_int1 = pd.read_csv('original_files/Interview1Date.csv',parse_dates=[1])
df_int1 = df_int1.drop(columns='id').rename(columns={'day of created date':'interview1'})
df_int2 = pd.read_csv('original_files/DayofInterview2.csv',parse_dates=[1])
df_int2 = df_int2.drop(columns='id').rename(columns={'day of created date':'interview2'})

# maybe add to other column
df_appsco['AppToStart'] = df_appsco['Course Start Date'] - df_appsco['Created Date']


# Combine 2016 & 2017 data
df_leads = pd.concat([df_lead16,df_lead17])
# combine boulders into one
df_leads['campus'] = df_leads['campus'].replace(['Boulder-Walnut Street','Boulder-West Pearl'], "Boulder")
# If there are duplicates, keep the most recent row
df_leads.drop_duplicates(subset=['leademail'],keep='last',inplace = True)
# We only care about the 2 main products, so remove the rest
df_leads = df_leads[df_leads['product'].isin(['Full Stack','Data Science'])]
# Remove Fort Collins
df_leads = df_leads[~df_leads['campus'].isin(['Fort Collins-Old Town'])]
# We need to identify direct app by leads that applied on the same day as lead created
df_leads['direct_app'] = (df_leads['day of lead created date'] == df_leads['application created date'])*1 #if matched, then direct apps
# Remove 'galvanize' or 'test' c
df_leads = df_leads[~df_leads['leademail'].str.contains('test|galvanize')]
# If application day is after course start, remove
df_immapp = df_immapp[df_immapp['day of course start date c'] > df_immapp['day of application created date']]
# Don't use 2018 after Jan 10
df_immapp = df_immapp[df_immapp['day of course start date c'] < '2018-01-10']
# If there are duplicates, keep the most recent row
df_immapp.drop_duplicates(subset=['student email c'],keep='last',inplace = True)
df_int1.drop_duplicates(subset=['student email c'],keep='last',inplace = True)
df_int2.drop_duplicates(subset=['student email c'],keep='last',inplace = True)
df_immapp = pd.merge(df_immapp,df_int1,how='left',left_on='student email c',right_on='student email c')
df_immapp = pd.merge(df_immapp,df_int2,how='left',left_on='student email c',right_on='student email c')

# Left join on common key email
df_combined = pd.merge(df_leads,df_immapp,how='left',left_on='leademail',right_on='student email c')
# Only care about 2016 & 2017
df_combined = df_combined[df_combined['day of lead created date'].dt.year.isin([2016,2017])]




# Create new variables for days for each segment, as defined below
df_combined['days_until_start'] = (df_combined['day of course start date c'] - df_combined['day of application created date']).dt.days
df_combined['take_sent_to_start'] = (df_combined['day of course start date c'] - df_combined['day of sent takehome on c']).dt.days
df_combined['take_to_start'] = (df_combined['day of course start date c'] - df_combined['day of date take home returned c']).dt.days
df_combined['interview1'] = (df_combined['day of course start date c'] - df_combined['interview1']).dt.days
df_combined['interview2'] = (df_combined['day of course start date c'] - df_combined['interview2']).dt.days
df_combined['enroll_to_start'] = (df_combined['day of course start date c'] - df_combined['day of accepted date c']).dt.days
df_combined['lead_to_app_days'] = (df_combined['day of application created date'] - df_combined['day of lead created date']).dt.days
df_combined['app_to_take_days'] = (df_combined['day of date take home returned c'] - df_combined['day of application created date']).dt.days
df_combined['take_to_enr_days'] = (df_combined['day of accepted date c'] - df_combined['day of date take home returned c']).dt.days



df_combined.to_pickle('new_files/test.pkl')
# df_combined.to_csv('new_files/combined_applicants.csv')




if __name__ == '__main__':
    print("Check if join doesn't create more rows")
    print(df_leads.shape)
    print(df_combined.shape)
    pass
