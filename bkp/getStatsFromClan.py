import requests
import numpy as np
import json
import pandas as pd
import time
import calendar
import datetime
import xlsxwriter
import csv

mykey='b0cab65a56f141d28fb04a4ee29aa8f10230573afbb149f3a6bbf160a68de0a7'
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

def getPlayerDF(data, lindx):
    newDf=getDFfromDict(data)
    startdf = pd.DataFrame(index=list(lindx))
    finalDF=startdf.assign(Valori = getValues(newDf,lindx))
    return finalDF

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
#print(final)



urlclan='https://api.royaleapi.com/clan/2GRV8JVY'
responseclan  = requests.request('GET', urlclan, headers=headers)
dataclan=responseclan.json()


#firstValid = newDf[i][newDf[i].first_valid_index()]

clanGetValues=getDFfromDict(dataclan)
#print(clanGetValues)
clanMembersList = clanGetValues['members'][clanGetValues['members'].first_valid_index()]
lindx = ['name','tag', 'trophies', 'donations', 'donationsReceived', 'donationsDelta']
#print(clanMembersList)
startdf = pd.DataFrame()
for player in clanMembersList:
    finalDF=getPlayerDF(player,lindx)
    #finalDF=finalDF.append(finalDF[i])
    startdf=startdf.append(other=finalDF)
print (startdf)



