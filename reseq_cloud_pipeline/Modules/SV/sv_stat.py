#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys

files = sys.argv[1:]

#deletion duplication
samples = [ os.path.basename(f).split(".")[0] for f in files ]
print samples
types = ["CTX", "DEL", "INS", "INV", "ITX"]
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
			stat[fname][line.split("\t")[6]] += 1

with open("sv.stat.xls", "w") as f2:
	f2.write("#samples\t"+"\t".join(sorted(types))+ "\tTotal" "\n")
	for sample in samples:
		f2.write("\t".join([sample,]+[ str(stat[sample][typ]) for typ in sorted(types) ] + [str(reduce(lambda x,y:x+y,[stat[sample][typ] for typ in sorted(types) ]))]) + "\n")	
