#!/usr/bin/env python
#-*-coding:utf-8-*-

import os, sys

file1 = sys.argv[1]
file2 = sys.argv[2]

gene_dict = {}
with open(file1, "r") as f1:
    for line in f1:
        if line.startswith("#"):continue
            geneID, genename, pk = line.rstrip("\n").split("\t")
	
            gene_dict[geneID.split(".")[0]] = [genename, pk]

#print gene_dict
with open(file2, "r") as f2, open("cogenelist.txt", "w") as f3:
    for line in f2:
	if line.startswith("#"):continue
	geneID1, geneID2, score = line.rstrip("\n").split("\t")

        if geneID1 in gene_dict and geneID2 in gene_dict:
            f3.write("\t".join([geneID1,] + gene_dict[geneID1] + [geneID2,] + gene_dict[geneID2] + [score,]) + "\n")

    	else:
            print(line)



