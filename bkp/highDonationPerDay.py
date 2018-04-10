import requests
import numpy as np
from scipy.ndimage.filters import maximum_filter1d
import json
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_pandas import Spread
import calendar
import datetime as dt
# import xlsxwriter
import csv
import timing
from io import StringIO
import schedule
pd.set_option('display.max_rows', 1000)

# Visualisation and time settings
ts = time.gmtime()
orario = time.strftime("%Y-%m-%d %H:%M:%S", ts)
pd.options.display.width=None


# Authentication and open csv from google sheets
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
gsheet = client.open("clan").sheet1

# Download content and create DataFrame
originalDF = pd.DataFrame(gsheet.get_all_records())

originalDF['date']=originalDF['date'].apply(lambda x:
                                            dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

originalDF['DayofYear']=originalDF['date'].dt.dayofyear
#highestDonationByTheDay=originalDF.groupby(['DayofYear', 'name'])
#originalDF['totalDonationOfTheDay'] = maximum_filter1d(highestDonationByTheDay.High, size=3, origin=1, mode='nearest')
print (originalDF)


highestDonationByTheDay=originalDF.groupby(['DayofYear', 'name']).max()
print (highestDonationByTheDay)
highestDonationByTheDay.to_csv(path_or_buf='donations.csv')
spreadDon = Spread('skoy87@clannopalmoil.iam.gserviceaccount.com', 'clan')
spreadDon.df_to_sheet(highestDonationByTheDay, index=True, sheet='donations', start='A1', replace=True)


