#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import compress
import os
import numpy as np
import scipy as sp
from scipy import stats
import sys
import time
import ctypes
import itertools
#import mplconfig

def check_vecnan(nparr):
	idx = ~np.isnan(nparr)
	if np.sum(idx) >=1:
		return idx
	else:
		return None

from copy import deepcopy
def get_clean_matrix(sinfo,data,deafult=1):
	# 1 is first to clean p 
	# 0 is first to clean n
	assert deafult in [0,1]
	sinfo2 = deepcopy(sinfo)
	data2  = deepcopy(data)
	if deafult:
		idx = ~np.isnan(data2.data)
		colclean = np.sum(idx,0) == data2.data.shape[0]
		colclean = np.asarray(colclean)[0]
		tmpdata = data2.data[:,colclean]
		idx_ = ~np.isnan(tmpdata)
		rowclean = np.sum(idx_,1) == tmpdata.shape[1] # row is samples , col is variables
		rowclean = np.asarray(rowclean.T)[0]
	else:
		idx = ~np.isnan(data2.data) 
		rowclean = np.sum(idx,1) == data2.data.shape[1]
		rowclean = np.asarray(rowclean.T)[0]
		tmpdata = data2.data[rowclean,:]
		idx_ = ~np.isnan(tmpdata)
		colclean = np.sum(idx_,0) == tmpdata.shape[0]
		colclean = np.asarray(colclean)[0]

	data2.data = data2.data[rowclean,:][:,colclean].copy()
	data2.anno    = np.asarray(data2.anno)[colclean].tolist()[:]
	data2.annosep = np.asarray(data2.annosep)[colclean].tolist()[:]
	data2.anno1   = np.asarray(data2.anno1)[colclean].tolist()[:]
	data2.anno2   = np.asarray(data2.anno2)[colclean].tolist()[:]
	
	sinfo2.samplenum   = np.sum(rowclean)
	sinfo2.classlabels = np.asarray(sinfo2.classlabels)[rowclean].tolist()[:]
	sinfo2.samplecolors= np.asarray(sinfo2.samplecolors)[rowclean].tolist()[:]
	sinfo2.classcolors = np.asarray(sinfo2.classcolors)[rowclean].tolist()[:]
	sinfo2.samplelines = np.asarray(sinfo2.samplelines)[rowclean].tolist()[:]
	sinfo2.classlines  = np.asarray(sinfo2.classlines)[rowclean].tolist()[:]
	sinfo2.samplemarkers = np.asarray(sinfo2.samplemarkers)[rowclean].tolist()[:]
	sinfo2.classmarkers  = np.asarray(sinfo2.classmarkers)[rowclean].tolist()[:]
	sinfo2.sns           = np.asarray(sinfo2.sns)[rowclean].tolist()[:]
	sinfo2.samplenames    = np.asarray(sinfo2.samplenames)[rowclean].tolist()[:]
	sinfo2.traits        = np.asarray(sinfo2.traits)[rowclean].tolist()[:]
	sinfo2.files         = np.asarray(sinfo2.files)[rowclean].tolist()[:]
	sinfo2.classids      = np.asarray(sinfo2.classids)[rowclean].tolist()[:]
	tmpclasslabels = np.asarray(sinfo2.classlabels)
	h = {}
	for i in xrange(len(sinfo2.uniqclasslabel)):
		tmplabel = sinfo2.uniqclasslabel[i]
		sinfo2.hidx[tmplabel] = tmpclasslabels == tmplabel
		h[tmplabel] = i
	"""
	136         for classlabel in self.classlabels:
	137             self.classnums.append(h[classlabel])
	138             self.classcolors = [self.uniqcolor[i] for i in self.classnums]
	139             self.classmarkers = [self.uniqmarker[i] for i in self.classnums]
	140             self.classlines  = [self.uniqline[i] for i in self.classnums]
	"""
	sinfo2.classnums = []
	for classlabel in sinfo2.classlabels:
		sinfo2.classnums.append(h[classlabel])
	return sinfo2,data2

