#!/usr/bin/env python
#-*-coding:utf-8-*-

'''
# TP53	chr17	7665053	7683550	
[{"fields": {"end": 7683550, "start": 7665053, "gene": "TP53", "genomeID": "hg38", "chromosome": "chr17"}, "model": "basepedia.locus", "pk": 1}]
将上面全部转成json格式，并一起放在[]中
'''
'''
{"fields": {"start": 123, "geneName": "gg1", "end": 1234, "chrom": 1, "geneID": "gene1"}, "model": "rest.genecode", "pk": 1}, 
'''

import sys,os
import gzip
import random

file1 = sys.argv[1]
file2 = sys.argv[2]
pk_list = random.sample(range(1000000), 80000)
print pk_list[0:100]

class Comment_obj(object):
	def __init__(self, comment):
		self.comment = comment
		
	def getvalue(self, key):
		attr = self.comment.split(key, 1)
		return {True: attr[-1].split(';')[0].strip(), False: "-"}[len(attr) >= 2]
		'''
		default_return = "-"
		if len(attr) >=2:
			default_return = attr[-1].split(';')[0].strip()
		return default_return
		'''

chr_dict = {"chr1":1, "chr2":2, "chr3":3, "chr4":4, "chr5":5, "chr6":6, "chr7":7, "chr8":8, "chr9":9, "chr10":10, "chr11":11, "chr12":12, "chr13":13, "chr14":14, "chr15":15, "chr16":16, "chr17":17, "chr18":18, "chr19":19, "chr20":20, "chr21":21, "chr22":22,"chrX":23, "chrY":24, "chrM":25, "chrx":23, "chry":24, "chrm":25}

''' genecode format
1	chromosome name	chr{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y,M} or GRC accession a
2	annotation source	{ENSEMBL,HAVANA}
3	feature type	{gene,transcript,exon,CDS,UTR,start_codon,stop_codon,Selenocysteine}
4	genomic start location	integer-value (1-based)
5	genomic end location	integer-value
6	score (not used)	.
7	genomic strand	{+,-}
8	genomic phase (for CDS features)	{0,1,2,.}
9	additional information as key-value pairs	see below

gene_id	ENSGXXXXXXXXXXX.X b,c _Xg
transcript_id d	ENSTXXXXXXXXXXX.X b,c _Xg
gene_type	list of biotypes
gene_status e	{KNOWN, NOVEL, PUTATIVE}
gene_name	string
transcript_type d	list of biotypes
transcript_status d,e	{KNOWN, NOVEL, PUTATIVE}
transcript_name d	string
exon_number f	indicates the biological position of the exon in the transcript
exon_id f	ENSEXXXXXXXXXXX.X b _Xg
level
'''

i = 0
with gzip.open(file1, "r") as f1, open(file2, "w") as f2, open("genelist.txt", "w") as f3:
	f2.write("[")
	f3.write("#gene\tgeneID\tpk\n")
	for line in f1:
		if line.startswith("#"):continue
		chrom, source, feature, start, end, score, strand, phase, info = line.strip().split("\t")
		
		if feature != "gene":continue
		i += 1
		info_obj = Comment_obj(info)
		
		f2.write(r'{"fields": {"geneName":' + info_obj.getvalue("gene_name") + r', "end": ' + end + r', "start": '+ start + r', "geneID":' + info_obj.getvalue("gene_id").split(".")[0] + r'", "chrom":' + str(chr_dict[chrom]) + r', "geneStatus":' + info_obj.getvalue("gene_status") + r', "level":' + info_obj.getvalue("level") + r', "geneType":' + info_obj.getvalue("gene_type") + r', "strand":"' + strand  + r'", "genome": 1'  + r'}, "model": "basepedia.genecode", "pk": ' + str(pk_list[i]) + r'}, ')
		f3.write(info_obj.getvalue("gene_name").strip('"') + "\t"+ info_obj.getvalue("gene_id").strip('"') +"\t"+ str(pk_list[i]) + "\n")
	f2.write("]")
	
