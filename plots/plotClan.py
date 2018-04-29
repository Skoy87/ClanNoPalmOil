from plotly.graph_objs import *
import plotly.offline as ply
import mysql.connector
import sshtunnel
from sshtunnel import open_tunnel
# import logging
import pandas as pd
pd.options.display.width=None
import plotly.plotly as py
py.sign_in('colizzaa', 'cYxFLBypGC6pyb6wfgdu')


# def sshToSQL():
#     sshtunnel.SSH_TIMEOUT = 5.0
#     sshtunnel.TUNNEL_TIMEOUT = 5.0
#     with sshtunnel.SSHTunnelForwarder(
#         ('ssh.pythonanywhere.com'),
#         ssh_username='skoyron', ssh_password='Alessiolm6666',
#         remote_bind_address=('skoyron.mysql.pythonanywhere-services.com', 3306)
#     ) as tunnel:
#         connection = mysql.connector.connect(
#             user='skoyron', password='alessio6',
#             host='127.0.0.1', port=tunnel.local_bind_port,
#             database='skoyron$default',
#         )
#         # data = db.query(sql).store_result()
#         dfSQL = pd.read_sql_query('select * from dailyDon;', connection)
#         connection.close()
#         return dfSQL


def plot(player, name):
    trace1 = {
      "x": player['date'],
      "y": player['trophies'],
      "hoverinfo": "y+name",
      "marker": {
        "size": 10,
        "symbol": "circle"
      },
      "mode": "lines+markers+text",
      "name": "trophies",
      "textposition": "top center",
      "textsrc": "colizzaa:13:e83232",
      "type": "scatter",
      "uid": "d402f9",
      "xsrc": "colizzaa:13:94b66f",
      "yaxis": "y2",
      "ysrc": "colizzaa:13:e83232"
    }
    trace2 = {
      "x": player['date'],
      "y": player['dailyDonations'],
      "hoverinfo": "y+name",
      "line": {"width": 2},
      "marker": {
        "size": 20,
        "symbol": "circle-open-dot"
      },
      "mode": "lines+markers",
      "name": "dailyDonations",
      "text": ["60.0", "89.0", "222.0", "63.0", "104.0", "163.0", "122.0"],
      "textsrc": "colizzaa:13:10ed51",
      "type": "scatter",
      "uid": "197e4c",
      "xsrc": "colizzaa:13:94b66f",
      "ysrc": "colizzaa:13:10ed51"
    }
    trace3 = {
      "x": player['date'],
      "y": player['dailyRDonations'],
      "hoverinfo": "y+name",
      "line": {
        "shape": "hvh",
        "width": 1
      },
      "marker": {
        "size": 11,
        "symbol": "diamond-open-dot"
      },
      "mode": "lines+markers",
      "name": "dailyRDonations",
      "text": ["110.0", "80.0", "120.0", "120.0", "80.0", "160.0", "80.0"],
      "textsrc": "colizzaa:13:52c3b8",
      "type": "scatter",
      "uid": "0f7731",
      "xsrc": "colizzaa:13:94b66f",
      "yaxis": "y",
      "ysrc": "colizzaa:13:52c3b8"
    }
    data = Data([trace1, trace2, trace3])
    layout = {
      "autosize": True,
      "hovermode": "closest",
      "showlegend": True,
      "title": name,
      "xaxis": {
        "autorange": True,
        "hoverformat": "%A",
        "nticks": 0,
        "range": ["2018-04-23 08:28:22.8116", "2018-04-29 23:17:37.1884"],
        "tickformat": "",
        "title": "date",
        "type": "date"
      },
      "yaxis": {
        "autorange": False,
        "domain": [0, 0.45],
        "dtick": 40,
        "nticks": 0,
        "range": [-19, 290],
        "tick0": 20,
        "tickmode": "linear",
        "title": "dailyDonations",
        "type": "linear"
      },
      "yaxis2": {
        "anchor": "x",
        "autorange": False,
        "domain": [0.55, 1],
        "dtick": 200,
        "range": [3800, 5000],
        "tick0": 0,
        "tickmode": "linear",
        "title": "trophies",
        "type": "linear"
      }
    }
    fig = Figure(data=data, layout=layout)
    py.image.save_as(fig, filename=str(name.replace('.',' ').replace(':',' ').replace('*',' '))+'.png')
    #ply.plot(fig,filename=str(count)+'.png')


def makePlayerDF():
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='skoyron', ssh_password='Alessiolm6666',
        remote_bind_address=('skoyron.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        connection = mysql.connector.connect(
            user='skoyron', password='alessio6',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='skoyron$default',
        )
        count=0
        df = pd.read_sql_query('select name from dailyDon group by name;', connection)
        # print (df['name'])
        for name in df['name']:
            # print(name, 'ciao')
            count +=1
            print (count)
            dfname = pd.read_sql_query('select * from dailyDon where name="'+name+'";', connection)
            plot(dfname, name)
            # print(stop the loop)
    connection.close()


plotPlayerDF=makePlayerDF()

