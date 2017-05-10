#!/usr/bin/env python
#-*-coding:utf-8-*-

'''
# TP53	chr17	7665053	7683550	
[{"fields": {"end": 7683550, "start": 7665053, "gene": "TP53", "genomeID": "hg38", "chromosome": "chr17"}, "model": "basepedia.locus", "pk": 1}]
将上面全部转成json格式，并一起放在[]中

{"fields": {"start": 123, "geneName": "gg1", "end": 1234, "chrom": 1, "geneID": "gene1"}, "model": "rest.genecode", "pk": 1}, 
'''

import sys,os
import gzip
import random

file1 = sys.argv[1]
file2 = sys.argv[2]

'''
class Comment_obj(object):
    def __init__(self, comment):
        self.comment = comment
		
    def getvalue(self, key):
        attr = self.comment.split(key, 1)
        return {True: attr[-1].split(';')[0].strip(), False: "-"}[len(attr) >= 2]
'''

chr_dict = {"chr1":1, "chr2":2, "chr3":3, "chr4":4, "chr5":5, "chr6":6, "chr7":7, "chr8":8, "chr9":9, "chr10":10, "chr11":11, "chr12":12, "chr13":13, "chr14":14, "chr15":15, "chr16":16, "chr17":17, "chr18":18, "chr19":19, "chr20":20, "chr21":21, "chr22":22,"chrX":23, "chrY":24, "chrM":25, "chrx":23, "chry":24, "chrm":25}

i = 0
with open(file1, "r") as f1, open(file2, "w") as f2:
    
    f2.write("[")
    for line in f1:
        if line.startswith("#"):continue
	geneID1, genename1, pk1, geneID2, genename2, pk2, score = line.rstrip("\n").split("\t")
	
        i +=1
        f2.write(r'{"fields": {"node1": ' + pk1 + r', "node2": ' + pk2 + r', "attr": "Co-expression"}, "model": "rest.contact", "pk": ' + str(i) + r'},')
    f2.write("]")
	
