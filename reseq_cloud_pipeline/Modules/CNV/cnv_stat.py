#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys

files = sys.argv[1:]

#deletion duplication
samples = [ os.path.basename(f).split(".")[0] for f in files ]
print samples
types = ["deletion", "duplication"]
stat = {}

for sample in samples:
	for tt in types:
		if sample not in stat:
			stat[sample] = {}
		stat[sample][tt] = 0

for f in files:
	fname = os.path.basename(f).split(".")[0]
	with open(f, "r") as f1:
		for line in f1:
			if line.startswith("#"):continue
			stat[fname][line.split("\t")[0]] += 1

with open("cnv.stat.xls", "w") as f2:
	f2.write("#cnv_type\t"+"\t".join(sorted(samples))+ "\n")
	for typ in types:
		f2.write("\t".join([typ,]+[ str(stat[sample][typ]) for sample in sorted(samples) ]) + "\n")	
	
	total = [] 
	for sample in sorted(samples):
		total.append(reduce(lambda x,y:str(x+y), [stat[sample][typ] for typ in types ]))
	f2.write("Total\t"+"\t".join(total)+"\n")

