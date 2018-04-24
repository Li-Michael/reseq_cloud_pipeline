import sys
annotype = sys.argv[1]
refannofile  = sys.argv[2]
genome   = sys.argv[3]


if annotype == "gtf":
	cmd0 = "/home/rongzhengqin/bin/tools/gtfToGenePred -genePredExt -geneNameAsName2 "
elif annotype == "gff":
	cmd0 = "/home/rongzhengqin/bin/tools/gff3ToGenePred"

cmd = """%s %s reference.ucsc.txt
awk '{print 1"\\t"$0}' reference.ucsc.txt > test.ens.gene.txt
awk -F "\\t" '{if($4!=".") print $0}' test.ens.gene.txt > ref_ucsc.txt
rm -rf test
mkdir test
mv ref_ucsc.txt ./test/test_ensGene.txt
/opt/software/annovar/retrieve_seq_from_fasta.pl test/test_ensGene.txt -seqfile %s -format ensGene -outfile test/test_ensGeneMrna.fa
"""%(cmd0,refannofile,genome)
print cmd



