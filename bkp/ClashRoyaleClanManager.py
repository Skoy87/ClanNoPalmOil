import requests
import json
import pandas as pd
import xlsxwriter
import csv
myKey= #api personal key
player=['8RLVV20PY']
url='https://api.royaleapi.com/player/'+player[0]
#writer = csv.writer(open("output3.csv", "w"))


headers = {
    'auth': myKey
}
response = requests.request('GET', url, headers=headers)
data = response.json()

data_pd =  pd.DataFrame(list(data.items()))
data_pd.columns = ['field', 'values']

list_fields_2_keep = ['name','trophies','tag']

keep_as_are = data_pd[data_pd['field'].isin(list_fields_2_keep)]
keep_as_are['from'] = pd.Series('parent',index=keep_as_are.index)
newsubset = keep_as_are

list_fields_2_change = ['clan','stats']
for i in list_fields_2_change:
    dict_2_tf = data_pd[data_pd['field']== i][['values']].values.item()
    subset = pd.DataFrame(list(dict_2_tf.items()))
    subset.columns = ['field', 'values']
    subset['from'] = pd.Series(i,index=subset.index)
    newsubset=newsubset.append(subset,ignore_index=True)

fields_2_keep = ['donations','donationsReceived']
prova = newsubset[newsubset['field'].isin(fields_2_keep)]
print(prova)
