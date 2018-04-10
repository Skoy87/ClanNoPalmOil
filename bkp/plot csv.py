import matplotlib.pyplot as plt
import pandas as pd
dfToPlot=pd.read_csv(filepath_or_buffer='clan.csv')

print(dfToPlot.plot())
plt.show()