import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import os
import glob

style.use('seaborn-colorblind')
path = r'C:\Users\mrp\Desktop\GralGramm_PostProcessing\Receptor_zeitreihe'
all_files = glob.iglob(os.path.join(path, "*.dat"))
frames = [pd.read_csv(f, sep = '\s+',header = None) for f in all_files]
df = pd.concat(frames, axis= 1, ignore_index = True)
df[0] = pd.to_datetime(df[0])

df.index = df[0]
del df[0]

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