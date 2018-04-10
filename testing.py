import requests
#import numpy as np
#import json
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_pandas import Spread
#import calendar
import datetime as dt
# import xlsxwriter
#import csv
# import timing
#from io import StringIO
#import schedule
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
gsheet = client.open("clan").sheet1

# Download content and create DataFrame
rawDF = pd.DataFrame(gsheet.get_all_records())

rawDF['date']=rawDF['date'].apply(lambda x:
                                        dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
maxDF = rawDF.set_index('date').between_time('00:00:00', '18:44:00').reset_index()
maxDF['DayofYear'] = maxDF['date'].dt.dayofyear
highestDonationOfTheDay = maxDF.groupby(['DayofYear', 'name']).max()
# highestDonationOfTheDay.to_csv('test2.csv')

print('0')
highestDonationOfTheDay['donations_shifted'] = rawDF.groupby(['name'])['donations'].shift(1)
print('1')
highestDonationOfTheDay=highestDonationOfTheDay.fillna(value=0) # .loc[rawDF['name']=='Skoy']
print('2')
highestDonationOfTheDay['dailyDonationPerc'] = ( highestDonationOfTheDay['donations']-highestDonationOfTheDay['donations_shifted']) / 260 * 100
print('3')
highestDonationOfTheDay['dailyDonation'] = ( highestDonationOfTheDay['donations']-highestDonationOfTheDay['donations_shifted'])
print('4')
highestDonationOfTheDay['dailyDonationPerc'][highestDonationOfTheDay['dailyDonationPerc']<0]=0
print('5')
highestDonationOfTheDay['dailyDonation'][highestDonationOfTheDay['dailyDonation']<0]=0
print('6')
highestDonationOfTheDay['dailyDonationPerc'][highestDonationOfTheDay['dailyDonationPerc']>100]=100
print('7')
highestDonationOfTheDay['dailyDonation'][highestDonationOfTheDay['dailyDonation']>260]=260
# print(rawDF.sort_values(by=['name', 'date']))
# print (rawDF.shape)
# csvDF=pd.DataFrame.to_csv(highestDonationOfTheDay,path_or_buf='csvtoplotly.csv')
spread = Spread('skoy87@clannopalmoil.iam.gserviceaccount.com', 'clan')
spread.df_to_sheet(highestDonationOfTheDay, index=True, sheet='donations', start='A1', replace=True)