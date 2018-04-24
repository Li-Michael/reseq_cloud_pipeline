# -*- coding: UTF-8 -*-
import sys
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from matplotlib import font_manager as fm
#from matplotlib_venn import venn2,venn3
import itertools
import mutilstats
import scipy.cluster.hierarchy as sch


# for projection='3d'
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import fcluster; import pandas

###
from matplotlib.patches import Polygon
# to get kmeans and scipy.cluster.hierarchy
from scipy.cluster.vq import *
from scipy.cluster.hierarchy import *

###
from matplotlib.colors import LogNorm

##kmeans归一化处理 from scipy.cluster.vq import whiten
from scipy.cluster.vq import whiten
#mpl.style.use('ggplot')

#import mplconfig
#from mplconfig import styles,color_grad,rgb2hex

def dirDetectCreate(dir):
	if not os.path.isdir(dir):
		try:
			os.mkdir(dir)
		except:
			sys.stderr.write("[ERROR] Cannot creat dir: %s!\n"%(dir))
			return 1
	return 0

def test_iter(num):
	fig = plt.figure(dpi=300)
	x = 1
	y = 1
	ax = fig.add_subplot(111)
	ret_color,ret_lines,ret_marker = styles(num)
	for i in xrange(num):
		ax.plot([x,x+1,x+2,x+3,x+4],[y,y,y,y,y],color=ret_color[i],linestyle=ret_lines[i],marker=ret_marker[i],markeredgecolor=ret_color[i],markersize=12,alpha=0.8)
		y += 1
	plt.savefig("test_style.png",format='png',dpi=300)	
	plt.clf()
	plt.close()
	return 0

def admixture_plot():
	return 0


def plot_enrich(resultmark,resultothers,fig_prefix,xlabel,ylabel):
	fig = plt.figure(figsize=(8,6),dpi=300)
	num = len(resultmark) + 1
	ret_color,ret_lines,ret_marker = styles(num)
	ax = fig.add_subplot(111)
	maxlim = 0
	for i in xrange(num-1):
		#ax.plot(resultmark[i][1],resultmark[i][2],ret_color[i]+ret_marker[i],label=resultmark[i][0],markeredgecolor=ret_color[i],markersize=8,alpha=0.7)
		ax.plot(resultmark[i][1],resultmark[i][2],color=ret_color[i],linestyle='',marker=ret_marker[i],label=resultmark[i][0],markeredgecolor=ret_color[i],markersize=10,alpha=0.7)
		if resultmark[i][2] > maxlim:
			maxlim = resultmark[i][2]
	xarr = []
	yarr = []
	for ret in resultothers:
		xarr.append(ret[0])
		yarr.append(ret[1])
	ax.plot(xarr,yarr,'ko',label="others",markeredgecolor='k',markersize=3,alpha=0.5)
	art = []
	lgd = ax.legend(bbox_to_anchor=(1.02, 1),loc=0,borderaxespad=0,numpoints=1,fontsize=6)
	art.append(lgd)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_ylim(0,maxlim+2)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',additional_artists=art,bbox_inches="tight",dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',additional_artists=art,bbox_inches="tight",dpi=300)
	plt.clf()
	plt.close()
	return 0

# 1425     ax1.scatter(xy[:,0],xy[:,1],c=colors)
#1426     ax1.scatter(res[:,0],res[:,1], marker='o', s=300, linewidths=2, c='none')
#1427     ax1.scatter(res[:,0],res[:,1], marker='x', s=300, linewidths=2)

def sim_scatter(X,Y,xlabel,ylabel,alpha=0.3,fig_prefix="simscatter"):
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	ax.scatter(X,Y,marker='o',linewidths=0,color='gray',alpha=alpha)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0
def scatter2(x,y,xlabel,ylabel,addline=None,fig_prefix="test",alpha=0.6): # line is  [[x1,x2],[y1,y2]] = addline
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	colors = styles(3)[0]
	ax.scatter(x,y,marker='o',linewidths=0,color=colors[0],alpha=alpha) #,label=labels[0])
	if addline <> None:
		[x1,x2],[y1,y2] = addline
		ax.plot([x1,x2],[y1,y2],color="gray",ls='--',lw=1.0) #ax.plot(xp,yp,color=colors[n-i-1],linestyle='--',lw=1.0)
		#ax.set_xlim(x1,x2)
		#ax.set_ylim(y1,y2)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close()
	return 0

def scatter(xother,yother,xsig,ysig,xlabel="X",ylabel="Y",labels =["No differential","Up regulated","Down regulated"] ,fig_prefix="DEGs_scatter_plot",alpha=0.3):
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xother = np.asarray(xother)
	yother = np.asarray(yother)
	xsig   = np.asarray(xsig)
	ysig   = np.asarray(ysig)
	ax.scatter(xother,yother,marker='^',linewidths=0,color='gray',alpha=alpha,label=labels[0])
	ax.scatter(xsig[ysig>xsig],ysig[ysig>xsig],marker='o',linewidths=0,color='#F15B6C',alpha=alpha,label=labels[1])
	ax.scatter(xsig[xsig>ysig],ysig[xsig>ysig],marker='o',linewidths=0,color='#2A5CAA',alpha=alpha,label=labels[2])
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.grid(True)
	ax.legend(loc=0,scatterpoints=1)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0


def venn_plot(datalist,setnames,fig_prefix="venn_plot",hplot=None):
	if len(setnames) == 2: 
		vennfun = venn2
		colors_arr = ["magenta","cyan"]
	elif len(setnames) == 3: 
		vennfun = venn3
		colors_arr = ["magenta","cyan","blue"]
	else:
		sys.stderr.write("[Warning] Only support 2 or 3 sets' venn plot")
		return 1
	fig = plt.figure(figsize=(5,4),dpi=300)
	ax = fig.add_subplot(111)
	vennfun(datalist,setnames,normalize_to=1,set_colors=colors_arr,alpha=0.3)
	plt.savefig(fig_prefix+"_venn.png",format='png',dpi=300)
	plt.savefig(fig_prefix+"_venn.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	dirDetectCreate(fig_prefix+"_venn_list")
	outdir = fig_prefix+"_venn_list"
	if len(setnames) == 3:
		f = file(outdir+"/"+setnames[0]+".specific.lst.xls","w")
		f.write("\n".join(datalist[0]-(datalist[1] | datalist[2] )))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[1]+".specific.lst.xls","w")
		f.write("\n".join(datalist[1]-(datalist[0] | datalist[2] )))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[2]+".specific.lst.xls","w")
		f.write("\n".join(datalist[2]-(datalist[0] | datalist[1] )))
		f.write("\n")
		f.close()
		comb = datalist[0] & datalist[2] & datalist[1]
		f = file(outdir+"/"+setnames[0]+"_and_"+setnames[1]+".lst.xls","w")
		f.write("\n".join(datalist[0] & datalist[1] - comb))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[1]+"_and_"+setnames[2]+".lst.xls","w")
		f.write("\n".join(datalist[1] & datalist[2] - comb))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[0]+"_and_"+setnames[2]+".lst.xls","w")
		f.write("\n".join(datalist[0] & datalist[2] - comb))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[0]+"_and_"+setnames[1]+"_and_"+setnames[2]+".lst.xls","w")
		f.write("\n".join(datalist[0] & datalist[2] & datalist[1] ))
		f.write("\n")
		f.close()
	if len(setnames) == 2:
		f = file(outdir+"/"+setnames[0]+".specific.lst.xls","w")
		f.write("\n".join(datalist[0]-datalist[1]))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[1]+".specific.lst.xls","w")
		f.write("\n".join(datalist[1]-datalist[0] ))
		f.write("\n")
		f.close()
		f = file(outdir+"/"+setnames[0]+"_and_"+setnames[1]+".lst.xls","w")
		f.write("\n".join(datalist[0] & datalist[1]))
		f.write("\n")
		f.close()
	return 0

def kdensity(var_arr,num = 200,fun='pdf',cdfstart=-np.inf):
	"""
	plot theory distribution
	y = P.normpdf( bins, mu, sigma)
	l = P.plot(bins, y, 'k--', linewidth=1.5)
	"""
	if fun not in ['cdf','pdf']:
		sys.stderr.write("kdensity Fun should be 'cdf' or 'pdf'")
		exit(1)
	#idx = mutilstats.check_vecnan(var_arr)
	#if idx == None:
	#	return [0,0],[0,0]
	#kden = stats.gaussian_kde(np.asarray(var_arr)[idx])
	kden = stats.gaussian_kde(np.asarray(var_arr))
	#kden.covariance_factor = lambda : .25	
	#kden._compute_covariance()
	min_a = np.nanmin(var_arr)
	max_a = np.nanmax(var_arr)
	xnew = np.linspace(min_a, max_a, num)
	if fun == 'cdf':
		ynew = np.zeros(num)
		ynew[0] = kden.integrate_box_1d(cdfstart,xnew[0])
		for i in xrange(1,num):
			ynew[i] = kden.integrate_box_1d(cdfstart,xnew[i])
	else: ynew = kden(xnew)
	return xnew,ynew
def hcluster(Xnp,samplenames,fig_prefix):
	linkage_matrix = linkage(Xnp,'ward','euclidean')
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	#dendrogram(linkage_matrix,labels=samplenames,leaf_label_rotation=45) ## new version of scipy
	dendrogram(linkage_matrix,labels=samplenames,orientation='right')
	ax.grid(visible=False)
	plt.savefig(fig_prefix+"_hcluster.png",format='png',dpi=300)
	plt.savefig(fig_prefix+"_hcluster.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def plot_hmc_curve(X,Y,colors,classlabels,figname_prefix="out",scale=0):
	#调和曲线生成Harmonic curve
	#X = n x p   Y is list, colors is list
	n,p = X.shape
	if n == len(Y) and len(Y) == len(colors):pass
	else: return 1
	
	if scale ==1:
		X = whiten(X)
	step = 100
	t = np.linspace(-np.pi, np.pi, num=step)
	f = np.zeros((n,step))
	for i in xrange(n):
		f[i,:] = X[i,0]/np.sqrt(2)
		for j in xrange(1,p):
			if j%2 == 1:
				f[i,:] += X[i,j]*np.sin(int((j+1)/2)*t)
			else:
				f[i,:] += X[i,j]*np.cos(int((j+1)/2)*t)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	uniq_colors = []
	for tmpcolor in colors:
		if tmpcolor not in uniq_colors:
			uniq_colors.append(tmpcolor)

	idx = [colors.index(color) for color in uniq_colors]
	labels = [classlabels[i] for i in idx]
	for i in idx:
		ax.plot(t,f[i,:],colors[i])
	ax.legend(labels,loc=0)
	for i in xrange(n):
		ax.plot(t,f[i,:],colors[i])
	ax.set_xlabel("$t(-\pi,\ \pi)$",fontstyle='italic')
	ax.set_ylabel("$f(t)$",fontstyle='italic')
	ax.grid(True)
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def plot_linear_regress(X,Y,xlabel,ylabel,classnum,h_uniq_colors,h_uniq_classlabels,figname_prefix="out"):
	##h_uniq_classlabels = {0:'class1',1:'class2'} , 0 and 1 must be the classnum
	##h_uniq_colors = {0:'r^',1:'b.'}
	plt.style.use('grayscale')
	if X.size != Y.size != len(classnum):
		sys.stderr("Error: X, Y should be same dimensions")
		return 1
	slope,intercept,rvalue,pvalue,stderr = stats.linregress(X,Y)
	tmpX = np.linspace(np.min(X),np.max(X),num=50)
	tmpY = tmpX*slope+intercept
	uniq_classnum = list(set(classnum))
	np_classnum = np.array(classnum)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(tmpX,tmpY,'k--')
	ax.grid(True,color='k',alpha=0.5,ls=':')
	for i in uniq_classnum:
		try:
			color = h_uniq_colors[i]
			label = h_uniq_classlabels[i]
		except:
			plt.clf()
			plt.close()
			sys.stderr("Error: key error")
			return 1
		idx = np.where(np_classnum == i)
		ax.plot(X[idx],Y[idx],color,label=label,alpha=0.6)
	ax.legend(loc=0,numpoints=1)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title('slope:%.3g,intercept:%.3g,r:%.3g,p:%.3g,stderr:%.3g'%(slope,intercept,rvalue,pvalue,stderr))
	ax.grid(True)
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

#def plot_vec_boxplot(Xvecs,fig_prefix,xlabels,ylabel,xticks_labels,outshow=1,colors=None,ylim=0):

def plot_boxplotscatter(X,fig_prefix,xlabel,ylabel,xticks_labels,colors=None,ylim=1,scatter=1):
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	bp = ax.boxplot(X)
	for box in bp['boxes']:
		box.set( color='#7570b3', linewidth=2)
		#box.set( facecolor = '#1b9e77')
	for whisker in bp['whiskers']:
		whisker.set(color='#7570b3', linewidth=2)
	for median in bp['medians']:
		median.set(color='red', linewidth=2)
	for flier in bp['fliers']:
		flier.set(marker='o', color='#e7298a', alpha=0)
	if scatter:
		for i in xrange(len(X)):
			x = np.random.normal(i+1, 0.03, size=len(X[i]))
			ax.plot(x, X[i], '.',color="#e7298a" ,alpha=0.3)
	ax.set_xticklabels(xticks_labels,rotation=45)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if ylim:
		ax1.set_ylim(-10,10)
	ax.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300);plt.savefig(fig_prefix+".svg",format='svg',dpi=300);
	plt.clf();plt.close()
	return 0

