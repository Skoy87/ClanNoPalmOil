import requests
import numpy as np
import json
import pandas as pd
import time
import calendar
import datetime
import xlsxwriter
import csv
mykey='insert private API key'
headers = {
    'auth': mykey
}

def getPlayersUrl(players):
    list_url = []
    for player in players:
        url='https://api.royaleapi.com/player/'+player
        list_url.append(url)
    return list_url

def getDataFromUrl(players):
    #downloading API as .json
    url_list = getPlayersUrl(players)
    headers = {
    'auth': mykey
    }
    data = [dict() for x in range(0,len(url_list))]
    for i in range(0,len(url_list)):
        response = requests.request('GET', url_list[i], headers=headers)
        data[i] = response.json()
    return data
#df=pd.DataFrame(dict([(k,pd.Series (v)) for k,v in data.items()]))
#print(df)

'''
urlclan='https://api.royaleapi.com/clan/2GRV8JVY'
responseclan  = requests.request('GET', urlclan, headers=headers)
dataclan=responseclan.json()
'''




def getDFfromDict(d):
    newDf = pd.DataFrame()
    lindx = ['name','tag', 'trophies', 'donations', 'donationsReceived', 'donationsDelta', 'clan', 'members']
    for k,v in d.items():
        if isinstance(v, dict):
            getDFfromDict(v)
            if k in lindx :
                #newDf = newDf.append({k : v}, ignore_index=True)
                newdf2 = pd.DataFrame(v)
                newDf = newDf.append(newdf2, ignore_index=True)
        else:
            if k in lindx :
                newDf = newDf.append({k : v}, ignore_index=True)
    return newDf

'''
clanGetValues=getDFfromDict(dataclan)
print(clanGetValues)
'''

def getValues(newDf, lindx):
    validvalues = []
    for i in lindx:
        firstValid = newDf[i][newDf[i].first_valid_index()]
        validvalues.append(firstValid)
        # print(validvalues)
        # print(firstValid)
        # print (validvalues)
        #finaldf=finaldf.append(validvalues)
    return validvalues
'''
lindx = ['members']
validateClanValues=getValues(clanGetValues, lindx)
print(validateClanValues)
'''

def getPlayerDF(data, lindx):
    newDf=getDFfromDict(data)
    startdf = pd.DataFrame(index=list(lindx))
    finalDF=startdf.assign(Valori = getValues(newDf,lindx))
    return finalDF

#print (getPlayerDF(data))

def getAllPlayers(data, players,lindx):

    startdf = pd.DataFrame(index=list(lindx))
    for i in range(0,len(players)):
        startdf[i] = getPlayerDF(data[i],lindx)
    return startdf

def pipeline():

    lindx = ['name', 'tag', 'trophies', 'donations', 'donationsReceived', 'donationsDelta']

    #players = getPlayersNames(clanUrl)
    players = ['8RLVV20PY', '8RLVV02PY']
    data = getDataFromUrl(players=players)
    allPlayersDf = getAllPlayers(data, players, lindx)
    return allPlayersDf

final = pipeline()
print(final)
