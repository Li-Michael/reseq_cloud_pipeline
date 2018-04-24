#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys, os
import pysam
#import bamio
#import mutilstats

def coverage_cal(mergedregionlen,send,qstart,qend,add=1):
	# must use sorted bam
	# send is last pos for  end of now cover
	# qstart qend is alignment blocks subarr   [ )  0 - based 
	if send >= qend:pass
	else:
		mergedregionlen = mergedregionlen + qend - max(send,qstart)
		send = qend
	return mergedregionlen,send

## cal coverage 
def bam_aln_cover(sortbamfile):
	samfile = pysam.Samfile( sortbamfile, "rb" )
	reflen = sum(samfile.lengths)
	mergedregionlen = {}
	send            = {}
	mappedreads_samtools = samfile.mapped	# use mapped reads ( porper align and MAPQ>=20 )
	mappedreads = 0
	totalreads = 0
	hchr = {}
	refcalled = 0 
	for alignread in samfile:
		totalreads +=1
		if alignread.is_secondary:continue
		if alignread.is_unmapped: continue
		mappedreads += 1
		#for qstart,qend in alignread.blocks:
		# 	mergedregionlen,send = bamio.coverage_cal(mergedregionlen,send,qstart,qend)
		if alignread.reference_id in mergedregionlen:
			mergedregionlen[alignread.reference_id],send[alignread.reference_id] = coverage_cal(mergedregionlen[alignread.reference_id],send[alignread.reference_id],alignread.reference_start,alignread.reference_end)
		else:
			mergedregionlen[alignread.reference_id] = 0
			send[alignread.reference_id]   = 0
			mergedregionlen[alignread.reference_id],send[alignread.reference_id] = coverage_cal(mergedregionlen[alignread.reference_id],send[alignread.reference_id],alignread.reference_start,alignread.reference_end)
	#rlen = alignread.rlen
		refcalled += alignread.reference_length		# can use like mergedregionlen to get each chrom depth
	summergedregionlen = sum(mergedregionlen.values())
	coverage_rate = summergedregionlen * 1.0/reflen*100
	## use mergedregionlen and samfile.lengths  can  call each chrom coverage
	return totalreads,mappedreads,summergedregionlen,refcalled*1.0/summergedregionlen,"%.3f"%coverage_rate

## use annotation for call  chips Capture efficiency

from GBCloud.processJson import *
from GBCloud.autoRun import *

## decode json ##
jsonConfigFile = sys.argv[1]
obj = getJson(jsonConfigFile)
inputObj = obj['input']
#configObj = obj['config']
outputObj = obj['output']
## get output ##
outDir, shDir,	reportDir, jsonDir = getOutput(outputObj)

# argv2
#sorttypebam = sys.argv[2]
#assert sorttypebam in ["bowtie","bowtie2","tophat","tophat2","bwa"]

# mapping quality stat result
fout = open(os.path.join(outDir,"MappingQC_stat.xls"),"w")
fout.write("##Reads mapping coverage and depth summary:\n")
fout.write("#Samplename\tRaw Reads\tMapped Reads\tDepth(X)\tCovered_region(bp)\tCoverage_Rate\n")

sufbam = ".bwa.sort.bam"
for sample,value in inputObj["cleandata_multiple_lanes"].items():
	#print sample, value
	sys.stderr.write("[INFO] process %s\n"%(sample))
	fn1 = os.path.join(outDir, sample, sample + sufbam)
	totalreads,mappedreads,coverbp,depth,coverage_rate = bam_aln_cover(fn1)
	fout.write("\t".join(map(str,[sample,totalreads,mappedreads, "%.3f"%depth, coverbp, coverage_rate]))+"\n")
fout.close()

