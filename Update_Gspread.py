import requests
import numpy as np
import json
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_pandas import Spread
import calendar
import datetime
# import xlsxwriter
import csv
# import timing
from io import StringIO

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



myKey='b0cab65a56f141d28fb04a4ee29aa8f10230573afbb149f3a6bbf160a68de0a7'
clanTag = '2GRV8JVY'
lindx = ['tag', 'name', 'trophies', 'donations', 'donationsReceived', 'donationsDelta']
members = ['members']

# Update stats
def getClanJson(myKey,clanTag):
    headers = {'auth': myKey}
    urlclan='https://api.royaleapi.com/clan/'+clanTag
    responseclan  = requests.request('GET', urlclan, headers=headers)
    dataclanJson=responseclan.json()
    return dataclanJson


def getDFfromJson(d):
    newDf = pd.DataFrame()
    lindx = ['name','tag', 'trophies', 'donations', 'donationsReceived', 'donationsDelta', 'clan', 'members']
    for k,v in d.items():
        if isinstance(v, dict):
            getDFfromJson(v)
            if k in lindx :
                newdf2 = pd.DataFrame(v)
                newDf = newDf.append(newdf2, ignore_index=True)
        else:
            if k in lindx :
                newDf = newDf.append({k : v}, ignore_index=True)
    return newDf


def getValues(newDf, members):
    validvalues = []
    for i in members:
        firstValid = newDf[i][newDf[i].first_valid_index()]
        validvalues.append(firstValid)
    return validvalues


def getPlayersStatList(playersStatList):
    seriesList = []
    for i in playersStatList:
        playerMatrix = getDFfromJson(i)
        playerSeries = getValues(playerMatrix, lindx )
        seriesList.append(playerSeries)
    #print (seriesList)
    playersDF = pd.DataFrame.from_dict(seriesList)
    playersDF.columns=lindx
    playersDF['date']= orario
    return playersDF


def pipeline():
    dataclanJson=getClanJson(myKey, clanTag)
    clanMatrix=getDFfromJson(dataclanJson)
    playersInfo=getValues(clanMatrix, members)
    playersStatList = playersInfo[0]
    playersDF=getPlayersStatList(playersStatList)
    print (playersDF)
    return playersDF

# Update csv on google sheets
updatedDF=originalDF.append(other=pipeline())
spread = Spread('skoy87@clannopalmoil.iam.gserviceaccount.com', 'clan')
spread.df_to_sheet(updatedDF, index=False, sheet='clan', start='A1', replace=True)

# Is this script gets stuck, refresh the web spreadsheet page