class SampleInfo(object):
	def __init__(self):
		#SN Files   samplename  classid classname
		#S1	xx_1.fq.gz,xx_2.fq.gz	S1sample	1	CK
		#S2 xx_1.fq.gz,xx_2.fq.gz   S2sample    1   CK
		#S3 xx_1.fq.gz,xx_2.fq.gz   S3sample    2   MT
		#S4 xx_1.fq.gz,xx_2.fq.gz   S4sample    2   MT
		self.samplenum = 0 # record 4
		
		self.classlabels = []    # record [CK,CK,MT,MT]   # 按读取的顺序
		self.uniqclasslabel = [] # record [CK,MT]         # 按读取的顺序
		
		self.samplecolors = []   # 用style 函数产生的 sample color 
		self.classcolors = []    # 用style 函数产生的 class  color
		self.samplelines = []    # 对应的线型
		self.classlines = []     #
		self.samplemarkers = []  # 对应的marker  'o','^','v','+'
		self.classmarkers = []   # 对应的marker 'o','o','^','^'
		
		self.uniqcolor = []      # 内置
		
		self.classnums =[]       # record [1,1,2,2,]  class index id 按顺序
		self.uniqclassnum = []   # record [1,2]
		
		self.sns = []            # 第一列
		self.samplenames=[]      # 第三列
		self.traits = []         # 第四列
		self.uniqline = []       # 内置 
		self.uniqmarker = []     # 内置
		
		self.files = []          # 记录文件["SN///filename",]
		self.hfiles = {}         # 记录hfiles["SN"] => [filename,filename]
		self.hidx = {}           # 记录hidx["CK"] => [0,1] 即某组样本的index 编号
		self.hclassidxsn = {}    # 记录hclassidxsn["CK"] => [sn,sn]
		self.classids = []       # 记录 nparray [1,1,2,2]
		self.hclassid2classname = {} # 记录 hclassid2classname["1"] => "CK"
	
	def parse_sampleinfo(self,sampleinfo,phenotype='category'):
		fh = file(sampleinfo,"r")
		classnumOrtraits = []
		for line in fh:
			if line.startswith("#") or line.startswith("\n") or line.startswith(" ") or line.startswith("\t"):continue
			nameid,filedetail,samplename,trait,other = line.rstrip("\n").split("\t",4)
			
			self.sns.append(nameid)
			files = filedetail.rstrip(",").split(",")
			self.hfiles[nameid] = []
			for filename in files:
				self.files.append(nameid+"///"+filename)
				self.hfiles[nameid].append(filename)
			classname = other.split("\t")[0]
			if classname not in self.hclassidxsn:
				self.hclassidxsn[classname] = []
			self.hclassidxsn[classname].append(nameid)
			self.hclassid2classname[trait] = classname
			self.samplenum += 1
			self.classlabels.append(classname)
			if classname in self.uniqclasslabel:pass
			else:self.uniqclasslabel.append(classname)
			classnumOrtraits.append(trait)
			self.samplenames.append(samplename)
		fh.close()
		## use sample number to get iteration colors, markers and lines
		self.uniqcolor,self.uniqline,self.uniqmarker = mplconfig.styles(len(self.uniqclasslabel))
		self.samplecolors,self.samplelines,self.samplemarkers = mplconfig.styles(self.samplenum)
		#self.uniqclasslabel = list(set(self.classlabels))
		self.uniqclassnum = range(len(self.uniqclasslabel))
		h={}
		tmpclasslabels = np.asarray(self.classlabels)
		for i in xrange(len(self.uniqclasslabel)):
			tmplabel = self.uniqclasslabel[i]
			self.hidx[tmplabel] = tmpclasslabels == tmplabel
			h[tmplabel] = i
		for classlabel in self.classlabels:
			self.classnums.append(h[classlabel])
			self.classcolors = [self.uniqcolor[i] for i in self.classnums]
			self.classmarkers = [self.uniqmarker[i] for i in self.classnums]
			self.classlines  = [self.uniqline[i] for i in self.classnums]
		#print self.classcolors
		#print self.classmarkers
		#print self.classlines
		
		if phenotype == "category":
			self.traits = np.transpose(np.asmatrix(np.float64(classnumOrtraits[:])))
			self.classids = np.float64(classnumOrtraits[:])
		elif phenotype == "quantificat":
			self.traits = np.transpose(np.asmatrix(np.float64(classnumOrtraits[:]))) ## n X 1 matrix
		else:return 1
		#print self.traits
		return 0