def plot_boxplot(Xnp,fig_prefix,xlabel,ylabel,xticks_labels,outshow=1,colors=None,ylim=1):
	fig = plt.figure(dpi=300)
	ax1 = fig.add_subplot(111)
	if outshow == 1:
		bp = ax1.boxplot(Xnp.T)
		plt.setp(bp['boxes'], color='white')
		plt.setp(bp['whiskers'], color='black')
		plt.setp(bp['fliers'], color='red', marker='+')
	else:
		bp = ax1.boxplot(Xnp.T,0,'')
	n,p = Xnp.shape
	
	if colors == None:
		colors = color_grad(n,cm.Paired) 
	for i in xrange(n):
		box = bp['boxes'][i]
		boxX = box.get_xdata().tolist()
		boxY = box.get_ydata().tolist()
		boxCoords = zip(boxX,boxY)
		boxPolygon = Polygon(boxCoords, facecolor=colors[i])
		ax1.add_patch(boxPolygon)
	ax1.set_xticklabels(xticks_labels,rotation=45)
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)
	if ylim:
		ax1.set_ylim(-10,10)
	ax1.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def plot_Xscore(Xnp,classnums,uniqclassnum,uniqcolor,uniqmarker,uniqclasslabel,fig_prefix,xlabel,ylabel,zlabel=None,dim=2):
	plt.style.use('grayscale')
	leng = len(uniqclassnum)
	Xnp = np.asarray(Xnp)
	fig = plt.figure(figsize=(10,8),dpi=300)
	if dim == 3:
		ax1 = fig.add_subplot(111,projection ='3d')
	elif dim==2:
		ax1 = fig.add_subplot(111)
	else:
		sys.stderr.write("[ERROR] Dim '%d' plot failed\n"%dim)
		return 1
	for i in xrange(leng):
		tmpclassidx = np.array(classnums) == uniqclassnum[i]
		tmplabel = uniqclasslabel[i]
		tmpcolor = uniqcolor[i%(len(uniqcolor))]
		tmpmarker = uniqmarker[i%(len(uniqmarker))]
		if dim == 2:
			ax1.plot(Xnp[tmpclassidx,0],Xnp[tmpclassidx,1],ls='',markerfacecolor=tmpcolor,marker=tmpmarker,label=tmplabel,markeredgecolor = tmpcolor,alpha=0.7,markersize=10)
			ax1.grid(True)
		else:ax1.plot(Xnp[tmpclassidx,0],Xnp[tmpclassidx,1],Xnp[tmpclassidx,2],ls='',markerfacecolor=tmpcolor,marker=tmpmarker,label=tmplabel,markeredgecolor = tmpcolor,alpha=0.7,markersize=10)
	ax1.legend(loc=0,numpoints=1)
	ax1.grid()
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)
	if dim == 3 and zlabel !=None:
		ax1.set_zlabel(zlabel)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0
def plot_XYscore(Xnp,Y,classnums,uniqclassnum,uniqcolor,uniqmarker,uniqclasslabel,fig_prefix,xlabel,ylabel,zlabel=None,dim=2):
	Xnp[:,dim-1] = Y[:,0]
	return plot_Xscore(Xnp,classnums,uniqclassnum,uniqcolor,uniqmarker,uniqclasslabel,fig_prefix,xlabel,ylabel,zlabel,dim)

def plot_markxy(X1,Y1,X2,Y2,xlabel,ylabel,fig_prefix):
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	ax.plot(X1,Y1,'b+')
	ax.plot(X2,Y2,'ro')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def plotline(Xvector,Ys,fig_prefix,xlabel,ylabel,colors,legends=None,title=None,xlimmax = None,ylimmax = None):
	n,p = Ys.shape
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	if legends:
		leng = len(legends)
	else:
		leng = 0
	for i in xrange(n):
		if i < leng:
			tmplabel = legends[i]
			ax.plot(Xvector,Ys[i,:],colors[i],label=tmplabel)
		else:
			ax.plot(Xvector,Ys[i,:],colors[i])
	if legends != None:
		ax.legend(loc=0)
	#ax.grid()
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if title != None:
		ax.set_title(title)
	if ylimmax:
		ax.set_ylim(0,ylimmax)
	if xlimmax:
		ax.set_xlim(0,p)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0
def barh_dict_class(hdata,fig_prefix,xlabel,ylabel,title = "",width=0.4,legends=[],colors=[],fmt="%.2f",ylog=0,rotation=0,plot_txt = 1):
	data = []
	yticklabels = []
	classnames = []
	classnumbers = [0] * len(hdata.keys())
	if not colors:
		color_class = cm.Paired(np.linspace(0, 1, len(hdata.keys())))
	else:
		color_class = colors
	idx = 0
	plot_idx = []
	plot_start = 0
	for classname in sorted(hdata.keys()):
		classnames.append(classname)
		for key in hdata[classname]:
			if hdata[classname][key] <=0:continue
			yticklabels.append(key)
			classnumbers[idx] += 1
			data.append(hdata[classname][key])
		plot_idx.append([plot_start,len(data)])
		plot_start += len(data)-plot_start
		idx += 1
	if len(data) > 16:
		fig = plt.figure(figsize=(5,15),dpi=300)
		fontsize_off = 2
	else:
		fig = plt.figure(figsize=(5,7),dpi=300)
	ax = fig.add_subplot(111)
	linewidth = 0
	alpha=0.8
	ylocations = np.asarray(range(len(data)))+width*2
	rects = []
	for i in xrange(len(plot_idx)):
		s,e = plot_idx[i]
		rect = ax.barh(ylocations[s:e],np.asarray(data[s:e]),width,color=color_class[i],linewidth=linewidth,alpha=alpha,align='center')
		rects.append(rect)
	ax.set_yticks(ylocations)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	ylabelsL = ax.set_yticklabels(yticklabels)
	ax.set_ylim(0,ylocations[-1]+width*2)
	tickL = ax.yaxis.get_ticklabels()
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 2)
	ax.xaxis.grid(True)
	ax.legend(classnames,loc=0,fontsize=8)
	#print fig.get_size_inches()
	fig.set_size_inches(10,12)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0
def bar_dict_class(hdata,fig_prefix,xlabel,ylabel,title = "",width=0.35,legends=[],colors=[],fmt="%.2f",ylog=0,rotation=0,plot_txt = 1):
	data = []
	xticklabels = []
	classnames = []
	classnumbers = [0] * len(hdata.keys())
	if not colors:
		color_class = cm.Paired(np.linspace(0, 1, len(hdata.keys())))
	else:
		color_class = colors
	idx = 0
	plot_idx = []
	plot_start = 0
	for classname in sorted(hdata.keys()):
		flagxx = 0
		for key in hdata[classname]:
			if hdata[classname][key] <=0:continue
			xticklabels.append(key)
			classnumbers[idx] += 1
			data.append(hdata[classname][key])
			flagxx = 1
		if flagxx:
			plot_idx.append([plot_start,len(data)])
			plot_start += len(data)-plot_start
			idx += 1
			classnames.append(classname)
	fontsize_off = 2
	if len(data) > 16:
		fig = plt.figure(figsize=(10,5),dpi=300)
		fontsize_off = 3
	else:
		fig = plt.figure(figsize=(7,5),dpi=300)
	ax = fig.add_subplot(111)
	if ylog:
		ax.set_yscale("log",nonposy='clip')
	linewidth = 0
	alpha=0.8
	xlocations = np.asarray(range(len(data)))+width*2
	#rects = ax.bar(xlocations,np.asarray(data),width,color=plot_colors,linewidth=linewidth,alpha=alpha,align='center')
	rects = []
	for i in xrange(len(plot_idx)):
		s,e = plot_idx[i]
		rect = ax.bar(xlocations[s:e],np.asarray(data[s:e]),width,color=color_class[i],linewidth=linewidth,alpha=alpha,align='center')
		rects.append(rect)
	max_height = 0
	if plot_txt:
		for rk in rects:
			for rect in rk:
				height = rect.get_height()
				if height < 0.1:continue
				ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='bottom',fontsize=(8-fontsize_off))
	ax.set_xticks(xlocations)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if rotation == 0 or rotation == 90:hafmt="center"
	else:hafmt="right"
	xlabelsL = ax.set_xticklabels(xticklabels,ha=hafmt,rotation=rotation)
	#print xlocations
	ax.set_xlim(0,xlocations[-1]+width*2)
	tickL = ax.xaxis.get_ticklabels()
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 2)
	ax.yaxis.grid(True)
	#print classnames
	if ylog:
		ax.set_ylim(0.99,np.max(data)*2)
	else:
		ax.set_ylim(0,np.max(data)*1.35)
	ax.legend(classnames,fancybox=True, loc=0, fontsize=(8-fontsize_off))
	#ax.legend(classnames,loc='upper center', bbox_to_anchor=(0.5, 1.0),ncol=6,fancybox=True, shadow=True)
	#else:
	#ax.xaxis.set_major_locator(plt.NullLocator())
	plt.tick_params(axis='x',          # changes apply to the x-axis
				    which='both',      # both major and minor ticks are affected
					bottom='off',      # ticks along the bottom edge are off
					top='off',         # ticks along the top edge are off
					labelbottom='on') # labels along the bottom edge are off
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0

def barlineraworder(data,xticklabels,fig_prefix,xlabel,ylabel,title = "",width=0.4,colors=[],fmt="%.2f",ylog=0,rotation=0,linecolor="r"):
	fig = plt.figure(figsize=(7,5),dpi=300)
	ax = fig.add_subplot(111)
	if ylog: ax.set_yscale("log",nonposy='clip')
	linewidth = 0; alpha=1.0
	if not colors:
		colors = styles(len(data))[0]
	xlocations = np.asarray(range(len(data)))+width*2
	rects = ax.bar(xlocations,np.asarray(data),width,color=colors,linewidth=linewidth,alpha=alpha,align='center')
	idxtmp = 0
	for rect in rects:
		height = rect.get_height()
		idxtmp += 1 
		if height < 0.1:continue
		if data[idxtmp-1] < 0: 
			height = -1 * height
			ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='top',fontsize=8)
		else:
			ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='bottom',fontsize=8)
	ax.plot(xlocations,data,ls='--',marker='.',markerfacecolor=linecolor,markeredgecolor=linecolor,color=linecolor)
	ax.set_xticks(xlocations)
	ax.set_ylabel(ylabel); ax.set_xlabel(xlabel)
	if rotation == 0 or rotation == 90:
		hafmt='center'
	else:hafmt = 'right'
	xlabelsL = ax.set_xticklabels(xticklabels,ha=hafmt,rotation=rotation)
	ax.set_title(title)
	ax.set_xlim(0,xlocations[-1]+width*2)
	tickL = ax.xaxis.get_ticklabels()
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 2)
	ax.yaxis.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0

