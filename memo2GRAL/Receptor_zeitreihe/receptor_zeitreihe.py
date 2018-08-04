import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

frame1 = pd.read_csv('timeseries.dat', header= None)
frame1 = pd.to_datetime(frame1[0], format = '%Y-%m-%d %H:%M:%S')
frame2 = pd.read_csv('zeitreihe.dat', sep ='\s+', header= None)

df  = pd.concat([frame1, frame2], axis = 1, ignore_index=True)
df.index = df[0]
del df[0]

print(df)

n=3

fig, axes = plt.subplots(nrows = n, ncols =1, sharex = True, sharey= True, figsize=(10,7.5))

for i in range(n):
   	df.iloc[:,i].plot(ax=axes[i], marker='.')

for ax in axes:
	ax.set_xlabel('Time')
	ax.tick_params(which='both',
                   bottom = 'off',
                   left='off',
                   right='off',
                   top='off')
	ax.grid(linewidth =0.25, linestyle= 'dotted')
	ax.legend().set_visible(False)

for i in range(n):
	if i % 2 == 0:
		axes[i].yaxis.tick_right()
		
fig.text(0.02, 0.5, '$CH_4$ concentration [$\mu g / m^3$]', fontsize = 12, va='center', rotation='vertical')
# fig.text(0.5, 0.02, 'Time', fontsize = 12)
plt.subplots_adjust(left=0.09, bottom=0.10, right=0.94, top=0.90, wspace=0.2, hspace=0.0)
plt.show()