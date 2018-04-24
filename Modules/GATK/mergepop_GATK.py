#!/usr/bin/env python
#-*-coding:utf-8-*-
#--------------------------mergpop_GATK.py--------------------------
#   
#		将GATK的cohort数据分成每个样本的vcf
#-------------------------------------------------------------------

import os,sys
import re

allvcf = sys.argv[1]     # cohort vcf
suffix = sys.argv[2]
depth = 10  # min depth per sample, optional
Qual = 30 # min qual , optional
sns = []

idx = 9
idx_INFO = 7
idx_qual = 5

#get the sample alt genotype
def alttype(ref, alt, s_genotype):
	def genos_dic(ref, alt):
		genos_dict = {'0':ref, '.':'0'}
		for i in xrange(len(alt.split(","))):
			genos_dict[str(i+1)] = alt.split(",")[i]
		return genos_dict
	sample_genotype =  s_genotype[0].split("/")
	genos_dict = genos_dic(ref, alt)

	if (sample_genotype[0] == '0') or (sample_genotype[0] == sample_genotype[1]):
		return genos_dict[sample_genotype[1]]
	elif sample_genotype[1] == '0':
		return genos_dict[sample_genotype[0]]
	else:
		return genos_dict[sample_genotype[0]]+','+genos_dict[sample_genotype[1]]

with open(allvcf, "r") as f1, open(os.path.splitext(allvcf)[0]+".sample_list.xls", "w") as f2:
	f2.write("##sample_list\n")
	for line in f1:
		if line.startswith(("#CHROM","#Chrom","#chrom")):
			arr = line.rstrip("\n").split("\t")
			for i in xrange(len(arr)-idx):
				sns.append(arr[i+idx].rstrip(r")").replace(r"(","_"))
				f2.write(sns[i] + "\n")
			f2.write("#end sample number: %d"%(len(arr)-idx))
			break

sn_num = len(sns)
sys.stderr.write("[INFO] %s samples:\n"%sn_num + "[INFO]"+" ".join(sns)+"\n")

f_vcf = []
for i in xrange(sn_num):
	#f = open(sns[i]+".vcf","w")
	f_vcf.append(open(os.path.join(os.path.dirname(allvcf), sns[i] + "." + suffix),"w"))
	f_vcf[i].write("#CHROM\tPOS\tID\tREF\tALT\tQual\tFilter\tINFO\tFormat\t"+sns[i]+"\n")

# num = 0
# sample_alt的多个突变情况的转换为单个样本的 '0' '1'
genotype_alt = {'0/0':'0/0','0/1':'0/1','0/2':'0/1','0/3':'0/1','0/4':'0/1','0/5':'0/1','0/6':'0/1','1/0':'1/0','1/1':'1/1','1/2':'1/2','1/3':'1/2','1/4':'1/2','1/5':'1/2','1/6':'1/2','2/0':'1/0','2/1':'1/2','2/2':'1/1','2/3':'1/2','2/4':'1/2','2/5':'1/2','2/6':'1/2','3/0':'1/0','3/1':'1/2','3/2':'1/2','3/3':'1/1','3/4':'1/2','3/5':'1/2','3/6':'1/2','4/0':'1/0','4/1':'1/2','4/2':'1/2','4/3':'1/2','4/4':'1/1','4/5':'1/2','4/6':'1/2','5/0':'1/0','5/1':'1/2','5/2':'1/2','5/3':'1/2','5/4':'1/2','5/5':'1/1','5/6':'1/2','6/6':'1/1'}

sys.stderr.write("[INFO] mergpop start!\n")
with open(allvcf,"r") as f1:
	for line in f1:
		if line.startswith("#"):continue
		#if len(line.strip()) ==0:continue
		arr = line.rstrip("\n").split("\t")
		
		if float(arr[idx_qual]) < Qual:continue
		DP_info = arr[idx_INFO].split("DP=")
		DP_total = DP_info[1].split(";")
		#if DP_total[0] < depth:continue 
		#genos_dict = genos_dic(arr[3], arr[4])
		#num = num +1
		#print num,genos_dict
		for i in xrange(sn_num):
			if re.match(r"^[0|\.]\/[0|\.]$",arr[i+idx].split(":")[0]):continue
			DP_sample = arr[i+idx].split(":")
			try:
				if int(DP_sample[2]) < depth:continue
			except:
				continue
			arr[idx_INFO] = DP_info[0] + "DP=" + DP_sample[2] + ";" + str(";".join(DP_total[1:]))
			gtype_alt = alttype(arr[3], arr[4], DP_sample)
			if gtype_alt == '*':continue
			genos = [arr[3], gtype_alt]
			genotype = genotype_alt[DP_sample[0]]
			if re.match(r"^1\/2$", genotype):
				f_vcf[i].write("\t".join(arr[0:3] + genos + arr[5:9])+"\t" + ":".join([genotype_alt[DP_sample[0]], DP_sample[1].split(",")[0]+','+DP_sample[1].split(",")[int(DP_sample[0].split("/")[0])]+','+DP_sample[1].split(",")[int(DP_sample[0].split("/")[1])]]+DP_sample[2:])+"\n")
			else:
				f_vcf[i].write("\t".join(arr[0:3] + genos + arr[5:9])+"\t" + ":".join([genotype_alt[DP_sample[0]], DP_sample[1].split(",")[0]+','+DP_sample[1].split(",")[int(DP_sample[0].split('/')[1])]]+DP_sample[2:])+"\n")
			
sys.stderr.write("[INFO] merpop finish!\n")
