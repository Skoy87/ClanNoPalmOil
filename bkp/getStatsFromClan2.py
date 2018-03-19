import requests
import numpy as np
import json
import pandas as pd
import xlsxwriter
import csv
import os
from time import gmtime, strftime
ora = strftime("%a, %d %b %Y %H_%M_%S +0000", gmtime())
orario = str(ora)[0:-6]
#pd.set_option('display.max_rows', -1)

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
    #print (validvalues)
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


#Get clan data as list
urlclan='https://api.royaleapi.com/clan/2GRV8JVY'
responseclan  = requests.request('GET', urlclan, headers=headers)
dataclan=responseclan.json()

def getClanData(dataclan):
    clanGetValues=getDFfromDict(dataclan)
    #print(clanGetValues)
    clanMembersList = clanGetValues['members'][clanGetValues['members'].first_valid_index()]
    return clanMembersList

#print (getClanData(dataclan))


def getPlayerStatsFromClan(dataclan):
    lindx = ['name','tag', 'trophies', 'donations', 'donationsReceived', 'donationsDelta']
    #print(clanMembersList)
    startdf = pd.DataFrame()
    for player in getClanData(dataclan):
        finalDF=getPlayerDF(player,lindx)
        #finalDF=finalDF.append(finalDF[i])
        startdf=startdf.append(other=finalDF)
        #print(startdf)
    return startdf
startingDF=getPlayerStatsFromClan(dataclan)
#print (getDFfromDict(dataclan))
print (startingDF)







############################################# CSV Work in progress #############################################
'''
dfCsv=startingDF.to_csv('clan.csv', mode='w')
dfCsv=startingDF.to_csv('clanupdated.csv', mode='w')
def appendUpdate():
    csvinput=open('clan.csv','r')
    csvoutput=open('clanupdated.csv', 'w')
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)
    all = []
    row = next(reader)
    row.append(orario)
    all.append(row)
    for row in reader:
        row.append(row[1])
        all.append(row)
    writer.writerows(all)
    csvinput.close()
    csvoutput.close()
    os.rename('clan.csv', 'originalbk '+str(orario)+'.csv')

# def appendUpdate():
#     with open('clan.csv','r') as csvinput:
#         with open('clanupdated.csv', 'w') as csvoutput:
#             writer = csv.writer(csvoutput, lineterminator='\n')
#             reader = csv.reader(csvinput)
#
#             all = []
#             row = next(reader)
#             row.append(orario)
#             all.append(row)
#
#             for row in reader:
#                 row.append(row[1])
#                 all.append(row)
#
#             writer.writerows(all)
#             #os.rename('clan.csv','original.csv')

appendUpdate()
#os.rename('C:\\Users\\Alessio\\PycharmProjects\\clan manager\\clan.csv','C:\\Users\\Alessio\\PycharmProjects\\clan manager\\original.csv')
os.rename('clanupdated.csv','clan.csv')
'''