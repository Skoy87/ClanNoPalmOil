import requests
import numpy as np
import json
import pandas as pd
import time
import calendar
import datetime
import xlsxwriter
import csv
import timing
originalDF=pd.read_csv(filepath_or_buffer='clan.csv')
print (originalDF)
ts = time.gmtime()
orario = time.strftime("%Y-%m-%d %H:%M:%S", ts)
pd.options.display.width=None

myKey='b0cab65a56f141d28fb04a4ee29aa8f10230573afbb149f3a6bbf160a68de0a7'
clanTag = '2GRV8JVY'
lindx = ['tag', 'name', 'trophies', 'donations', 'donationsReceived', 'donationsDelta']
members = ['members']


def getClanJson(myKey,clanTag):
    headers = {'auth': myKey}
    urlclan='https://api.royaleapi.com/clan/'+clanTag
    responseclan  = requests.request('GET', urlclan, headers=headers)
    dataclanJson=responseclan.json()
    return dataclanJson

# dataclanJson=getClanJson(myKey,clanTag)
# print (dataclanJson)


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
# clanMatrix=getDFfromJson(dataclanJson)


def getValues(newDf, members):
    validvalues = []
    for i in members:
        firstValid = newDf[i][newDf[i].first_valid_index()]
        validvalues.append(firstValid)
    return validvalues

# playersInfo=getValues(clanMatrix, members)
# playersStatList=playersInfo[0]


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
# playersDF=getPlayersStatList()
# print(playersStatList)


def pipeline():
    dataclanJson=getClanJson(myKey, clanTag)
    clanMatrix=getDFfromJson(dataclanJson)
    playersInfo=getValues(clanMatrix, members)
    playersStatList = playersInfo[0]
    playersDF=getPlayersStatList(playersStatList)
    print (playersDF)
    return playersDF


updatedDF=originalDF.append(other=pipeline())
updatedDF.to_csv(path_or_buf='clan.csv', index=False)