import sys
import statplot
import numpy as np
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import *
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from mplconfig import styles

# Q from 2 to 8
# use stack plot 

def plotstructure(data,samplenums,samplenames,fig_prefix="structure",width=0.8):
	colors = styles(8)[0]

	fig = plt.figure(figsize=(10,8))
	mapGS = gridspec.GridSpec(14,1,wspace=0.0,hspace=0.0,height_ratios=[2,1,0.1,1,0.1,1,0.1,1,0.1,1,0.1,1,0.1,1])
	tmpdata = data[-1]
	pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(tmpdata,'correlation')) # tmpdata n * p
	clusters = linkage(pairwise_dists,method='average')
	denAX = fig.add_subplot(mapGS[0,0])
	denD = dendrogram(clusters)
	xticks = denAX.get_xticks()
	#denAX.set_linewidth(1.0)
	denAX.set_axis_off()
	
	# tmp = np.float64(data[:,col_denD['leaves']])
	samplenames = np.asarray(samplenames)[denD['leaves']]
	# then to plot each kinds of structure
	xticks = (xticks-xticks[0])/(xticks[1]-xticks[0])
	#set_link_color_palette(colors)
	#sch.set_link_color_palette(['black'])

	for i in xrange(7): # stack[col_denD['leaves'],:]
		ax = fig.add_subplot(mapGS[i*2+1,0])
		tmpdata = data[i][denD['leaves'],:]
		tmpdata = tmpdata.T
		n,p = tmpdata.shape # 
		assert p == samplenums
		for j in xrange(n):
			if j:
				cumtmp = cumtmp + np.asarray(tmpdata[j-1,:])
				rects = ax.bar(xticks,np.asarray(tmpdata[j,:]),width=width,color=colors[j],linewidth=0,alpha=1.0,bottom=cumtmp,align='center')
			else:
				cumtmp = 0
				rects = ax.bar(xticks,np.asarray(tmpdata[j,:]),width=width,color=colors[j],linewidth=0,alpha=1.0,align='center')
		statplot.clean_axis(ax)
		ax.set_ylabel("$k = %d$"%(i+2))
		ax.set_ylim(0,1)
		ax.set_xlim(xticks[0]-width/2,xticks[-1]+width/2)
		if i == 5:
			pass
			#ax.set_xticklabels(samplenames,rotation=90)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=600)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	print samplenames
	return 0

if __name__=="__main__":
	prefix = sys.argv[1]
	samplelist = open(prefix+".fam","r")
	samplenum = 0
	samplename = []
	for line in samplelist:
		if line.startswith("#"):continue
		samplenum += 1
		samplename.append(line.rstrip("\n").split()[0])
	data = []
	for i in xrange(2,9):
		f = open(prefix+".%d.Q"%i,"r")
		tmpdata = []
		for line in f:
			tmpdata.append(line.rstrip().split())
		f.close()
		tmpdata = np.float64(tmpdata)
		data.append(tmpdata.copy())
		print data
	#plotstructure(data,samplenum,samplename,fig_prefix=prefix)
	plotstructure(data,samplenum,samplename)


