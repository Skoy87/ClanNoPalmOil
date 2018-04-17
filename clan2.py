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

    for i in players:
        pla=list(i.values())
        DFdata.append(pla)
    # print (DFdata)
    df = pd.DataFrame(data= DFdata,columns=list(dict(values[0]).keys()))
    df=df.drop(columns=['rank','previousRank', 'expLevel', 'donationsDelta', 'arena', 'donationsPercent','role'])
    df['date']= timenow
    return df


def makeSql(df):
    conn=sqlite3.connect('Clan2.db')
    cur = conn.cursor()
    df.to_sql('clan2',conn, if_exists='replace', index=False)
    dfSQL = pd.read_sql_query("select * from clan2;", conn)
    # print (dfSQL)
    cur.close()
    conn.close()
    return dfSQL


def pipeline():
    data=getAPI(clanTag)
    df=makeDF(data)
    dfSQL = makeSql(df)
    print(dfSQL)
    return dfSQL

pipeline()
