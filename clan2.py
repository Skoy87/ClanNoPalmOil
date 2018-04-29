import timing
import sqlite3
import requests
import pandas as pd
import time
ts = time.gmtime()
timenow = time.strftime("%Y-%m-%d %H:%M", ts)
pd.options.display.width=None

clanTag='2GRV8JVY'

def getAPI(clanTag):
    url = "https://api.royaleapi.com/clan/"+clanTag+'?keys=members'
    headers = {
        'auth': "b0cab65a56f141d28fb04a4ee29aa8f10230573afbb149f3a6bbf160a68de0a7"
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data



def makeDF(data):
    values = list(data.values())[0]
    players = list(data.values())[0]
    DFdata=[]
    namesList=[]
    for i in players:
        player=list(i.values())
        namesList.append(player[0])  # name
        DFdata.append(player)
    # print (DFdata)
    df = pd.DataFrame(data= DFdata,columns=list(dict(values[0]).keys()))
    df=df.drop(columns=['rank','previousRank', 'expLevel', 'donationsDelta', 'arena', 'donationsPercent','role'])
    df['date']= timenow
    print (df)
    return df
# asd = makeDF(getAPI(clanTag))

def makePlayerValues(data):
    values = list(data.values())[0]
    players = list(data.values())[0]
    DFdata=[]
    for i in players:
        player=list(i.values())
        DFdata.append(player)
    return DFdata

# print(makePlayerValues(getAPI(clanTag)))


def makeNamesList(data):
    players = list(data.values())[0]
    namesList=[]
    for i in players:
        player=list(i.values())
        namesList.append(player[0])
    return namesList


def makeSql(df):
    conn=sqlite3.connect('Clan2.db')
    cur = conn.cursor()
    df.to_sql('clan2',conn, if_exists='append', index=False)
    dfSQL = pd.read_sql_query("select * from clan2;", conn)
    # print (dfSQL)
    cur.close()
    conn.close()
    return dfSQL

'''
def tableForEachPlayer(namesList, DFdata, data):
    conn = sqlite3.connect('Clan2.db')
    values = list(data.values())[0]
    print (DFdata)
    for i in namesList:
        df = pd.DataFrame(data=DFdata, columns=list(dict(values[0]).keys()))
        df = df.drop(columns=['rank','clanChestCrowns', 'previousRank', 'expLevel', 'donationsDelta', 'arena', 'donationsPercent', 'role'])
        df['date'] = timenow
        makeSQL=df.to_sql(i, conn, if_exists='append', index=False)
        read= pd.read_sql_query("select * from "+"'"+str(i)+"'"+" where name = '"+str(i)+"'"+";", conn)
        print(read)
    conn.close()
'''


def pipeline():
    data=getAPI(clanTag)
    df=makeDF(data)
    dfSQL = makeSql(df)
    namesList=makeNamesList(data)
    print(dfSQL)
    print (namesList)
    return dfSQL

pipeline()