class MatrixAnno(object):
	##np.asarray(a[:,0].T)[0].tolist()
	def __init__(self):
		"""
		# file format:
		#geneid	ID2	SN1	SN2	SN3	SN4
		genaeA	trA	1.73	2.56	7.31	8.991
		geneB	trB	2.123	123.1	21313.	12312.      // note: tab sep
		"""
		self.p = 0 # p record: variate numbers
		self.n = 0 # n record: sample numbers 
		self.data  = None # np.matrix => n X p matrix
		self.anno = []    # ["genaeA\ttrA","geneB\ttrB"]
		self.annosep = [] # ["genaeA|trA","geneB|trB"] 
		self.anno1 = []   # ["genaeA","geneB"]
		self.anno2 = []   # ["trA","trB"]
	def parse_matrix_anno(self,fmatrixanno,cutoff=-10000000.0,precent=0.5,addtolog=0.001,log2tr=0):
		fh = compress.gz_file(fmatrixanno,"r") # -np.inf
		t0 = time.time()	
		sys.stderr.write('[INFO] Start to Build data ...\n')
		for line in fh:
			if line.startswith("#") or line.startswith("\n") or line.startswith(" ") or line.startswith("\t"):
				continue
			else:
				#arr = line.rstrip("\n").split("\t")
				arr = line.rstrip("\n").split("\t")
				self.n = len(arr[2:])
				break
		fh.seek(0)
		t0 = time.time()
		num = int(self.n * precent)
		self.p = 0
		for line in fh:
			if line.startswith("#") or line.startswith("\n") or line.startswith(" ") or line.startswith("\t"):continue
			else:
				self.p += 1
		fh.seek(0)
		self.data = np.zeros((self.n,self.p))
		realp = 0
		filterp = 0
		for line in fh:
			if line.startswith("#") or line.startswith("\n") or line.startswith(" ") or line.startswith("\t"):continue
			else:
				arr = line.rstrip("\n").rstrip().split("\t")
				try:
					tmpdata = np.float64(arr[2:])
				except:
					sys.stderr.write("[ERROR] %s"%line)
					sys.stderr.write("[ERROR] n is not same as exprsnums\n")
					exit(1)
				if self.n >=2:
					if np.nanstd(tmpdata,ddof=1) <=0:
						sys.stderr.write("[INFO] data: %s was filtered, no variation \n"%(arr[0]+": "+arr[1]))
						filterp += 1
						continue## filter the no var data
					if np.sum(np.isnan(tmpdata)) > num:
						sys.stderr.write("[WARN] data: %s was filtered, too many NANs \n"%(arr[0]+": "+arr[1]))
						filterp += 1
						continue
					if np.sum(np.isnan(tmpdata)) + np.sum(tmpdata[~np.isnan(tmpdata)] < cutoff) > num:
						sys.stderr.write("[WARN] data: %s was filtered, too many exprs lower than noise \n"%(arr[0]+": "+arr[1]))
						filterp += 1
						continue
					if len(set(arr[2:])) <= 1:
						sys.stderr.write("[WARN] data: %s was filtered, because of no variation\n"%(arr[0]+": "+arr[1]))
						filterp += 1
						continue
				if log2tr:
					tmpdata = np.log2(tmpdata+addtolog)
				realp += 1
				if realp % 100000 == 0:
					sys.stderr.write("[INFO] parsed %d data\n"%realp)
				self.data[:,realp-1] = tmpdata
				self.anno.append(arr[0] + "\t" + arr[1])
				self.annosep.append(arr[0] + "|" + arr[1])
				self.anno1.append(arr[0])
				self.anno2.append(arr[1])
		#self.data = np.asmatrix(np.transpose(self.data.reshape(self.p,self.n)))
		#filter the sd 
		sys.stderr.write("[INFO] filter numbers: %d\n"%filterp)
		sys.stderr.write("[INFO] real numbers: %d\n"%realp)
		fh.close()
		# 2723,  4195,  8263,  8744, 11416
		self.data = np.asmatrix(self.data[:,0:realp])
		self.p = realp
		assert len(self.anno) == self.p
		sys.stderr.write("\n")
		sys.stderr.write('[INFO] Data Built done! cost %.2fs\n'%(time.time()-t0))
		#self.data = np.asmatrix(self.data)
		#print self.data[:,10]
		#print self.anno[10]
		#print self.annosep[10]
		return 0

class FactorFrame(object):
	def __init__(self):
		self.fnm = []##factor name
		self.snm = []##must same as sample infos
		self.lvs = 0## number of variables
		self.var = []##
		self.levels = []
	def parse_factor(self,factorfile):
		f = compress.gz_file(factorfile,"r")
		for line in f:
			if line.startswith("##"):continue
			if line.startswith("#"):
				self.fnm = line.rstrip("\n").split("\t")[1:]
				self.lvs = len(self.fnm)
				self.levels = [0,]*self.lvs
				continue
			arr = line.rstrip("\n").split("\t")
			self.snm.append(arr[0])
			self.var.append(map(str,arr[1:]))
		f.close()
		self.var = np.asarray(self.var)
		for i in xrange(self.lvs):
			self.levels[i] = len(set(self.var[:,i].tolist()))
		print self.levels
		self.var = np.float64(self.var)
		return 0

