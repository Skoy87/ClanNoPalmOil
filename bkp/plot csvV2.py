import matplotlib.pyplot as plt
import pandas as pd
import time
font = {'family' : 'arial',
        'weight' : 'light',
        'size'   : 8}

plt.rc('font', **font)
pd.options.display.width=None
dfToPlot=pd.read_csv(filepath_or_buffer='clan.csv')
print(dfToPlot)
pivotedTrophies= dfToPlot.pivot(index='date', columns='name', values='trophies')
#pivotedTrophies.plot(legend(loc=7, fontsize=8))
print (pivotedTrophies)
#print(pivotedTrophies.plot())

for column in pivotedTrophies:
        plt.title(column)
        plt.xlabel('Tempo')
        plt.ylabel('Trofei')
        #plt.grid(True)
        singlePlayerSeries = pivotedTrophies[column]
plt.plot(singlePlayerSeries)








# groupTag=dfToPlot.groupby('tag')
# trop = groupTag['donations', 'donationsReceived']
#
#
# trop.plot(title='name')

# for name, trophies in dfToPlot.groupby('tag'):
#     trophies.plot(x='trophies', y='date', title='title')

#groupDF = dfToPlot.groupby(['tag', 'name']).count()
#print(groupDF)

#print(dfToPlot.plot())
plt.show()