import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import numpy as np

# style.use('seaborn-colorblind')


def timeseries(data, n):
	colors = plt.cm.GnBu(np.linspace(0, 1, n))

	conc = pd.read_csv(data,
					sep='\s+',
					parse_dates =[['Date', 'Time']])

	conc['Date_Time'] = pd.to_datetime(conc['Date_Time'], format = '%d.%m %H:%M')
	conc['Date_Time'] = conc['Date_Time'].apply(lambda x: x+pd.DateOffset(years=110))
	conc.set_index('Date_Time', drop = True)

	fig, axes = plt.subplots(nrows = n, ncols =1, sharex = True, sharey= True, figsize=(15,10))

	print(conc.head())

	for i in range(n):
   		conc.iloc[0:360,i::n].plot.area(ax=axes[i], ylim = [0,80], color = colors)

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
		if i % 2 != 0:
			axes[i].yaxis.tick_right()
		
	# handles, labels = ax.get_legend_handles_labels()
	fig.text(0.04, 0.5, '$CH_4$ concentration [$\mu g / m^3$]', fontsize = 12, va='center', rotation='vertical')
	plt.subplots_adjust(left=0.09, bottom=0.10, right=0.94, top=0.90, wspace=0.2, hspace=0.0)
	# fig.legend(handles, labels, loc = (0.5, 0), ncol=3 )
	# fig.legend(handles, ('Point Source', 'Line Source', 'Area Source'), loc=1, ncol=3, mode="expand", borderaxespad=0.)
	#plt.legend(bbox_to_anchor=(0, 0),
	#            bbox_transform=plt.gcf().transFigure)
	return ax



timeseries('case_1.txt',3)