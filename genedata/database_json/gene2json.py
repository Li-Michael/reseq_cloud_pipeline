#!/usr/bin/env python
#-*-coding:utf-8-*-

'''
# TP53	chr17	7665053	7683550	
[{"fields": {"end": 7683550, "start": 7665053, "gene": "TP53", "genomeID": "hg38", "chromosome": "chr17"}, "model": "basepedia.locus", "pk": 1}]
将上面全部转成json格式，并一起放在[]中
'''

import sys
i = 3
with open(sys.argv[1], "r") as f1, open(sys.argv[2], "w") as f2, open("genelist.txt", "w") as f3:
	f2.write("[")
	for line in f1:
		i += 2 
		if line.startswith("#"):continue
		gene,chromosome,start,end, genomeID = line.strip().split("\t")

		f2.write(r'{"fields": {"end": ' + end + r', "start": '+ start + r', "gene": "' + gene + r'", "genomeID": "' + genomeID + r'", "chromosome": "' + chromosome + r'"}, "model": "basepedia.locus", "pk": ' + str(i) + r'}, ')
			
	f2.write("]")

