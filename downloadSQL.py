import mysql.connector
import sshtunnel
from sshtunnel import open_tunnel
import logging
import pandas as pd
pd.options.display.width=None

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
# sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG


query1 = 'select * from clan;'
query2 = 'select * from dailyDon where dailyDonations < 130 order by tag;'
query3 = 'select date, name, dailyDonations from dailyDon where dailyDonations < 100 order by name;'

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


    dfSQL = pd.read_sql_query(query2, connection)

    print (dfSQL)
    connection.close()