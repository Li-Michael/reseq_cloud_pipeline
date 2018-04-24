#-*-coding:utf-8-*-
import sys
from statplot import bar_dict,stackv_bar_plot
import statplot
import os
import numpy as np
from mutilstats import centring,normalize

def MutSubPattern(annofns,outdir="./",target_region=None):
	#annoregion = ['downstream','exonic','intergenic','intronic','ncRNA_exonic','ncRNA_intronic','ncRNA_UTR3','ncRNA_UTR5','splicing','upstream','UTR3','UTR5']
	#flag = 0
	#if target_region in annoregion:
	#   flag  = 1
	sample_arr = []
	indel_c_arr = []
	snp_c_arr = []
	C_A_arr = []# C->A / G->T
	C_T_arr = []# C->T / G->A
	C_G_arr = []# C->G / G->C
	T_A_arr = []# T->A / A->T
	T_C_arr = []# T->C / A->G
	T_G_arr = []# T->G / A->C
	for i in xrange(len(annofns)):
		samplename = annofns[i].split(os.sep)[-1].split(".")[0].split("_vs_")[0] # to 
		variant_function = file(annofns[i],"r")
		indel_c = 0;snp_c = 0;snp_CA = 0;snp_CT = 0;snp_CG = 0;snp_TA = 0;snp_TC = 0;snp_TG = 0;
		line = variant_function.next()
		if not line:continue
		if line[0:3] == "Chr" or line[0]=="#":
			pass
		else:
			variant_function.seek(0)
		for line in variant_function:
			if line.startswith("#"):continue
			if line.startswith("Note:"):break
			arr = line.split("\t")
			try:
				ref = arr[3];alt = arr[4];assert ref!=alt;
			except:
				print arr
			if ref == "-" or alt == "-":
				indel_c +=1
			elif len(ref) != len(alt):
				indel_c +=1
			else:
				snp_c += 1
				if ref == "C":
					if alt == "A":
						snp_CA += 1
					elif alt == "T":
						snp_CT += 1
					elif alt == "G":
						snp_CG += 1
				elif ref == "G":
					if alt == "T":
						snp_CA += 1
					elif alt =="A":
						snp_CT += 1
					elif alt == "C":
						snp_CG += 1
				elif ref == "T":
					if alt == "A":
						snp_TA += 1
					elif alt == "C":
						snp_TC += 1
					elif alt == "G":
						snp_TG += 1
				elif ref == "A":
					if alt == "T":
						snp_TA += 1
					elif alt == "G":
						snp_TC += 1
					elif alt == "C":
						snp_TG += 1
		sample_arr.append(samplename)
		C_A_arr.append(snp_CA);C_T_arr.append(snp_CT);C_G_arr.append(snp_CG);
		T_A_arr.append(snp_TA);T_C_arr.append(snp_TC);T_G_arr.append(snp_TG);indel_c_arr.append(indel_c);snp_c_arr.append(snp_c);
		variant_function.close()
	leng = len(sample_arr)
	mut_stat_xls = file(outdir+"/"+"Mutation_pattern.xls","w")
	mut_stat_xls.write("#Variant\t"+"\t".join(sample_arr)+"\n")
	if len(C_A_arr) == leng and len(C_T_arr) == leng and len(C_G_arr) == leng and len(T_A_arr) == leng and len(T_C_arr) == leng and len(T_G_arr) ==leng and len(indel_c_arr) == leng and len(snp_c_arr) == leng:
		#mut_stat_xls.write("indel_count\t"+"\t".join(map(str,indel_c_arr))+"\n")
		mut_stat_xls.write("SNP_count\t"+"\t".join(map(str,snp_c_arr))+"\n")
		mut_stat_xls.write("C->A/G->T\t"+"\t".join(map(str,C_A_arr))+"\n")
		mut_stat_xls.write("C->T/G->A\t"+"\t".join(map(str,C_T_arr))+"\n")
		mut_stat_xls.write("C->G/G->C\t"+"\t".join(map(str,C_G_arr))+"\n")
		mut_stat_xls.write("T->A/A->T\t"+"\t".join(map(str,T_A_arr))+"\n")
		mut_stat_xls.write("T->C/A->G\t"+"\t".join(map(str,T_C_arr))+"\n")
		mut_stat_xls.write("T->G/A->C\t"+"\t".join(map(str,T_G_arr))+"\n")
		#mut_stat_xls.write("InDel\t"+"\t".join(map(str,indel_c_arr))+"\n")
		mut_stat_xls.close()
		#tot_snp = sum(snp_c_arr);
		tot1 = sum(C_A_arr);tot2= sum(C_T_arr);tot3 = sum(C_G_arr);
		tot4 = sum(T_A_arr);tot5= sum(T_C_arr);tot6 = sum(T_G_arr);
		labels = ["C->A/G->T","C->T/G->A","C->G/G->C","T->A/A->T","T->C/A->G","T->G/A->C"]
		fracs=[tot1,tot2,tot3,tot4,tot5,tot6]
		h = {}
		for i in xrange(6):
			h[labels[i]] = fracs[i]
		bar_dict(h,"total_snp_substitution","Substitution","Counts",fmt="%d")
		plot_data = np.asmatrix(np.float64(np.asarray((C_A_arr,C_T_arr,C_G_arr,T_A_arr,T_C_arr,T_G_arr))))
		stackv_bar_plot(plot_data,sample_arr,"SNP_substitution_pattern","","Percentage",width=0.5,legends=labels,scale=1,orientation ="horizontal",rotation=0)
		# p * n
		plot_2 = plot_data.T[0:,:]
		plot_2 = np.asarray(plot_2)
		plot_2new = plot_2.T/np.sum(plot_2.T,axis=0)
		#print np.sum(plot_2new.T,axis=1)
		plot_2new = plot_2new.T
		centring(plot_2new)
		normalize(plot_2new)
		if len(sample_arr) > 1:
			statplot.cluster_heatmap(np.asmatrix(plot_2new),sample_arr,labels,fig_prefix="SNP_substitution_Mutation_Spectrum",colornorm = 1,nosample=False,nogene=True,plotxlabel=1,plotylabel=1,cbarlabel="Normalized Frequency", trees = 3)	
	return 0

if __name__ == "__main__":
	MutSubPattern(sys.argv[1:])
	###py ~/bin/variant_call/mut_sub_pattern.py *.somatic.indel.snp.fmt
		

