import requests
import numpy as np
import json
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import calendar
import datetime
# import xlsxwriter
import csv
# import timing
from io import StringIO
pd.options.display.width=None
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

gsheet = client.open("clan").sheet1
rawDF = pd.DataFrame(gsheet.get_all_records())
#print(rawDF)

rawDF['donations_shifted'] = rawDF.groupby(['name'])['donations'].shift(1)

rawDF=rawDF.fillna(value=0) # .loc[rawDF['name']=='Skoy']
# noNa=rawDF.fillna(value=0)
#print (rawDF.shape)
rawDF['dailyDonationPerc'] = ( rawDF['donations']-rawDF['donations_shifted']) / 260 * 100
rawDF['dailyDonation'] = ( rawDF['donations']-rawDF['donations_shifted'])
rawDF['dailyDonationPerc'][rawDF['dailyDonationPerc']<0]=0
rawDF['dailyDonation'][rawDF['dailyDonation']<0]=0
rawDF['dailyDonationPerc'][rawDF['dailyDonationPerc']>100]=100
rawDF['dailyDonation'][rawDF['dailyDonation']>260]=260
# print(rawDF.sort_values(by=['name', 'date']))
#print (rawDF.shape)
csvDF=pd.DataFrame.to_csv(rawDF,path_or_buf='csvtoplotly.csv')
