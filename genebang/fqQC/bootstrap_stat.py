import sys
#from utils import get_pathfile
#print get_pathfile(__file__)
import seqio
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
mpl.rcParams.update({'font.size': 8})
class seqqc_result(object):
	def __init__(self,sn,fn,seqlen):
		self.fn = fn
		self.sn = sn
		self.fstat = np.zeros(6)#[bases,reads,Q20,Q30,flowQ,N]
		self.fG = np.zeros(seqlen)#list
		self.fA = np.zeros(seqlen)
		self.fC = np.zeros(seqlen)
		self.fT = np.zeros(seqlen)
		self.fN = np.zeros(seqlen)
		self.fQ = np.zeros((42,seqlen))## 41 X seqlen  <=0 ~ >=40
			
def plot_stat(fQ,fG,fC,fT,fA,fN,seqlen,figprefix):#GCATN distribution and qual distribution
	fig = plt.figure(figsize=(10,4),dpi=300)
	ax1 = fig.add_subplot(121)
	#bp  = ax1.boxplot(fQ,0,'')
	#ax1.set_ylabel('Base quality')
	#ax1.set_xlabel('Postion along reads')
	#ax1.grid()
	nmin = np.min(fQ,0)
	nmax = np.max(fQ,0)
	#fQ  = (fQ-nmin+1)/(nmax-nmin+1)
	fQ  = fQ / (np.sum(fQ,axis=0)+0.001)
	image_instance = ax1.imshow(fQ,interpolation='nearest',aspect='auto',cmap=cm.coolwarm,alpha=0.8,origin='lower')
	#ax1.set_yticks(np.arange(0,41))
	#ax1.set_xticks(np.arange(1,seqlen+1))
	cb = fig.colorbar(image_instance,ax=ax1,orientation='horizontal')
	cb.set_label("Percentage")
	cb.outline.set_linewidth(0)
	#cb.ax.set_yticklabels(['0', '0.2', '0.4','0.6','0.8','1'])
	#cb.ax.yaxis.set_ticks_position('left')
	#cb.ax.yaxis.set_label_position('left')
	ax1.set_xlabel('Postion along reads')
	ax1.set_ylabel('Base quality')
	ax2 = fig.add_subplot(122)
	sum_nuc = fA + fT + fG + fC + fN + 1
	ax2.plot(range(1,len(fA)+1),fA/sum_nuc*100,'r-',alpha=0.6,label='A')
	ax2.plot(range(1,len(fT)+1),fT/sum_nuc*100,'b-.',alpha=0.6,label='T')
	ax2.plot(range(1,len(fG)+1),fG/sum_nuc*100,'g--',alpha=0.6,label='G')
	ax2.plot(range(1,len(fC)+1),fC/sum_nuc*100,'m:',alpha=0.6,label='C')
	ax2.plot(range(1,len(fN)+1),fN/sum_nuc*100,'c--',alpha=0.6,label='N')
	#yl,yh = ax2.get_ylim()
	#ax2.set_ylim(-5,yh)
	ax2.legend(loc=0)
	ax2.set_ylim(0,100)
	ax2.set_ylabel('Base content')
	ax2.set_xlabel('Postion along reads')
	ax2.grid()
	plt.savefig(figprefix+".png",format='png',dpi=300)
	plt.savefig(figprefix+".svg",format='svg',dpi=300)
	plt.clf()
	plt.close()
	return 0

def bootstrap_stat(sn,fn,seqlen,fig_dir,qual=64,times=60000):
	fmt = "fastq-sanger"
	if qual == 64:
		fmt = "fastq-illumina"
	elif qual == 33:
		fmt = "fastq-sanger"
	#for fn in files:
	result_ins = seqqc_result(sn,fn,seqlen)
	count = 0
	print "Begin"
	tmpseq = [""]*seqlen
	tmpqual = [-1]*seqlen
	totalbase = 0.0
	for rec in seqio.fastq_read(fn,fmt):
		if np.random.random()>0.01:continue
		count +=1
		if count % 5000 == 0:
			print "parse",count
		if count % times == 0:break
		sequences = np.asarray(list(rec.seq))
		quals = np.asarray(rec.letter_annotations['phred_quality'])
		tmpseqlen = len(sequences)
		assert tmpseqlen == len(quals)
		try:
			assert tmpseqlen == seqlen
		#except Exception,e:
			#sys.stderr.write("[WARN] Read len warning, can not pass 'readlen(%d) == qualiltylen(%d) == options.readlen(%d)'\n"%(len(sequences),len(quals),seqlen))
			#exit(1)
		except Exception:
			sequences = tmpseq[:]
			quals     = tmpqual[:]
			uuseqlen = min(tmpseqlen,seqlen)
			sequences[0:uuseqlen] = list(rec.seq)[0:uuseqlen]
			quals[0:uuseqlen]     = rec.letter_annotations['phred_quality'][0:uuseqlen]
			sequences = np.asarray(sequences)
			quals     = np.asarray(quals)
		totalbase += min(tmpseqlen,seqlen)
		result_ins.fstat += np.asarray([seqlen,1,np.sum(quals>=20),np.sum(quals>=30),np.sum((quals>=0)*(quals<5)),np.sum(sequences == "N")])
		result_ins.fG += (sequences == "G");result_ins.fC += (sequences == "C");result_ins.fA += (sequences == "A");result_ins.fT += (sequences == "T");
		result_ins.fN += (sequences == "N");
		result_ins.fQ[0,:] += (quals == 0)
		result_ins.fQ[41,:] += (quals >= 41)
		for i in xrange(1,41):
			result_ins.fQ[i,:] += (quals == i)
	bases,reads,Q20,Q30,flowQ,N = result_ins.fstat
	fnt = result_ins.fn.split("/")[-1]
	snt = result_ins.sn
	#fstatout = file(fstatout,"w")
	#fstatout.write("%s\t%s\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\n"%(snt,fnt,float(Q20)/bases*100,float(Q30)/bases*100,float(flowQ)/bases*100,float(N)/bases*100))
	plot_stat(result_ins.fQ,result_ins.fG,result_ins.fC,result_ins.fT,result_ins.fA,result_ins.fN,seqlen,fig_dir+"/"+snt+"."+fnt)	
	#fstatout.close()
	return "%.2f%%\t%.2f%%\t%.2f%%\t%.2f%%\n"%(float(Q20)/totalbase*100,float(Q30)/totalbase*100,float(flowQ)/totalbase*100,float(N)/totalbase*100)
if __name__ == "__main__":
	bootstrap_stat("SN",[sys.argv[1],],100,"quality_stat.xls")