def bar_dict(hdata,fig_prefix,xlabel,ylabel,title = "",width=0.4,legends=[],colors=[],fmt="%.2f",ylog=0,hlist=None,rotation=0,filter_flag=1):
	data = []
	xticklabels = []
	if hlist == None:
		for key in sorted(hdata):
			if hdata[key] <=0 and filter_flag:
				continue
			xticklabels.append(key)
			data.append(hdata[key])
	else:
		for key in sorted(hlist):
			if hdata[key] <=0 and filter_flag:
				continue
			xticklabels.append(key)
			data.append(hdata[key])
	fig = plt.figure(figsize=(7,5),dpi=300)
	ax = fig.add_subplot(111)
	if ylog:
		ax.set_yscale("log",nonposy='clip')
	linewidth = 0
	alpha=1.0
	if not colors:
		colors = cm.Accent(np.linspace(0, 1, len(data)))
	xlocations = np.asarray(range(len(data)))+width*2
	rects = ax.bar(xlocations,np.asarray(data),width,color=colors,linewidth=linewidth,alpha=alpha,align='center')
	idxtmp = 0
	for rect in rects:
		height = rect.get_height()
		idxtmp += 1
		if height < 0.1:continue
		if data[idxtmp-1] < 0: 
			height = -1 * height
			ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='top',fontsize=8)
		else:
			ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='bottom',fontsize=8)
	ax.set_xticks(xlocations)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if rotation == 0 or rotation == 90:
		hafmt='center'
	else:
		hafmt = 'right'
	xlabelsL = ax.set_xticklabels(xticklabels,ha=hafmt,rotation=rotation)
	#if rotation:
	#	for label in xlabelsL:
	#		label.set_rotation(rotation)
	ax.set_title(title)
	ax.set_xlim(0,xlocations[-1]+width*2)
	tickL = ax.xaxis.get_ticklabels()
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 2)
	ax.yaxis.grid(True)
	#ax.set_adjustable("datalim")
	if ylog and filter_flag:
		ax.set_ylim(0.99,np.max(data)*2)
	elif filter_flag:
		ax.set_ylim(0,np.max(data)*1.5)
	#ax.set_ylim(ymin=0)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0

def cluster_stackv_bar_plot(data,xticks_labels,fig_prefix,xlabel,ylabel,title="",width=0.7,legends=[],colors=[],scale=0,rotation=0,nocluster=0,noline=0):
	Xnpdata = data.T.copy()
	#Xnpdata = np.random.random((12,9))
	lfsm = 8 
	if len(xticks_labels) > 40:
		lfsm  = int(len(xticks_labels) * 1.0 * 8/40); lfsm = np.min([lfsm,16])
	widsm = 8
	fig = plt.figure(figsize=(widsm,lfsm))
	stackmapGS = gridspec.GridSpec(1,2,wspace=0.0,hspace=0.0,width_ratios=[0.15,1])
	if not nocluster:
		col_pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(Xnpdata,'euclidean'))
		#print col_pairwise_dists
		col_clusters = linkage(col_pairwise_dists,method='ward')
		col_denAX = fig.add_subplot(stackmapGS[0,0])
		col_denD = dendrogram(col_clusters,orientation='left')
		col_denAX.set_axis_off()

	n,p = data.shape
	ind = np.arange(p)
	if not nocluster:
		tmp = np.float64(data[:,col_denD['leaves']])
	else:
		tmp = data
	if scale:  
		tmp = tmp/np.sum(tmp,0)*100
	if not colors:
		colors = styles(n)[0]
	lfsm = 8

	stackvAX = fig.add_subplot(stackmapGS[0,1])
	linewidth = 0
	alpha=0.8
	def plot_line_h(ax,rects):
		for i in xrange(len(rects)-1):
			rk1 = rects[i]
			rk2 = rects[i+1]
			x1 = rk1.get_x()+rk1.get_width()
			y1 = rk1.get_y()+rk1.get_height()
			x2 = rk2.get_x()+rk2.get_width()
			y2 = rk2.get_y()
			ax.plot([x1,x2],[y1,y2],'k-',linewidth=0.4)
		return 0
	for i in xrange(n):
		if i:
			cumtmp = cumtmp + np.asarray(tmp[i-1,:])[0]
			rects = stackvAX.barh(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,left=cumtmp,align='edge',label=legends[i])
			if not noline:plot_line_h(stackvAX,rects)
		else:
			cumtmp = 0
			rects = stackvAX.barh(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,align='edge',label=legends[i])
			if not noline:plot_line_h(stackvAX,rects)
	stackvAX.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=6,fancybox=True, shadow=True)
	stackvAX.set_ylim(0-(1-width),p)
	#clean_axis(stackvAX)
	#stackvAX.set_ylabel(xlabel)
	#stackvAX.set_yticks(ind)
	#stackvAX.set_yticklabels(xticks_labels,rotation=rotation)
	
	if scale: 
		stackvAX.set_xlim(0,100)
	if nocluster:
		t_annonames = xticks_labels
	else:
		t_annonames = [xticks_labels[i] for i in col_denD['leaves']]
	stackvAX.set_yticks(np.arange(p)+width/2)
	stackvAX.yaxis.set_ticks_position('right')
	stackvAX.set_yticklabels(t_annonames)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0




def stackv_bar_plot(data,xticks_labels,fig_prefix,xlabel,ylabel,title="",width=0.8,legends=[],colors=[],scale=0,rotation=45,orientation="vertical",legendtitle=""):
	"""orientation   is "vertical" or horizontal"""
	n,p = data.shape
	ind = np.arange(p)
	tmp = np.float64(data.copy())
	#tmp = np.cumsum(data,0)
	#print tmp - data
	if scale:
		tmp = tmp/np.sum(tmp,0)*100
		#print tmp
	#tmp = np.cumsum(tmp,0)
	if not colors:
		colors = cm.Dark2(np.linspace(0, 1, n))
	lfsm  = 6
	widsm = 6 
	if len(xticks_labels) > 40:
		lfsm  = int(len(xticks_labels) * 1.0 * 8/40); lfsm = np.min([lfsm,16])
	if orientation == "vertical":
		fig = plt.figure(figsize=(widsm*2,lfsm),dpi=300)
	elif orientation == "horizontal":
		fig = plt.figure(figsize=(widsm*2,lfsm),dpi=300)
	ax = fig.add_subplot(121)
	linewidth = 0
	alpha=1.0
	def plot_line_h(ax,rects):
		for i in xrange(len(rects)-1):
			rk1 = rects[i]
			rk2 = rects[i+1]
			x1 = rk1.get_x()+rk1.get_width()
			y1 = rk1.get_y()+rk1.get_height()
			x2 = rk2.get_x()+rk2.get_width()
			y2 = rk2.get_y()
			ax.plot([x1,x2],[y1,y2],'k-',linewidth=0.4)
		return 0
	def plot_line_v(ax,rects):
		for i in xrange(len(rects)-1):
			rk1 = rects[i]
			rk2 = rects[i+1]
			x1 = rk1.get_y()+ rk1.get_height()
			y1 = rk1.get_x()+rk1.get_width()
			x2 = rk2.get_y()+rk2.get_height()
			y2 = rk2.get_x()
			ax.plot([y1,y2],[x1,x2],'k-',linewidth=0.4)
	for i in xrange(n):
		if i:
			cumtmp = cumtmp + np.asarray(tmp[i-1,:])[0]
			if orientation == "vertical":
				rects = ax.bar(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,bottom=cumtmp,align='center',label=legends[i])
				#for rk in rects:
				#	print "h",rk.get_height()
				#	print "w",rk.get_width()
				#	print "x",rk.get_x()
				#	print "y",rk.get_y()
				#break
				if scale:
					plot_line_v(ax,rects)
			elif orientation == "horizontal":
				rects = ax.barh(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,left=cumtmp,align='center',label=legends[i])
				if scale:
					plot_line_h(ax,rects)
				#for rk in rects:
					#print "h",rk.get_height()
					#print "w",rk.get_width()
					#print "x",rk.get_x()
					#print "y",rk.get_y()
		else:
			cumtmp = 0
			#print ind,np.asarray(tmp[i,:])[0]
			if orientation == "vertical":
				rects = ax.bar(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,align='center',label=legends[i])
				if scale:
					plot_line_v(ax,rects)
			elif orientation == "horizontal":
				rects = ax.barh(ind,np.asarray(tmp[i,:])[0],width,color=colors[i],linewidth=linewidth,alpha=alpha,align='center',label=legends[i])
				if scale:
					plot_line_h(ax,rects)
	#ax.legend(loc=0)
	if orientation == "vertical":
		ax.set_ylabel(ylabel)
		ax.set_xlabel(xlabel)
		ax.set_xticks(ind)
		ax.set_xticklabels(xticks_labels,rotation=rotation,ha="right")
		if scale:
			ax.set_ylim(0,100)
			ax.set_xlim(0-1,p)
	else:
		ax.set_ylabel(xlabel)
		ax.set_xlabel(ylabel)
		ax.set_yticks(ind)
		ax.set_yticklabels(xticks_labels,rotation=rotation)
		if scale:
			ax.set_xlim(0,100)
			ax.set_ylim(0-1,p)
	ax.set_title(title)
	ax.grid(True)
	#ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=6,borderaxespad=0, fancybox=True, shadow=True, handlelength=1.1)
	#ax.legend(loc=0, fancybox=True, bbox_to_anchor=(1.02, 1),borderaxespad=0)
	plt.legend(title=legendtitle,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0


def bar_group(data,group_label,xticklabel,xlabel,ylabel,colors=None,fig_prefix="bar_group",title=None,width=0.3,ylog=0,text_rotation=0):
	num_groups,p = data.shape
	assert num_groups == len(group_label)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.arange(p)
	rects = []
	if colors == None:
		"""
		110 def color_grad(num,colorgrad=cm.Set2):
		111     color_class = cm.Set2(np.linspace(0, 1, num))
		112     return color_class
		"""
		colors = color_grad(num_groups,colorgrad=cm.Dark2)
	for i in xrange(num_groups):
		rect=ax.bar(xlocations+width*i, np.asarray(data)[i,:], width=width,linewidth=0,color=colors[i],ecolor=colors[i],alpha=0.6,label=group_label[i])
		rects.append(rect)
	for rk in rects:
		for rect in rk:
			height = rect.get_height()
			if height < 0.0001:continue
			ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, "%.0f"%float(height),ha='center', va='bottom',fontsize=(8-0),rotation=text_rotation)
	ax.legend(group_label,loc=0)
	ax.set_xticks(xlocations+width/2*num_groups)
	ax.set_xticklabels(xticklabel,ha="right",rotation=45)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if ylog:
		ax.set_yscale("log")
	ax.grid(True)
	if title <> None:ax.set_title(title)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def err_line_group(data,error,group_label,xticklabel,xlabel,ylabel,colors,fig_prefix,title=None):
	num_groups,p = data.shape
	assert num_groups == len(group_label)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.arange(p) + 1
	ret_color,ret_lines,ret_marker = styles(p)

	for i in xrange(num_groups):
		ax.errorbar(xlocations,data[i,:],yerr=error[i,:],marker=ret_marker[i],ms=8,ls='dotted',color=ret_color[i],capsize=5,alpha=0.6,label=group_label[i])
	ax.legend(group_label,loc=0)
	ax.set_xticklabels(xticklabel)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if title <> None:ax.set_title(title)
	fig.tight_layout()
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def bargroup(data,group_label,xticklabel,xlabel,ylabel,colors=None,fig_prefix="test",title=None,width=0.3): # group * xticks 
	num_groups,p = data.shape
	if colors == None:
		colors = styles(len(group_label))[0]
	assert num_groups == len(group_label)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.arange(p)
	for i in xrange(num_groups):
		ax.bar(xlocations+width*i, data[i,:],width=width,linewidth=0,color=colors[i],ecolor=colors[i],alpha=0.6,label=group_label[i])
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=6,borderaxespad=0, fancybox=True, shadow=True)
	ax.set_xticks(xlocations+width/2*num_groups)
	ax.set_xticklabels(xticklabel)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if title <> None:ax.set_title(title)
	fig.tight_layout()
	ax.grid(True)
	fig.tight_layout(rect = [0,0,1,0.9])
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close()
	return 0
	

