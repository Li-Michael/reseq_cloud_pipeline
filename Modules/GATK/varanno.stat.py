#/* Prog Description:
#* ######...   ...######
#* Author: Rong Zheng-Qin
#* Email: zju3351689@gmail.com || rongzhengqin@genomics.org.cn
#* 2013-04-08 15:55:30
#*/

"=================Modules Load==============="
import sys
import re
"=================Format Define==============="

"=============Func and Class Define==========="

"====================Script==================="
samplename_arr = []
count = 0
hash_variant_function = {}
hash_exonic_variant_function = {}
sample_numbers = len(sys.argv)-2
gene_anno_type = sys.argv[-1]
for i in xrange(1,len(sys.argv)-1):
	count += 1
	samplename = sys.argv[i].split("/")[-1].split(".")[0]
	samplename_arr.append(samplename.split("_vs_")[0])
	variant_function = file(sys.argv[i]+"."+gene_anno_type+".variant_function","r")
	exonic_variant_function = file(sys.argv[i]+"."+gene_anno_type+".exonic_variant_function","r")
	for line in variant_function:
		type_arr = line.split("\t")[0].split(";")
		for k in xrange(len(type_arr)):
			type = type_arr[k]
			if hash_variant_function.has_key(type):
				hash_variant_function[type][i-1] += 1
			else:
				hash_variant_function[type] = [0]*sample_numbers
				hash_variant_function[type][i-1] += 1
	for line in exonic_variant_function:
		type_arr = line.split("\t")[1].split(";")
		for k in xrange(len(type_arr)):
			type = type_arr[k]
			if hash_exonic_variant_function.has_key(type):
				hash_exonic_variant_function[type][i-1] += 1
			else:
				hash_exonic_variant_function[type] = [0]*sample_numbers
				hash_exonic_variant_function[type][i-1] += 1
print "##Mutation Annotation result"
print "#Annotation\t"+"\t".join(samplename_arr)
for type in hash_variant_function.iterkeys():
	print type+"\t"+"\t".join(map(str,hash_variant_function[type]))
for type in hash_exonic_variant_function.iterkeys():
	print type + "\t" + "\t".join(map(str,hash_exonic_variant_function[type]))




