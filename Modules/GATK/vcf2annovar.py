import os,sys
import commands

vcfs = sys.argv[1:]
if vcfs:pass
else:
	sys.stderr.write("[INFO] No vcf found!\n")
	exit(1)
for vcf in vcfs:
	if not vcf.endswith(".vcf"):
		sys.stderr.write("[ERROR] Error to parse file: '%s',please use vcf file"%vcf)

	status,perlpath = commands.getstatusoutput("which perl")
	sys.stderr.write("[INFO] File transfer: %s\n"%vcf)
	status,output = commands.getstatusoutput("%s /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/GATK/convert2annovar.pl  -format vcf4old %s -include -outfile %s.fmt"%(perlpath,vcf,vcf))
	#input_prefix = os.path.splitext(vcf)[0]
	#status2, stdout = commands.getstatusoutput("cat %s.fmt2 > %s.fmt && rm -f %s.fmt2" %(vcf,vcf,vcf))
sys.stderr.write("[INFO] All File transferred Done.\n")
sys.stderr.write("[INFO] All File format Done.\n")
exit(0)