def err_bar_group(data,error,group_label,xticklabel,xlabel,ylabel,colors=None,fig_prefix="test",title=None,width=0.3):
	num_groups,p = data.shape
	if colors == None:
		colors = color_grad(len(group_label))
	assert num_groups == len(group_label)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.arange(p)
	for i in xrange(num_groups):
		ax.bar(xlocations+width*i, data[i,:],yerr=error[i,:], width=width,linewidth=0,color=colors[i],ecolor=colors[i],alpha=0.6,label=group_label[i])# capsize=5
	#ax.legend(group_label,loc=0)
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=6,borderaxespad=0, fancybox=True, shadow=True)
	ax.set_xticks(xlocations+width/2*num_groups)
	ax.set_xticklabels(xticklabel)
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	if title <> None:ax.set_title(title)
	fig.tight_layout()
	ax.grid(True)
	fig.tight_layout(rect = [0,0,1,0.9])
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0
	
def err_bar(data,error,xlabel,ylabel,fig_prefix,title=None,mark_sig=None,mark_range=[[0,1],],width=0.3):
	num = len(data)
	assert num == len(error) == len(xlabel)
	#colors = cm.Set3(np.linspace(0, 1, len(xlabel)))
	#colors = ["black","gray"]
	if num == 2:
		colors = ["black","gray"]
	colors,ret_lines,ret_marker = styles(num)
	
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.asarray(range(len(data)))+width
	ax.bar(xlocations, data, yerr=error, width=width,linewidth=0.5,ecolor='r',capsize=5,color=colors,alpha=0.5)
	ax.set_xticks(xlocations+width/2)
	ax.set_xticklabels(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_xlim(0, xlocations[-1]+width*2)
	if title <> None:ax.set_title(title)
	if mark_sig <> None:
		xlocations = xlocations+width/2
		ybin = np.max(np.asarray(data)+np.asarray(error))
		step = ybin/20
		offset = ybin/40
		assert len(mark_sig) == len(mark_range)
		for i in xrange(len(mark_range)):
			mark_r = mark_range[i]
			sig_string = mark_sig[i]
			xbin = np.asarray(mark_r)
			ybin += step
			ax.plot([xlocations[mark_r[0]],xlocations[mark_r[1]]],[ybin,ybin],color='gray',linestyle='-',alpha=0.5)
			ax.text((xlocations[mark_r[0]]+xlocations[mark_r[1]])/2,ybin,sig_string)
		ax.set_ylim(0,ybin+step*2.5)
	ax.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def trendsiglabel(Xvec,Yvec,meansdata,totmean,color,xticklabel,fig_prefix="trend",rotation=45):
	num = len(Xvec)
	ngenes_sig,p = meansdata.shape
	ngenes_tot,p = totmean.shape
	assert num == len(Yvec) == len(xticklabel) == p
	
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	#ax.plot(Xvec,Yvec,color+'^-',markeredgecolor='None',markersize = 12)
	for i in xrange(ngenes_tot):
		#print i
		ax.plot(Xvec,totmean[i,:],'g-',lw=0.5,alpha=0.3)
	for i in xrange(ngenes_sig):
		ax.plot(Xvec,meansdata[i,:],'b-',lw=0.5,alpha=0.3)
	ax.plot(Xvec,Yvec,color+'^-',markeredgecolor=color,markersize = 5)
	ax.set_xticks(np.arange(num))
	xlabelsL = ax.set_xticklabels(xticklabel,rotation=rotation)
	ax.grid(True)
	#clean y
	#ax.get_yaxis().set_ticks([])
	#min_a = np.min(Yvec)
	#max_a = np.max(Yvec)
	#ax.set_ylim(min_a-1,max_a+1)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def twofactor_diff_plot(Xmeanarr,Xstdarr,xticklabel,fig_prefix="Sigplot",title=None,xlabel=None,ylabel="Expression",width=0.3,labels=None,ylimmin=-0.5):
	num = Xmeanarr.shape[-1]
	fmts = ['o-','^--','x-.','s--','v-.','+-.']
	ecolors = ['r','b','g','c','m','y','k']
	assert num == Xstdarr.shape[-1] == len(xticklabel)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.asarray(range(num))+width
	n,p = Xmeanarr.shape
	for i in xrange(n):
		ax.errorbar(xlocations, Xmeanarr[i,:], yerr=Xstdarr[i,:],fmt=fmts[i],ecolor=ecolors[i],markeredgecolor=ecolors[i])
	if labels:
		ax.legend(labels,loc=0,numpoints=1)
	ax.set_xticks(xlocations)
	ax.set_xticklabels(xticklabel)
	ax.set_ylabel(ylabel)
	if xlabel: ax.set_xlabel(xlabel)
	ax.set_xlim(0, xlocations[-1]+width*2)
	#ax.set_ylim(bottom=ylimmin)
	if title <> None:ax.set_title(title)
	ax.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def onefactor_diff_plot(Xmeanarr,Xstdarr,xticklabel,fig_prefix="Sigplot",title=None,xlabel=None,ylabel="Expression",width=0.3):
	num = len(Xmeanarr)
	assert num == len(Xstdarr) == len(xticklabel)
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	xlocations = np.asarray(range(len(Xmeanarr)))+width
	ax.errorbar(xlocations, Xmeanarr, yerr=Xstdarr,fmt='o-',ecolor='r')
	ax.set_xticks(xlocations)
	ax.set_xticklabels(xticklabel)
	ax.set_ylabel(ylabel)
	if xlabel: ax.set_xlabel(xlabel)
	ax.set_xlim(0, xlocations[-1]+width*2)
	if title <> None:ax.set_title(title)
	ax.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def bar_plot(data,xticks_labels,fig_prefix,xlabel,ylabel,title="",width=0.3,rotation=0,fmt='%.2f',ylog=0,colors=None):
	ind = np.arange(len(data))
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if ylog:
		ax.set_yscale("log",nonposy='clip')
	linewidth = 0
	alpha=0.5
	if not colors:
		colors = 'k'
	rects = ax.bar(ind,data,width,color=colors,linewidth=linewidth,alpha=alpha,align='center')
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	ax.set_xticks(ind)
	ax.yaxis.grid(True)
	#ax.set_xticks(ind+width/2)
	if rotation == 0 or rotation == 90:hafmt='center'
	else:hafmt = 'right'
	xlabelsL = ax.set_xticklabels(xticks_labels,ha=hafmt,rotation=rotation)
	#rotate labels 90 degrees
	if rotation:
		for label in xlabelsL:
			label.set_rotation(rotation)
	ax.set_title(title)
	for rect in rects:
		height = rect.get_height()
		if height < 0.1:continue
		ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, fmt%float(height),ha='center', va='bottom',fontsize=8)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def MA_vaco_plot(avelogFC,logFC,totavelogFC,totlogFC,fig_prefix,xlabel,ylabel,title="MAplot"):
	fig = plt.figure(figsize=(5,4),dpi=300)
	ax = fig.add_subplot(111)
	ax.plot(avelogFC,logFC,'ro',markersize = 5,alpha=0.5,markeredgecolor='r')
	ax.plot(totavelogFC,totlogFC,'bo',markersize = 3,alpha=0.5,markeredgecolor='b')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(title)
	ax.grid(True)
	fig.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def vaco_plot(X,Y,Xcut,Ycut,fig_prefix,xlabel,ylabel,title=None):
	# X is rho or fc
	Xcutx = [np.min(X),np.max(X)]
	Ycuts = [Ycut,Ycut]
	idx1 = (Y > Ycut) & (np.abs(X) > Xcut)
	idx2 = ~idx1
	fig = plt.figure(figsize=(5,4),dpi=300)
	ax = fig.add_subplot(111)
	ax.plot(X[idx1],Y[idx1],'ro',markersize = 5,alpha=0.5,markeredgecolor='None')
	ax.plot(X[idx2],Y[idx2],'bo',markersize = 5,alpha=0.5,markeredgecolor='None')
	ax.plot(Xcutx,Ycuts,'r--')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	#ax.set_xlim(-6,6)
	if title != None:
		ax.set_title(title)
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def baohedu_plot(genes,reads,samples,fig_prefix,xlabel="number of reads",ylabel="number of detected genes",title=None,lim=0):
	n1,p1 = genes.shape
	n2,p2 = reads.shape
	assert n1==n2 and p1==p2
	"saturability"
	#types = ['ro-','b^--','gs-.','kv:','c^-.','m*--','yp:']
	ret_color,ret_lines,ret_marker = styles(n1)
	fig = plt.figure(figsize=(8,6),dpi=300)
	ax = fig.add_subplot(111)
	for i in xrange(n1):
		x = reads[i,:]
		y = genes[i,:]
		ax.plot(x,y,color=ret_color[i],linestyle=ret_lines[i],marker=ret_marker[i],markeredgecolor=ret_color[i],markersize = 4,alpha=0.7,label=samples[i])
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if title != None: ax.set_title(title)
	ax.legend(loc=0,numpoints=1)
	ax.grid(True)
	ax.set_ylim(bottom=0)
	if lim:
		ax.set_xlim(-1,101)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.tight_layout()
	plt.clf()
	plt.close()
	return 0

def plotyy(Xvector,Y1np,Y2np,fig_prefix,xlabel,ylabel1,ylabel2,title=None):
	Y1np = np.asarray(Y1np)
	Y2np = np.asarray(Y2np)
	fig = plt.figure(figsize=(10,8),dpi=300)
	ax1 = fig.add_subplot(111)
	try:
		n1,p1 = Y1np.shape
	except ValueError:
		n1 = 1
	try:
		n2,p2 = Y2np.shape
	except ValueError:
		n2 = 1
	for i in xrange(n1):
		if n1 == 1:
			ax1.plot(Xvector,Y1np, 'b-')
			break
		if i == 0:
			ax1.plot(Xvector,Y1np[i,:], 'b-')
		else:
			ax1.plot(Xvector,Y1np[i,:], 'b--')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel1, color='b')
	if title: ax1.set_title(title)
	for tl in ax1.get_yticklabels():
		tl.set_color('b')
	ax2 = ax1.twinx()
	for i in xrange(n2):
		if n2 == 1:
			ax2.plot(Xvector,Y2np, 'r-')
			break
		if i == 0:
			ax2.plot(Xvector,Y2np[i,:], 'r-')
		else:
			ax2.plot(Xvector,Y2np[i,:], 'r-.')
	ax2.set_ylabel(ylabel2, color='r')
	for tl in ax2.get_yticklabels():
		tl.set_color('r')
	ax1.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def clean_axis(ax):
	"""Remove ticks, tick labels, and frame from axis"""
	ax.get_xaxis().set_ticks([])
	ax.get_yaxis().set_ticks([])
	for spx in ax.spines.values():
		spx.set_visible(False)