def datacheck(X):
	ret = 1
	if isinstance(X,np.matrix) or isinstance(X,np.array):pass
	else:
		sys.stderr.write('[ERROR] centring only support matrix or array data\n')
		return ret
	if X.dtype == np.float64 or X.dtype == np.float32:pass
	else:
		sys.stderr.write('[ERROR] centring only support float64 or float32 data\n')
		return ret
	return 0

def centring(X,axis=0):
	ret = 1
	#if datacheck(X):
	#	return ret
	Xmean = np.mean(X,axis=axis)
	X -= Xmean
	return Xmean

def normalize(X,axis=0):
	ret = 1
	#if datacheck(X):
	#	return ret
	Xstd =np.std(X,ddof=1,axis=axis)
	#print np.where(Xstd==0)
	X /= Xstd
	return Xstd


def twoDimDistr(object, fraction = 100):
	''' 
	Object must be a matrix format, and the number of columns is 2.
	'''
	if not isinstance(object, np.ndarray):
		try:object = np.asarray(object)
		except:
			raise
		else:sys.stderr.write('[WARN] Transfer the raw data to matrix format.\n')
	if object.shape[-1] <> 2: exit(1)
	#for i in xrange(np.shape(object)[-1]):
	#	if np.max(abs(object[:, i])) > 1:
	#		object[:, i] = object[:, i] / np.max(abs(object[:, i]))
	xmin = -1#np.min(object[:,0]);
	xmax = 1 #np.max(object[:,0]);
	ymin = -1#np.min(object[:,1]);
	ymax = 1 #np.max(object[:,1])
	x_coord = np.linspace(xmin, xmax, fraction).tolist()
	y_coord = np.linspace(ymin, ymax, fraction).tolist()
	x_coord.append(np.inf)
	y_coord.append(np.inf)
	countsMatrix = np.zeros((fraction, fraction))
	for i in xrange(fraction):
		bool_x = np.int32(object[:,0] >= x_coord[i]) * np.int32(object[:,0] < x_coord[i+1])
		#x_idx = np.bool8(bool_x)
		for j in xrange(fraction):
			#tmp_y = object[:,1][x_idx]
			#bool_x = np.int32(object[:,0] >= x_coord[i]) * np.int32(object[:,0] < x_coord[i+1])
			bool_y = np.int32(object[:,1] >= y_coord[j]) * np.int32(object[:,1] < y_coord[j+1])
			countsMatrix[i,j] = np.sum(bool_x * bool_y)
	return countsMatrix,[xmin,xmax,ymin,ymax]

def quantile(Xnp):
	ranks=[]
	n, p = Xnp.shape
	Xnormalize = np.asmatrix(np.zeros((n,p)))
	for i in xrange(n):
		ranks.append(np.int32(stats.rankdata(Xnp[i,:],"min")).tolist())
	Xnptmp = Xnp.copy()
	Xnptmp.sort()
	ranks = np.asarray(ranks)
	Xnptmpmean = np.asarray(np.mean(Xnptmp,axis = 0))
	for i in xrange(n):
		Xnormalize[i] = Xnptmpmean[0][ranks[i]-1]
	return Xnormalize

##int get_permutation(char *vipname,char *pername,long c_demensionx_adv,long c_ntimes,double *pvalue_adv)
def c_permutation(fvipname,fpername,p,ntimes=1000):
	pvalue = None
	try:
		libpremutation  = ctypes.CDLL('cal_permutation.so')
	except:
		sys.stderr.write('[ERROR] Can not load cal_permutation.so\n')
		return pvalue
	pvalue = (ctypes.c_double * p)()
	ctypes.memset(ctypes.addressof(pvalue),0,ctypes.sizeof(pvalue))
	ret = libpremutation.get_permutation(ctypes.c_char_p(fvipname),ctypes.c_char_p(fpername),ctypes.c_long(p),ctypes.c_long(ntimes),pvalue)
	return pvalue

def comb_replace(datalist,num):
	return list(itertools.combinations_with_replacement([datalist], num))

if __name__ == "__main__":
	##can use abspath to get __file__ path ,and then load module
	libpremutation  = ctypes.CDLL('cal_permutation.so')
	print libpremutation.get_permutation
	#a = np.array([[5,4,3],[2,1,4],[3,4,6],[4,2,8]])
	#a= np.asmatrix(np.transpose(a))
	#print quantile(a)
	ins = FactorFrame()
	ins.parse_factor(sys.argv[1])