def density_plt(Xarr,colors,legendlabel,figname_prefix="density",xlabel=None,ylabel=None,fun="pdf",fill=0,title=None,exclude=0.0,xlog=0,xliml=None,xlimr=None):
	"""not at the same scale  """
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	n = len(Xarr)
	assert len(colors) == len(legendlabel)
	for i in xrange(n):
		dat = np.asarray(Xarr[i])
		xp,yp = kdensity(dat[dat <> exclude],num = 400,fun=fun)
		ax.plot(xp,yp,colors[i],label=legendlabel[i],markeredgecolor='None')
		if fill:
			ax.fill_between(xp,yp,y2=0,color=colors[i],alpha=0.2)
	ax.legend(loc=0,numpoints=1)
	if xliml <> None:
		ax.set_xlim(left = xliml)
	if xlimr <> None:
		ax.set_xlim(right = xlimr)
	#if xliml and xlimr:
	#	print "get"
	#	ax.set_xlim((xliml,xlimr))
	if xlog:
		ax.set_xscale("log")
	if xlabel: ax.set_xlabel(xlabel)
	if ylabel: ax.set_ylabel(ylabel)
	if title:  ax.set_title(title)
	ax.grid(True)
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0
def exprs_density(Xnp,colors,classlabels,figname_prefix="out",xlabel=None,ylabel=None,fun="cdf",exclude=0.0,ylim=10):
	n,p = Xnp.shape
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	uniq_colors = []
	for tmpcolor in colors:
		if tmpcolor not in uniq_colors:
			uniq_colors.append(tmpcolor)

	idx = [colors.index(color) for color in uniq_colors]
	labels = [classlabels[i] for i in idx]
	for i in idx:
		dat = np.asarray(Xnp[i,:])
		if fun == "cdf":
			xp,yp = kdensity(dat[dat <> exclude],fun="cdf")
		elif fun == "pdf":
			xp,yp = kdensity(dat[dat <> exclude],fun="pdf")	
		ax.plot(xp,yp,colors[i])
	ax.legend(labels,loc=0)
	for i in xrange(n):
		dat = np.asarray(Xnp[i,:])
		if fun == "cdf":
			xp,yp = kdensity(dat[dat <> exclude],fun="cdf")
		elif fun == "pdf":
			xp,yp = kdensity(dat[dat <> exclude],fun="pdf")
		ax.plot(xp,yp,colors[i])
		#print xp
		#print yp
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.grid(True)
	if ylim:
		ax.set_xlim(0,ylim)
	fig.tight_layout()
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0



def hist_groups(data,labels,xlabel,fig_prefix,bins=25,alpha=0.7,normed=True,colors=None,rwidth=1,histtype="stepfilled",linewidth=0.5,xlim=(0,10000)):
	"""
	histtype='bar', rwidth=0.8
	stepfilled
	"""
	n = len(data)
	assert n == len(labels)
	if not colors:
		if n >7:
			colors = cm.Accent(np.linspace(0, 1,n))
		else:
			colors = plt.rcParams['axes.color_cycle'][0:n]
	if normed:ylabel = "Density"
	else:ylabel = "Frequency"
	fig = plt.figure(dpi=300)
	ax = fig.add_subplot(111)
	for i in xrange(n):
		xp,yp = kdensity(data[i],fun="pdf")
		ax.hist(data[i],histtype=histtype,rwidth=rwidth,linewidth=linewidth,bins=bins, alpha=alpha,normed=normed,label=labels[i],color=colors[n-i-1])
		ax.plot(xp,yp,color=colors[n-i-1],linestyle='--',lw=1.0)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.legend(loc=0)
	if xlim:
		ax.set_xlim(xlim[0],xlim[1])
	ax.grid(True)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def exprs_RLE(Xnp,mean="median",fig_prefix=None,samplenames=None,colors=None):
	###!!!!用median 保持robust
	#在同一组实验中，即使是相互比较的对照组与实验组之间，大部分基因的表达量还是应该保持一致的，何况平行实验之间。当我们使用相对对数表达（Relative Log Expression(RLE)）的的箱线图来控制不同组之间的实验质量时，我们会期待箱线图应该在垂直中央相类的位置（通常非常接近0）。如果有一个芯片的表现和其它的平行组都很不同，那说明它可能出现了质量问题。
	n,p = Xnp.shape
	if mean == "median":
		Xmean =np.median(Xnp,axis=0)	
	elif mean == "mean":
		Xmean =np.mean(Xnp,axis=0)
	plot_boxplot(Xnp-Xmean,fig_prefix,"","Relative Log Expression",samplenames,colors=colors,ylim=0)
	
	return 0

def exprs_NUSE():
	#1. hist 
	#2. julei 
	#3. RLE
	#array corr
	#
	#相对标准差（Normalized Unscaled Standard Errors(NUSE)）
	#是一种比RLE更为敏感 的质量检测手段。如果你在RLE图当中对某组芯片的质量表示怀疑，那当你使用NUSE图时，这种怀疑就很容易被确定下来。NUSE的计算其实也很简单，它是某芯片基因标准差相对于全组标准差的比值。我们期待全组芯片都是质量可靠的话，那么，它们的标准差会十分接近，于是它们的NUSE值就会都在1左右。然而，如果有实验芯片质量有问题的话，它就会严重的偏离1，进而影响其它芯片的NUSE值偏向相反的方向。当然，还有一种非常极端的情况，那就是大部分芯片都有质量问题，但是它们的标准差却比较接近，反而会显得没有质量问题的芯片的NUSE值会明显偏离1，所以我们必须结合RLE及NUSE两个图来得出正确的结论
	return 0

from itertools import izip
def show_values(pc, fmt="%.3f", **kw):
	pc.update_scalarmappable()
	ax = pc.get_axes()
	for p, color, value in izip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
		x, y = p.vertices[:-2, :].mean(0)
		if np.all(color[:3] > 0.5):
			color = (0.0, 0.0, 0.0)
		else:
			color = (1.0, 1.0, 1.0)
		ax.text(x, y, fmt % value, ha="center", va="center", color=color)

def pcolor_plot(Xnp,xsamplenames,ylabelnames,figname_prefix,txtfmt = "%.3f"):
	n,p = Xnp.shape
	fig = plt.figure(figsize=(8,6),dpi=300)
	ax = fig.add_subplot(111)
	clean_axis(ax)
	cplot = ax.pcolor(Xnp, edgecolors='k', linestyle= 'dashed', linewidths=0.2, cmap = cm.coolwarm)
	ax.set_yticks(np.arange(p)+ 0.5)
	ax.set_yticklabels(ylabelnames)
	ax.set_xticks(np.arange(n)+0.5)
	xlabelsL = ax.set_xticklabels(xsamplenames)
	for label in xlabelsL:
		label.set_rotation(90)
	cb = fig.colorbar(cplot,ax=ax)
	cb.set_label("correlation")
	cb.outline.set_linewidth(0)
	ax.grid(visible=False)
	show_values(cplot,fmt=txtfmt)
	#fig.tight_layout()
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0
def exprs_corrarray(Xnp,samplenames,figname_prefix,txtfmt = "%.3f",plottext=1,Xdist=None,cbarlabel = "correlation"):
	"""
	def show_values(pc, fmt="%.3f", **kw):
		from itertools import izip
		pc.update_scalarmappable()
		ax = pc.get_axes()
		for p, color, value in izip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
			x, y = p.vertices[:-2, :].mean(0)
			if np.all(color[:3] > 0.5):
				color = (0.0, 0.0, 0.0)
			else:
				color = (1.0, 1.0, 1.0)
			ax.text(x, y, fmt % value, ha="center", va="center", color=color, **kw)
	"""
	if type(Xdist) == type(None):
		corr_coef = np.abs(np.corrcoef(Xnp))
	else:
		corr_coef = Xdist
	n,p = corr_coef.shape
	fig = plt.figure(figsize=(14,12),dpi=300)
	ax = fig.add_subplot(111)
	clean_axis(ax)
	
	cplot = ax.pcolor(corr_coef, edgecolors='k', linestyle= 'dashed', linewidths=0.2, cmap = 'RdBu_r')
	#image_instance = ax.imshow(corr_coef,interpolation='nearest',aspect='auto',alpha=0.8,origin='lower',cmap=cm.coolwarm)
	
	ax.set_yticks(np.arange(p)+ 0.5)
	ax.set_yticklabels(samplenames)
	ax.set_xticks(np.arange(n)+0.5)
	xlabelsL = ax.set_xticklabels(samplenames)
	
	for label in xlabelsL:
		label.set_rotation(90)
	cb = fig.colorbar(cplot,ax=ax)
	cb.set_label(cbarlabel)
	cb.outline.set_linewidth(0)
	ax.grid(visible=False)
	if plottext:
		show_values(cplot,fmt=txtfmt)
	fig.tight_layout()
	plt.savefig(figname_prefix+".png",format='png',dpi=300)
	plt.savefig(figname_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return corr_coef

def pie_plot(sizes,labels,fig_prefix="pie_plot",autopct='%1.1f%%',colors=None,explode=None,shadow=False, startangle=90,radius=1):
	fig = plt.figure(figsize=(6,6),dpi=300)
	ax5 = fig.add_subplot(111)
	if not colors:
		colors = cm.Paired(np.linspace(0, 1, len(labels)))
	#patches, texts, autotexts = ax5.pie(sizes,explode,labels=labels, colors=colors,autopct=autopct, shadow=shadow, startangle=startangle,radius=radius)
	patches, texts = ax5.pie(sizes,explode,colors=colors, shadow=shadow, startangle=startangle,radius=radius)
	tmplabels = []
	total = sum(sizes)
	for i in xrange(len(labels)):
		lable = labels[i]
		size = float(sizes[i])/total*100
		#print lable+"("+ autopct+")"
		tmplabels.append((lable+"("+ autopct+")")%size)
	ax5.legend(patches,tmplabels,loc='best')
	for w in patches:
		w.set_linewidth(0.2)
		w.set_edgecolor('white')
	##plt.legend(patches, labels, loc="best")
	#proptease = fm.FontProperties()
	#proptease.set_size('xx-small')
	#plt.setp(autotexts, fontproperties=proptease)
	#plt.setp(texts, fontproperties=proptease)
	plt.axis('equal')
	plt.tight_layout()
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0


def cluster_heatmap_dist(Xdist,samplenames,fig_prefix="test_cluster_heatmap",colornorm = True,nosample=False,plotxlabel=1,plotylabel=1,cbarlabel="scaled measures",usepcolor=0,cmcolor="autumn"):
	n,p = Xdist.shape
	assert n == p
	assert np.sum(np.isnan(Xdist)) == 0
	if colornorm:
		vmin = np.floor(np.min(Xdist))
		vmax = np.ceil(np.max(Xdist))
		vmax = max([vmax,abs(vmin)])
		my_norm = mpl.colors.Normalize(vmin, vmax)
	else:my_norm = None

	lfsm = 8	
	if len(samplenames) > 20:
		lfsm  = int(len(samplenames) * 1.0 * 8/40); lfsm = np.min([lfsm,16])
	sys.stderr.write("[INFO] plot size is %dX%d\n"%(lfsm,lfsm))
	fig = plt.figure(figsize=(lfsm,lfsm))
	heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[0.15,1],height_ratios=[0.15,1])
	if not nosample:
		col_clusters = linkage(Xdist,method='average')
		col_denAX = fig.add_subplot(heatmapGS[0,1])
		sch.set_link_color_palette(['black'])
		col_denD = dendrogram(col_clusters,color_threshold=np.inf,) # use color_threshold=np.inf not to show color
		col_denAX.set_axis_off()
	heatmapAX = fig.add_subplot(heatmapGS[1,1])
	if nosample:pass
	else:
		Xtmp = Xdist[:,col_denD['leaves']]
		Xtmp = Xtmp[col_denD['leaves'],:]
	clean_axis(heatmapAX)
	if not usepcolor:
		axi = heatmapAX.imshow(Xtmp,interpolation='nearest',aspect='auto',origin='lower',norm=my_norm,cmap = cmcolor)
	else:
		axi = heatmapAX.pcolor(np.asarray(Xtmp), edgecolors='k', linestyle= 'dashdot', linewidths=0.2, cmap = cmcolor) # cmap = cm.coolwarm
	if plotxlabel:
		if not nosample:
			t_samplenames = [samplenames[i] for i in col_denD['leaves']]
		else:
			t_samplenames = samplenames 
		heatmapAX.set_xticks(np.arange(n)+0.5)
		xlabelsL = heatmapAX.set_xticklabels(t_samplenames)
		for label in xlabelsL:
			label.set_rotation(90)
		for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines():
			l.set_markersize(0)
	#heatmapAX.grid()
	scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,1,subplot_spec=heatmapGS[1,0],wspace=0.0,hspace=0.0)
	scale_cbAX = fig.add_subplot(scale_cbGSSS[0,0])
	scale_cbAX.set_axis_off()
	cb = fig.colorbar(axi,ax=scale_cbAX,shrink=0.6,fraction=0.6)
	font = {'size': 10}
	tl = cb.set_label(cbarlabel,fontdict=font)
	cb.ax.yaxis.set_ticks_position('right')
	cb.ax.yaxis.set_label_position('right')
	cb.outline.set_linewidth(0)
	tl = cb.set_label(cbarlabel,fontdict=font)
	tickL = cb.ax.yaxis.get_ticklabels() 
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 2) 
	fig.tight_layout()	
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0 
	
def highfreq_mutmap(topgenesmuted,mut_stack,samplenames,annonames,fig_prefix="test_cluster_muted",colornorm=True,nosample=False,nogene=False,plotxlabel= 1,plotylabel=1,cbarlabel="Mutation Frequency",genecolors=None,samplecolors=None,cmap='RdYlBu_r',tree=3,stacklegends=[],colorbarlabels=[]):
	Xnp = topgenesmuted
	n,p = Xnp.shape
	assert n == len(samplenames) and p == len(annonames)
	if colornorm:
		vmin = np.floor(np.min(Xnp))
		vmax = np.ceil(np.max(Xnp))
		vmax = max([vmax,abs(vmin)])
		my_norm = mpl.colors.Normalize(vmin, vmax)
	else:my_norm = None
	if len(samplenames)/3 <=9:rightx = 8
	else:rightx = len(samplenames)/3
	if len(annonames)/5 <=9: leftx = 8
	else:
		leftx = int(len(annonames)/4.5)
	if len(samplenames) > 80:
		rightx = 8;plotxlabel = 0
	if len(annonames) > 80:
		leftx = 8;plotylabel = 0
	leftx = min(int(32700/300.0),leftx)
	rightx = min(int(32700/300.0),rightx)
	fig = plt.figure(figsize=(rightx,leftx))
	sys.stderr.write("[INFO] plot size is %dX%d\n"%(leftx,rightx))
	width_ratios = [0.07,0.115,1];height_ratios=[0.15,1]
	samples_l = 3; genes_l = 2;
	if type(samplecolors) <> type(None): 
		samples_l += 1
		width_ratios = [0.07,0.115,0.05,1]
	if type(genecolors) <> type(None): 
		genes_l = 3
		height_ratios = [0.1,0.05,1]
	heatmapGS = gridspec.GridSpec(samples_l,genes_l,wspace=0.0,hspace=0.0,width_ratios=height_ratios,height_ratios=width_ratios)
	Xtmp = Xnp.T.copy()
	if not nosample:
		col_pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(Xnp))
		col_clusters = linkage(col_pairwise_dists,method='average')
		#cutted_trees = cut_tree(col_clusters)
		col_denAX = fig.add_subplot(heatmapGS[0,genes_l-1])
		col_denD = dendrogram(col_clusters)
		col_denAX.set_axis_off()
		Xtmp = Xtmp[:,col_denD['leaves']]
	if not nogene:
		row_pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(Xtmp))
		row_clusters = linkage(row_pairwise_dists,method='average')
		#assignments = fcluster(row_clusters, cut_tree, 'distance')
		#row_cluster_output = pandas.DataFrame({'team':annonames, 'cluster':assignments})
		row_denAX = fig.add_subplot(heatmapGS[samples_l-1,0])
		row_denD = dendrogram(row_clusters,orientation='left')
		row_denAX.set_axis_off()
		Xtmp = Xtmp[row_denD['leaves'],:]
	# stack plot:
	stackvAX = fig.add_subplot(heatmapGS[1,genes_l-1])
	mut_stack = np.asmatrix(mut_stack)
	stackn,stackp = mut_stack.shape
	stackcolors = color_grad(3,cm.Dark2)
	#mut_stackT = mut_stack.T
	if not nosample: mut_stack = mut_stack[col_denD['leaves'],:]
	ind = np.arange(stackn)
	for i in xrange(stackp):
		if i:
			cumtmp = cumtmp + np.asarray(mut_stack[:,i-1].T)[0]
			rects = stackvAX.bar(ind,np.asarray(mut_stack[:,i].T)[0],0.6,color=stackcolors[i],linewidth=0,alpha=0.7,align='center',bottom=cumtmp,label=stacklegends[i])
		else:
			cumtmp = 0
			rects = stackvAX.bar(ind,np.asarray(mut_stack[:,i].T)[0],0.6,color=stackcolors[i],linewidth=0,alpha=0.7,align='center',label=stacklegends[i])
	# ax.legend(alx,bbox_to_anchor=(1.02, 1),loc=0,borderaxespad=0,numpoints=1,fontsize=6)
	stackvAX.legend(loc=0, fancybox=True, bbox_to_anchor=(1.02, 1),borderaxespad=0)
	stackvAX.set_ylabel("Mutations")
	stackvAX.set_xlim(-0.5,stackn-0.5)
	heatmapAX = fig.add_subplot(heatmapGS[samples_l-1,genes_l-1])
	if samplecolors <> None:
		if not nosample:
			tmpxxx = []
			for x in col_denD['leaves']:
				tmpxxx.append(samplecolors[x])
			samplecolors = tmpxxx[:]
			del tmpxxx
		col_cbAX = fig.add_subplot(heatmapGS[2,genes_l-1])
		col_axi = col_cbAX.imshow([list(samplecolors)],interpolation='nearest',aspect='auto',origin='lower')
		clean_axis(col_cbAX)
	if genecolors <> None:
		if not nogene:
			genecolors   = genecolors[row_denD['leaves']]
		row_cbAX = fig.add_subplot(heatmapGS[samples_l-1,1])
		row_axi = row_cbAX.imshow([genecolors.tolist(),],interpolation='nearest',aspect='auto',origin='lower')
		clean_axis(row_cbAX)
	# cmap = 'RdBu_r'
	#tmpmap = cm.Set2()
	axi = heatmapAX.pcolor(Xtmp,edgecolors='w', linewidths=1,cmap="Set2")
	#axi = heatmapAX.imshow(Xtmp,interpolation='nearest',aspect='auto',origin='lower',norm=my_norm,cmap = cmap)
	clean_axis(heatmapAX)

	if plotylabel:
		if not nogene:
			t_annonames = [annonames[i] for i in row_denD['leaves']]
		else:
			t_annonames = annonames
		heatmapAX.set_yticks(np.arange(p)+0.5)
		heatmapAX.yaxis.set_ticks_position('right')
		heatmapAX.set_yticklabels(t_annonames)
	if plotxlabel:
		if not nosample:
			t_samplenames = [samplenames[i] for i in col_denD['leaves']]
		else:
			t_samplenames = samplenames
		heatmapAX.set_xticks(np.arange(n)+0.5)
		xlabelsL = heatmapAX.set_xticklabels(t_samplenames)
		for label in xlabelsL:
			label.set_rotation(90)
		for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines():
			l.set_markersize(0)
	heatmapAX.grid(False)
	#scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,1,subplot_spec=heatmapGS[samples_l-1,0],wspace=0.0,hspace=0.0)
	scale_cbAX = fig.add_subplot(heatmapGS[samples_l-1,0])
	scale_cbAX.set_axis_off()
	cb = fig.colorbar(axi,ax=scale_cbAX,fraction=0.5,shrink=0.6)
	font = {'size': 8}
	#tl = cb.set_label(cbarlabel,fontdict=font)
	cb.ax.yaxis.set_ticks_position('left')
	cb.ax.yaxis.set_label_position('left')
	#cb.outline.set_linewidth(0)
	#tickL = cb.ax.yaxis.get_ticklabels()
	cb.set_ticks(np.arange(len(colorbarlabels)))
	cb.set_ticklabels(colorbarlabels)
	#for t in tickL:
	#	t.set_fontsize(t.get_fontsize() - 7)
	fig.subplots_adjust(bottom = 0)
	fig.subplots_adjust(top = 1)
	fig.subplots_adjust(right = 1)
	fig.subplots_adjust(left = 0)
	plt.savefig(fig_prefix+".png",format='png',additional_artists=fig,bbox_inches="tight",dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',additional_artists=fig,bbox_inches="tight",dpi=300)
	plt.clf()
	plt.close()

	return 0

def plot_contest(data,ynames,xlabel=None,ylabel=None,fig_prefix="plot_ContEst"):
	"""
	data = [[mean,low,up],...]
	"""
	meandat = []; lowdat = []; updat = []; rangedat = []; num = len(data); yoffset = []
	for i in xrange(num):
		meandat.append(data[i][0]); lowdat.append(data[i][1]); updat.append(data[i][2]); yoffset.append(i+1); rangedat.append(data[i][2]-data[i][1])
	if num < 25: heightsize = 6
	else: heightsize = int(num * 1.0 * 6/30)
	widthsize = 6
	fig = plt.figure(figsize=(widthsize,heightsize))
	ax = fig.add_subplot(111)
	ax.errorbar(meandat,yoffset,xerr=rangedat,ls="none", marker='o',color='r',markersize=6,markeredgecolor='None')
	
	yoffset.append(num+1)
	yoffset.insert(0,0)
	# ls='',markerfacecolor=tmpcolor,marker=tmpmarker,label=tmplabel,markeredgecolor = tmpcolor,alpha=0.7
	ax.plot([1.5,1.5],[0,yoffset[-1]],ls='--',markerfacecolor=u'#E24A33',markeredgecolor = u'#E24A33', alpha=0.7)
	ax.plot([5,5],[0,yoffset[-1]],ls='--',markerfacecolor=u'#988ED5',markeredgecolor = u'#988ED5', alpha=0.7)
	#ax.plot([1.5,1.5],[yoffset,yoffset],ls='--',markerfacecolor=u'#E24A33',markeredgecolor = u'#E24A33', alpha=0.7)
	#ax.fill_betweenx(yoffset,0,1.5,color=u'#E24A33',alpha=0.3)
	#ax.fill_betweenx(yoffset,1.5,5,color=u'#348ABD',alpha=0.3)
	#ax.fill_betweenx(yoffset,5,np.max(updat)+1,color=u'#988ED5',alpha=0.3)
	
	ax.set_yticks(np.arange(1,num+1))
	ax.yaxis.set_ticks_position('left')
	ax.set_yticklabels(ynames)
	ax.grid(True)
	ax.set_ylim(0,num+1)
	ax.set_xlim(0,np.max(updat)+1)
	if xlabel <> None: ax.set_xlabel(xlabel)	
	if ylabel <> None: ax.set_ylabel(ylabel)
	plt.savefig(fig_prefix+".png",format='png',dpi=300)
	plt.savefig(fig_prefix+".svg",format='svg',dpi=300)
	plt.clf();plt.close();
	return 0

def cluster_heatmap(Xnp,samplenames,annonames,fig_prefix="test_cluster_heatmap",colornorm = True,nosample=False,nogene=False,plotxlabel=1,plotylabel=1,cbarlabel="Expression",genecolors=None,samplecolors=None,cmap='RdYlBu_r', trees = 3,numshow=80,metric="euclidean"):
	n,p = Xnp.shape
	#print n,p,len(samplenames),len(annonames)
	assert n == len(samplenames) and p == len(annonames)
	# make norm
	if colornorm:
		vmin = np.floor(np.min(Xnp))
		vmax = np.ceil(np.max(Xnp))
		vmax = max([vmax,abs(vmin)]) # choose larger of vmin and vmax
		#vmin = vmax * -1
		my_norm = mpl.colors.Normalize(vmin, vmax)
	else:my_norm = None
	# heatmap with row names
	if len(samplenames)/3 <=9:
		rightx = 8
	else:
		rightx = len(samplenames)/3
	if len(annonames)/3 <=9:
		leftx = 8
	else:
		leftx = int(len(annonames)/4.5)
	if len(samplenames) > numshow:
		rightx = 8
		plotxlabel = 0
	if len(annonames) > numshow:
		leftx = 8
		plotylabel = 0
	#import pdb; pdb.set_trace()
	leftx = min(int(32700/300.0),leftx)
	rightx = min(int(32700/300.0),rightx)
	sys.stderr.write("[INFO] plot size is %dX%d\n"%(leftx,rightx))
	fig = plt.figure(figsize=(rightx,leftx))
	samples_l = 2; genes_l = 2;
	width_ratios = [0.15,1];height_ratios=[0.15,1]
	if type(samplecolors) <> type(None): 
		samples_l= 3
		width_ratios = [0.15,0.05,1]
	if type(genecolors) <> type(None) or (not nogene): 
		genes_l = 5
		height_ratios = [0.15,0.015,0.025,0.015,1]

	heatmapGS = gridspec.GridSpec(samples_l,genes_l,wspace=0.0,hspace=0.0,width_ratios=height_ratios,height_ratios=width_ratios)
	### col dendrogram ### col is sample cluster
	#import pdb; pdb.set_trace()
	if not nosample and n >1:
		col_pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(Xnp,metric)) # 'correlation'
		col_clusters = linkage(col_pairwise_dists,method='average')#ward, average

		assignments = cut_tree(col_clusters,[trees,])
		col_cluster_output = pandas.DataFrame({'team': samplenames, 'cluster':assignments.T[0]})
		#print col_cluster_output
		
		col_denAX = fig.add_subplot(heatmapGS[0,genes_l-1])
		col_denD = dendrogram(col_clusters)
		col_denAX.set_axis_off()
	###  fcluster(col_clusters,0.7*max(col_clusters[:,2]),'distance') 
	###  to return the index of each sample for each cluster
	
	### row dendrogram ### row is anno cluster
	if not nogene and p > 1:
		row_pairwise_dists = sp.spatial.distance.squareform(sp.spatial.distance.pdist(Xnp.T,metric))
		row_clusters = linkage(row_pairwise_dists,method='average')

		assignments = cut_tree(row_clusters,[trees,])
		row_cluster_output = pandas.DataFrame({'team':annonames, 'cluster':assignments.T[0]})
		#print row_cluster_output
		numbergenescluter = len(set(assignments.T[0].tolist()))
		row_denAX = fig.add_subplot(heatmapGS[samples_l-1,0])
		row_denD = dendrogram(row_clusters,orientation='left')
		row_denAX.set_axis_off()
	### heatmap ####
	heatmapAX = fig.add_subplot(heatmapGS[samples_l-1,genes_l-1])
	if nogene:
		Xtmp = Xnp.T.copy()
	else:
		Xtmp = Xnp.T[row_denD['leaves'],:]
	if nosample:
		pass
	else:
		Xtmp = Xtmp[:,col_denD['leaves']]

	if samplecolors <> None:
		if not nosample:
			tmpxxx = []
			for x in col_denD['leaves']:
				tmpxxx.append(samplecolors[x])
			samplecolors = tmpxxx[:]
			del tmpxxx
		col_cbAX = fig.add_subplot(heatmapGS[1,genes_l-1])
		col_axi = col_cbAX.imshow([list(samplecolors)],interpolation='nearest',aspect='auto',origin='lower')
		clean_axis(col_cbAX)
	if genecolors <> None or (not nogene):
		if not nogene:
			uniqgenecolors = color_grad(numbergenescluter,colorgrad=cm.Set3)
			genecolors = [i for i in assignments.T[0]]
			#print genecolors
			genecolors   = np.asarray(genecolors)[row_denD['leaves']]
			#print genecolors
		row_cbAX = fig.add_subplot(heatmapGS[samples_l-1,2])
		row_axi = row_cbAX.imshow(np.asarray([genecolors.tolist(),]).T,interpolation='nearest',aspect='auto',origin='lower',alpha=0.6)
		clean_axis(row_cbAX)

	axi = heatmapAX.imshow(Xtmp,interpolation='nearest',aspect='auto',origin='lower',norm=my_norm,cmap = cmap)## 'RdBu_r'  'RdYlGn_r'
	clean_axis(heatmapAX)
	## row labels ##
	if plotylabel:
		if not nogene:
			t_annonames = [annonames[i] for i in row_denD['leaves']]
		else:
			t_annonames = annonames
		heatmapAX.set_yticks(np.arange(p))
		heatmapAX.yaxis.set_ticks_position('right')
		heatmapAX.set_yticklabels(t_annonames)
	## col labels ##
	if plotxlabel:
		if not nosample:
			t_samplenames = [samplenames[i] for i in col_denD['leaves']]
		else:
			t_samplenames = samplenames
		heatmapAX.set_xticks(np.arange(n))
	
		xlabelsL = heatmapAX.set_xticklabels(t_samplenames)
		#rotate labels 90 degrees
		for label in xlabelsL:
			label.set_rotation(90)
		#remove the tick lines
		for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines():
			l.set_markersize(0)
	heatmapAX.grid(False)
	#cplot = ax.pcolor(corr_coef, edgecolors='k', linestyle= 'dashed', linewidths=0.2, cmap = 'RdBu_r')
	### scale colorbar ###
	#scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,2,subplot_spec=heatmapGS[0,0],wspace=0.0,hspace=0.0)
	#scale_cbAX = fig.add_subplot(scale_cbGSSS[0,1])
	scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,1,subplot_spec=heatmapGS[0,0],wspace=0.0,hspace=0.0)
	scale_cbAX = fig.add_subplot(scale_cbGSSS[0,0])
	scale_cbAX.set_axis_off()
	cb = fig.colorbar(axi,ax=scale_cbAX,fraction=0.5,shrink=1.0)
	font = {'size': 8}
	tl = cb.set_label(cbarlabel,fontdict=font)
	cb.ax.yaxis.set_ticks_position('left')
	cb.ax.yaxis.set_label_position('left')
	cb.outline.set_linewidth(0)
	#print cb.get_ticks()
	#print cb.ax.get_fontsize()
	tickL = cb.ax.yaxis.get_ticklabels()
	for t in tickL:
		t.set_fontsize(t.get_fontsize() - 7)
	#fig.tight_layout()
	fig.subplots_adjust(bottom = 0)
	fig.subplots_adjust(top = 1)
	fig.subplots_adjust(right = 1)
	fig.subplots_adjust(left = 0)
	#plt.savefig(fig_prefix+".tiff",format='tiff',additional_artists=fig,bbox_inches="tight",dpi=300)
	plt.savefig(fig_prefix+".png",format='png',additional_artists=fig,bbox_inches="tight",dpi=300)
	if n * p < 200000:
		plt.savefig(fig_prefix+".svg",format='svg',additional_artists=fig,bbox_inches="tight",dpi=300)
	plt.clf()
	plt.close()
	try: 
		return 0, row_cluster_output
	except:
		return 0, ''

def loess_testplot(x,y,ynp,labels=[]):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	n,p = ynp.shape
	assert len(labels) == n
	ret_color,ret_lines,ret_marker = styles(n)

	ax.plot(x,y,"ko")
	#for i in xrange(n)
	



def __test():
	X1 = np.random.normal(0,0.5,(3,3))
	X2 = np.random.normal(3,0.5,(2,3))
	X3 = np.random.normal(6,0.5,(4,3))
	X = np.concatenate((X1,X2,X3))
	Y = [0,0,0,1,1,2,2,2,2]
	color = ['r-','k--','g+']
	uniqclasslables= ['r3','k2','g4']
	colors = [color[i] for i in Y]
	classlabels = [uniqclasslables[i] for i in Y]
	print plot_hmc_curve(X,Y,colors,classlabels,"test_hmc_curve")

def __testplot():
	##绘制kde估计的概率密度  测试 kdensity
	#======================================
	aa = np.random.randn(10000)
	xn,yn = kdensity(aa.tolist())
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(xn,yn,'r--',label="Scott Rule")
	ax.legend(loc=0)
	plt.savefig("test_density.png",format='png',dpi=300)
	#plt.savefig("test_density.jpg",format='jpg',dpi=300)
	#plt.savefig("test_density.tif",format='tif',dpi=300)
	plt.savefig("test_density.svg",format='svg',dpi=300)
	plt.savefig("test_density.pdf",format='pdf',dpi=300)
	plt.clf()
	plt.close()
	##boxplot
	#======================================
	mm = np.array([np.random.randn(100).tolist(),np.random.lognormal(1,1, 100).tolist()])
	mm = mm.transpose()
	boxColors = ['darkkhaki','royalblue']
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
	bp = ax1.boxplot(mm)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')
	for i in xrange(2):
		box = bp['boxes'][i]
		boxX = box.get_xdata().tolist()
		boxY = box.get_ydata().tolist()
		boxCoords = zip(boxX,boxY)
		boxPolygon = Polygon(boxCoords, facecolor=boxColors[i])
		ax1.add_patch(boxPolygon)
	#ax1.set_xticklabels(["Normal","Uniform"],rotation=45)
	ax1.set_xticklabels(["Normal","Lognormal"],rotation=45)
	ax1.set_title('Test Boxplot')
	#ax1.set_title(u'箱图')
	ax1.set_xlabel('Distribution',fontstyle='italic')
	#ax1.set_xlabel('Distribution',fontstyle='oblique')
	ax1.set_ylabel('Values')
	#ax1.set_axis_off() 不显示坐标轴
	plt.savefig("test_boxplot.png",format='png',dpi=300)
	plt.savefig("test_boxplot.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#=====================================
	##kmeans class plot
	pt1 = np.random.normal(1, 0.2, (100,2))
	pt2 = np.random.normal(2, 0.5, (300,2))
	pt3 = np.random.normal(3, 0.3, (100,2))
	pt2[:,0] += 1
	pt3[:,0] -= 0.5
	xy = np.concatenate((pt1, pt2, pt3))
	##归一化处理 from scipy.cluster.vq import whiten
	xy = whiten(xy)
	## res 是类中心点坐标，idx为类别
	res, idx = kmeans2(xy,3)
	## 非常好的生成colors的方法
	colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in idx])
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.scatter(xy[:,0],xy[:,1],c=colors)
	ax1.scatter(res[:,0],res[:,1], marker='o', s=300, linewidths=2, c='none')
	ax1.scatter(res[:,0],res[:,1], marker='x', s=300, linewidths=2)
	plt.savefig("test_kmeans.png",format='png',dpi=300)
	plt.savefig("test_kmeans.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#====================================
	##plot hierarchy
	mat1 = np.random.normal(0,1,(3,3))
	mat2 = np.random.normal(2,1,(2,3))
	mat = np.concatenate((mat1,mat2))
	linkage_matrix = linkage(mat,'ward','euclidean')
	fig = plt.figure()
	#ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222)
	dendrogram(linkage_matrix,labels=["N1","N2","N3","P1","P2"],leaf_rotation=45)
	ax3 = fig.add_subplot(223)
	dendrogram(linkage_matrix,labels=["N1","N2","N3","P1","P2"],orientation='right',leaf_rotation=45)
	#ax4 = fig.add_subplot(224)
	plt.savefig("test_hcluster.png",format='png',dpi=300)
	plt.savefig("test_hcluster.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#======================================
	##plot hierarchy with image
	mat1 = np.random.normal(0,1,(4,10))
	mat2 = np.random.normal(5,1,(3,10))
	mat = np.concatenate((mat1,mat2))
	mat[:,3:] -= 20
	mat -= np.mean(mat,axis=0)
	samplenames = ["N1","N2","N3","N4","P1","P2","P3"]
	dimensions = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]
	cluster_heatmap(mat,samplenames,dimensions)
	#===============================================
	##bar plot and err barplot
	N = 5
	menMeans   = (20, 35, 30, 35, 27)
	womenMeans = (25, 32, 34, 20, 25)
	menStd     = (2, 3, 4, 1, 2)
	womenStd   = (3, 5, 2, 3, 3)
	ind = np.arange(N)
	width = 0.35
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.bar(ind, menMeans,   width, color='r', yerr=womenStd,label='Men')
	ax.bar(ind, womenMeans, width, color='y',bottom=menMeans, yerr=menStd,label = 'Women')
	ax.set_ylabel('Scores')
	ax.set_title('Scores by group and gender')
	ax.set_xticks(ind+width/2)
	ax.set_xlim(left = -0.25)
	ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
	#ax.set_xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5'))
	ax.set_yticks(np.arange(0,81,10))
	ax.legend(loc=0)
	plt.savefig("test_bar.png",format='png',dpi=300)	
	plt.savefig("test_bar.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#==============================================
	##hist plot
	mu=2
	x = mu + np.random.randn(1000,3)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	n,bins,patches = ax.hist(x, 15, normed=1, histtype='bar',linewidth=0,color=['crimson', 'burlywood', 'chartreuse'],label=['Crimson', 'Burlywood', 'Chartreuse'])
	ax.legend(loc=0)
	plt.savefig("test_hist.png",format='png',dpi=300)
	plt.savefig("test_hist.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#===============================================
	##hist2D plot  and  image colorbar plot on the specific ax 
	x = np.random.randn(100000)
	y = np.random.randn(100000)+5
	fig = plt.figure()
	ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222)
	ax3 = fig.add_subplot(223)
	ax4 = fig.add_subplot(224)
	counts, xedges, yedges, image_instance = ax4.hist2d(x, y, bins=40, norm=LogNorm())
	ax1.set_axis_off()
	plt.colorbar(image_instance,ax=ax1)
	plt.savefig("test_hist2d.png",format='png',dpi=300)
	plt.savefig("test_hist2d.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#===============================================
	##image show plot
	y,x = np.ogrid[-2:2:200j,-3:3:300j]
	z = x*np.exp(-x**2 - y**2)
	extent = [np.min(x),np.max(z),np.min(y),np.max(y)]
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	#alpha: scalar The alpha blending value, between 0 (transparent) and 1 (opaque)
	#设定每个图的colormap和colorbar所表示范围是一样的，即归一化  
	#norm = matplotlib.colors.Normalize(vmin=160, vmax=300), 用法  imshow(norm = norm)
	image_instance = ax1.imshow(z,extent=extent,cmap=cm.coolwarm,alpha=0.6,origin='lower')
	plt.colorbar(image_instance,ax=ax1)
	plt.savefig("test_image.png",format='png',dpi=300)
	plt.savefig("test_image.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#===============================================
	##contour map with image
	fig = plt.figure()	
	ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222)
	#cs = ax1.contour(z,5,extent = extent,origin = 'lower',linestyles='dashed')
	cs = ax2.contour(z,10,extent = extent,origin = 'lower',cmap=cm.coolwarm)
	plt.clabel(cs,fmt = '%1.1f',ax=ax2)
	ax3 = fig.add_subplot(223)
	ax4 = fig.add_subplot(224)
	cs1 = ax4.contour(x.reshape(-1),y.reshape(-1),z,10,origin = 'lower',colors = 'k',linestyles='solid')
	cs2 = ax4.contourf(x.reshape(-1),y.reshape(-1),z,10,origin = 'lower',cmap=cm.coolwarm)
	plt.clabel(cs1,fmt = '%1.1f',ax=ax4)
	plt.colorbar(cs2,ax=ax4)
	plt.savefig("test_contour.png",format='png',dpi=300)
	plt.savefig("test_contour.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#===============================================
	##meshgird plot 3D
	#生成格点数据，利用griddata插值  
	#grid_x, grid_y = np.mgrid[275:315:1, 0.60:0.95:0.01]
	#from scipy.interpolate import griddata 
	#grid_z = griddata((LST,EMS), TBH, (grid_x, grid_y), method='cubic') 
	x,y = np.mgrid[-2:2:200j,-3:3:300j]	
	z = x*np.exp(-x**2 - y**2)
	fig = plt.figure(figsize=(20,20), dpi=300)
	ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222,projection ='3d')
	ax3 = fig.add_subplot(223,projection ='3d')
	ax4 = fig.add_subplot(224,projection ='3d')
	cs1 = ax1.contour(x,y,z,10,extent = extent,origin = 'lower',cmap=cm.coolwarm)
	plt.clabel(cs,fmt = '%1.1f',ax=ax1)
	surf = ax2.plot_surface(x,y,z, rstride=20, cstride=20, cmap=cm.coolwarm,linewidth=1, antialiased=False)
	fig.colorbar(surf,ax=ax2)
	surf = ax3.plot_wireframe(x,y,z, rstride=20, cstride=20, cmap=cm.coolwarm)
	#仰角elevation和方位轴azimuth
	#ax.view_init(elevation, azimuth)   ‘elev’ stores the elevation angle in the z plane， ‘azim’ stores the azimuth angle in the x,y plane.
	ax4.plot_surface(x, y, z, rstride=20, cstride=20, alpha=0.3)
	cset = ax4.contour(x, y, z, 10, offset = ax4.get_zlim()[0],zdir='z',cmap=cm.coolwarm)
	cset = ax4.contour(x, y, z, 10, offset = ax4.get_xlim()[0],zdir='x',cmap=cm.coolwarm)
	cset = ax4.contour(x, y, z, 10, offset = ax4.get_ylim()[-1],zdir='y',cmap=cm.coolwarm)
	plt.savefig("test_surface3d.png",format='png',dpi=300)
	plt.savefig("test_surface3d.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#====================================================
	## pie plot
	labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
	sizes = np.array([15.2, 31, 42, 10.5])
	#sizes = sizes/np.sum(sizes)
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	explode = (0, 0.05, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
	fig = plt.figure(figsize=(8,8),dpi=300)
	ax5 = fig.add_subplot(111)
	ax5.pie(sizes,explode,labels=labels, colors=colors,autopct='%1.1f%%', shadow=False, startangle=90)
	plt.savefig("test_pie.png",format='png',dpi=300)
	plt.savefig("test_pie.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#====================================================
	## scatter
	N = 100
	r0 = 0.6
	x = 0.9*np.random.rand(N)
	y = 0.9*np.random.rand(N)
	area = np.pi*(10 * np.random.rand(N))**2
	c = np.sqrt(area)
	r = np.sqrt(x*x+y*y)
	area1 = np.ma.masked_where(r < r0, area)
	area2 = np.ma.masked_where(r >= r0, area)
	fig = plt.figure()
	ax  = fig.add_subplot(111)
	ax.scatter(x,y,s=area1, marker='^', c=c)
	ax.scatter(x,y,s=area2, marker='o', c=c)
	# Show the boundary between the regions:
	theta = np.arange(0, np.pi/2, 0.01)
	ax.plot(r0*np.cos(theta), r0*np.sin(theta))
	plt.savefig("test_scatter.png",format='png',dpi=300)
	plt.savefig("test_scatter.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#====================================================
	## table
	colheader = ['#probe_id','gene symbol','fold change','pvalue','FDR']
	#rowheader = ["top1","top2"]
	content = [["ge","ann1",3,4,5],["ge2","ann2",7,8,8]]
	#colors = plt.cm.BuPu(np.linspace(0, 0.5, len(colheader)))
	fig = plt.figure()
	ax = plt.gca()
	#the_table = ax.table(cellText=cell_text,rowLabels=rows,rowColours=colors,colLabels=columns,loc='bottom')
	##colWidths = [0.1]*5
	ax.table(cellText=content,colLabels = colheader,loc='top')
	ax.set_axis_off()
	plt.savefig("test_table.png",format='png',dpi=300)
	plt.savefig("test_table.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	#====================================================
	## plotyy
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	t = np.arange(0.01, 10.0, 0.01)
	s1 = np.exp(t)
	ax1.plot(t, s1, 'b-')
	ax1.set_xlabel('time (s)')
	ax1.set_ylabel('exp', color='b')
	for tl in ax1.get_yticklabels():
		tl.set_color('b')
	ax2 = ax1.twinx()
	s2 = np.sin(2*np.pi*t)
	ax2.plot(t, s2, 'ro')
	ax2.set_ylabel('sin', color='r')
	for tl in ax2.get_yticklabels():
		tl.set_color('r')
	plt.savefig("test_plotyy.png",format='png',dpi=300)
	plt.savefig("test_plotyy.svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
if __name__ == "__main__":
	__testplot()
	__test()




"""
The following color abbreviations are supported
'b'         blue
'g'         green
'r'         red
'c'         cyan
'm'         magenta
'y'         yellow
'k'         black
##'w'         white

In addition, you can specify colors in many weird and
wonderful ways, including full names (``'green'``), hex
strings (``'#008000'``), RGB or RGBA tuples (``(0,1,0,1)``) or
grayscale intensities as a string (``'0.8'``).

the line style or marker:

	================    ===============================
	character           description
	================    ===============================
	``'-'``             solid line style
	``'--'``            dashed line style
	``'-.'``            dash-dot line style
	``':'``             dotted line style
	
	
	``'.'``             point marker
	``','``             pixel marker
	``'o'``             circle marker
	``'v'``             triangle_down marker
	``'^'``             triangle_up marker
	``'<'``             triangle_left marker
	``'>'``             triangle_right marker
	``'1'``             tri_down marker
	``'2'``             tri_up marker
	``'3'``             tri_left marker
	``'4'``             tri_right marker
	``'s'``             square marker
	``'p'``             pentagon marker
	``'*'``             star marker
	``'h'``             hexagon1 marker
	``'H'``             hexagon2 marker
	``'+'``             plus marker
	``'x'``             x marker
	``'D'``             diamond marker
	``'d'``             thin_diamond marker
	``'|'``             vline marker
	``'_'``             hline marker

marker: [ ``7`` | ``4`` | ``5`` | ``6`` | ``'o'`` | ``'D'`` | ``'h'`` | ``'H'`` | ``'_'`` | ``''`` | ``'None'`` | ``' '`` | ``None`` | ``'8'`` | ``'p'`` | ``','`` | ``'+'`` | ``'.'`` | ``'s'`` | ``'*'`` | ``'d'`` | ``3`` | ``0`` | ``1`` | ``2`` | ``'1'`` | ``'3'`` | ``'4'`` | ``'2'`` | ``'v'`` | ``'<'`` | ``'>'`` | ``'^'`` | ``'|'`` | ``'x'`` | ``'$...$'`` | *tuple* | *Nx2 array* ]

"""


