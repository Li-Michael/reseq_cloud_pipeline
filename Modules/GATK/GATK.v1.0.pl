#!/opt/bio/perl/bin/perl -w

use strict;
use Getopt::Long;
use File::Basename;
use PerlIO::gzip;
use FindBin '$Bin';
use GBCloud;
use AutoRun;

die $! if @ARGV < 1;

## decode json ##
my $obj = get_json(@ARGV);
my $input = $obj->{input};
my $config = $obj->{config};
my $output = $obj->{output};

## get output ##
my ($outdir, $shdir, $reportdir, $jsondir) = get_output($output);

## get config ##
my ($main_paras, $soft_paras) = get_config($config);

## init out_json ##
my $out_json;

my $time = q{`date +%F'  '%H:%M`};
my (%jobs, %run_jobs);

################# above this line is settled code #################

# must set the total_step of the module
my ($step, $total_step) = (0, 8);


# generate shell script for each step
# step 1:
#my ($stat_samples, $stat_files);
%jobs=();
foreach my $sample(keys %{$input->{bam_list}}){
	`mkdir -p $outdir/$sample`;
	foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){  
		`mkdir -p $outdir/$sample/$lane`;	
		open SH,">$shdir/dup.$sample.${lane}.sh" or die"cant open duplicate SH to write";
		print SH<<END;
echo start duplicate_bam $sample at $time && \\
java -Xmx8G -jar $Bin/$config->{software}->{'picard mark_duplicates'}->{cmd} $soft_paras->{'picard mark_duplicates'} I=$input->{bam_list}->{$sample}->{$lane} O=$outdir/$sample/$lane/$sample.${lane}.bwa.sort.dup.bam M=$outdir/$sample/$lane/marked_dup_metrics.txt && \\
$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$lane/$sample.${lane}.bwa.sort.dup.bam && \\

echo finish duplication $sample $lane at $time && \\
echo finish &> $shdir/dup.$sample.${lane}.sh.ok
END
		close SH;
		$jobs{"$shdir/dup.$sample.${lane}.sh"} = 1;
	}
}

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "8G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 2:
# merge bam  %jobs=();
foreach my $sample(keys %{$input->{bam_list}}){
	my @lanes = keys %{$input->{bam_list}->{$sample}};
	foreach my $lane(@lanes){
		$lane = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.dup.bam";
	}   
	if($#lanes){
		my $lanes = join(" ",@lanes);
		open SH,">$shdir/merge.$sample.sh" or die"cant open merge SH to write";
		print SH<<END;
echo start merge_bam $sample at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

$Bin/$config->{software}->{'samtools merge'}->{cmd} $soft_paras->{'samtools merge'} -c -p $outdir/$sample/$sample.bwa.sort.dup.bam $lanes  && \\
$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$sample.bwa.sort.dup.bam && \\

echo finish merge $sample bam at $time && \\
echo finish &> $shdir/merge.$sample.sh.ok
END
	close SH; 
	$jobs{"$shdir/merge.$sample.sh"} = 1;

   # push some file into out_json for the next module
	$out_json->{result}->{bam_list}->{$sample} = "$outdir/$sample/$sample.bwa.sort.dup.bam";
}
	# samples have not lanes, ln -s $sample.$lane.bwa.sort.bam ../
	else{
		open SH,">$shdir/merge.$sample.sh";
		print SH<<END;
echo start merge "ln -s bam" $sample at $time && \\
ln -s $lanes[0] $outdir/$sample/$sample.bwa.sort.dup.bam
$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$sample.bwa.sort.dup.bam && \\
 
echo finish merge $sample stat at $time && \\
echo finish &> $shdir/merge.$sample.sh.ok
END

		close SH;
		$jobs{"$shdir/merge.$sample.sh"} = 1;

		# push some file into out_json for the next module
		$out_json->{result}->{bam_list}->{$sample} = "$outdir/$sample/$sample.bwa.sort.dup.bam";
	}
}
 
## generate out json file ##
generate_json($out_json, "$jsondir/merge_bam.json");
 
if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 2, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 3
#my ($seqType, $qualSys, $outType);
foreach my $sample(keys %{$input->{bam_list}}){
	`mkdir -p $outdir/$sample`;
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#`mkdir -p $outdir/$sample/$lane`;
	open SH,">$shdir/HC.$sample.sh" or die"can\'t open HC SH to write";
	print SH<<END;
echo start HC-calling snp/indel $sample at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

java -Xmx10G -jar $Bin/$config->{software}->{'GATK HC'}->{cmd} $soft_paras->{'GATK HC'} -R $main_paras->{reference_genome} -I $outdir/$sample/$sample.bwa.sort.dup.bam -o $outdir/$sample/$sample.bwa.sort.dup.g.vcf && \\
echo finish HC-calling snp/indel $sample  at $time && \\
echo finish &> $shdir/HC.$sample.sh.ok
END
	close SH;
	$jobs{"$shdir/HC.$sample.sh"} = 1;
	
	#push some file into out_json for the next module
	$out_json->{result}->{gVCF_list}->{$sample} = "$outdir/$sample/$sample.bwa.sort.dup.g.vcf";
}


# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "10G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}

# step 4:
my ($allgvcf, $samples);
foreach my $sample(keys %{$input->{bam_list}}){
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#$lane = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.dup.g.vcf";	
		$allgvcf .= " -V "."$outdir/$sample/$sample.bwa.sort.dup.g.vcf";
		$samples .=" ".$sample	
}
	open SH,">$shdir/cohort.all.sh" or die"cant open cohort SH to write";
	print SH<<END;
echo start cohort_calling $samples at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

#/opt/software/lib/jvm/java-1.8.0-openjdk-1.8.0.65-0.b17.el6_7.x86_64/bin/java  -Xmx35G -jar GenomeAnalysisTK.jar  -T GenotypeGVCFs -nt 1 -nct 1 -R hg38.fa --dbsnp dbsnp_144.hg38.vcf.gz -V DB195.bwa.sort.dedup.g.vcf -V DB.g.vcf -L chr23.interval_list
java -Xmx30G -jar $Bin/$config->{software}->{'GATK GenotypeGVCFs'}->{cmd} $soft_paras->{'GATK GenotypeGVCFs'} -R $main_paras->{reference_genome} $allgvcf -o $outdir/cohort.all.vcf && \\

echo finish cohort stat at $time && \\
echo finish &> $shdir/cohort.all.sh.ok
END
	close SH;
	$jobs{"$shdir/cohort.all.sh"} = 1;


#push some file into out_json for the next module
$out_json->{result}->{cohort_vcf} = "$outdir/cohort.vcf";
	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.cohort.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "30G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 5:
# filter cohort vcf
	open SH,">$shdir/cohort.selectVariants.sh" or die"cant open selectVariants SH to write";
	print SH<<END;
echo start cohort_select_variants at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

java -Xmx4G -jar $Bin/$config->{software}->{'GATK SNP'}->{cmd} $soft_paras->{'GATK SNP'} -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.snp.vcf && \\
java -Xmx4G -jar $Bin/$config->{software}->{'GATK INDEL'}->{cmd} $soft_paras->{'GATK INDEL'} -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.indel.vcf && \\
#java -Xmx4g -jar $Bin/$config->{software}->{'GATK filterINDEL'}->{cmd} $soft_paras->{'GATK filterINDEL'} -R $main_paras->{reference_genome} --variant $outdir/cohort.snp.vcf --mask $outdir/cohort.indel.vcf --out $outdir/cohot.snp.filter.vcf && \\
java -Xmx4g -jar $Bin/$config->{software}->{'GATK filterSNP'}->{cmd} $soft_paras->{'GATK filterSNP'} -R $main_paras->{reference_genome} --variant $outdir/cohort.snp.vcf --mask $outdir/cohort.indel.vcf --out $outdir/cohort.snp.filter.vcf && \\
echo finish cohort_select_variants at $time && \\
echo finish &> $shdir/cohort.selectVariants.sh.ok
END
	close SH;
	$jobs{"$shdir/cohort.selectVariants.sh"} = 1;

#push some file into out_json for the next module
#$out_json = ();
$out_json->{result}->{vcf_list}->{SNP} = "$outdir/cohort.snp.vcf";
$out_json->{result}->{vcf_list}->{SNP_filter} = "$outdir/cohort.snp.filter.vcf";
$out_json->{result}->{vcf_list}->{INDEL} = "$outdir/cohort.indel.vcf";
#$out_json->{result}->{vcf_list}->{INDEL_filter} = "$outdir/cohort.indel.filter.vcf";
	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.cohort.snp_indel.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 6:
# annovar - filter cohort vcf
	open SH,">$shdir/annovar_gtfgff.sh" or die"cant open annovar_gtfgff SH to write\n";
	print SH<<END;
echo start gtfgff - annovar at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:/home/rongzhengqin/software/anaconda2/envs/gbcloud/lib/python2.7:\$LD_LIBRARY_PATH && \\

$Bin/$config->{software}->{'gtfToGene'}->{cmd} $soft_paras->{'gtfToGene'} -genePredExt -geneNameAsName2  $main_paras->{reference_gtf}  $outdir/reference.ucsc.txt && \\
awk \'{print 1\"\\t\"\$0}\' $outdir/reference.ucsc.txt > $outdir/test.ens.gene.txt && \\
awk -F \"\\t\" \'{if(\$4!=\".\") print \$0}\' $outdir/test.ens.gene.txt > $outdir/ref_ucsc.txt && \\
rm -rf $outdir/test && mkdir $outdir/test && \\
mv $outdir/ref_ucsc.txt $outdir/test/test_ensGene.txt  && \\
$Bin/$config->{software}->{'retrieve_seq_from_fasta'}->{cmd}  $outdir/test/test_ensGene.txt -seqfile $main_paras->{reference_genome} -format ensGene -outfile $outdir/test/test_ensGeneMrna.fa && \\

$Bin/$config->{software}->{'mergepop_GATK'}->{cmd} $outdir/cohort.snp.filter.vcf snp.filter.vcf && \\
$Bin/$config->{software}->{'mergepop_GATK'}->{cmd} $outdir/cohort.indel.vcf  indel.vcf && \\

python $Bin/$config->{software}->{'convert2annovar'}->{cmd} $soft_paras->{'convert2annovar'}  $outdir/cohort.snp.filter.vcf  && \\
$Bin/$config->{software}->{'table_annovar'}->{cmd} $soft_paras->{'table_annovar'}  $outdir/cohort.snp.filter.vcf.fmt $outdir/test/ -buildver test -protocol ensGene -operation g   \\

python $Bin/$config->{software}->{'convert2annovar'}->{cmd} $soft_paras->{'convert2annovar'}  $outdir/cohort.indel.vcf  && \\
$Bin/$config->{software}->{'table_annovar'}->{cmd} $soft_paras->{'table_annovar'}  $outdir/cohort.indel.vcf.fmt $outdir/test/ -buildver test -protocol ensGene -operation g   \\

echo finish gtfgff-annovar at $time && \\
echo finish &> $shdir/annovar_gtfgff.sh.ok
END
	close SH;
	$jobs{"$shdir/annovar_gtfgff.sh"} = 1;

#push some file into out_json for the next module
#$out_json->{result}->{vcf_list}->{INDEL_filter} = "$outdir/cohort.indel.filter.vcf";
	
## generate out json file ##
#generate_json($out_json, "$jsondir/GATK.cohort.snp_indel.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 7
# annotation
foreach my $sample(keys %{$input->{bam_list}}){
	#`mkdir -p $outdir/$sample`;
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#`mkdir -p $outdir/$sample/$lane`;
	open SH,">$shdir/annovar.$sample.sh" or die"can\'t open annovar SH to write";
	print SH<<END;
echo start annovar $sample at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

$Bin/$config->{software}->{'convert2annovar'}->{cmd} $soft_paras->{'convert2annovar'}  $outdir/$sample.snp.filter.vcf  -include -outfile $outdir/$sample.snp.filter.vcf.fmt && \\
$Bin/$config->{software}->{'table_annovar'}->{cmd} $soft_paras->{'table_annovar'}  $outdir/$sample.snp.filter.vcf.fmt $outdir/test/ -buildver test -protocol ensGene -operation g   \\

$Bin/$config->{software}->{'convert2annovar'}->{cmd} $soft_paras->{'convert2annovar'}  $outdir/$sample.indel.vcf  -include -outfile $outdir/$sample.indel.vcf.fmt && \\
$Bin/$config->{software}->{'table_annovar'}->{cmd} $soft_paras->{'table_annovar'}  $outdir/$sample.indel.vcf.fmt $outdir/test/ -buildver test -protocol ensGene -operation g  \\

echo finish annotation snp/indel $sample  at $time && \\
echo finish &> $shdir/annovar.$sample.sh.ok
END
	close SH;
	$jobs{"$shdir/annovar.$sample.sh"} = 1;
	
	#push some file into out_json for the next module
	#$out_json->{result}->{gVCF_list}->{$sample} = "$outdir/$sample/$sample.bwa.sort.dup.g.vcf";
}


# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "2G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}



# step 8:
# annovar - filter cohort vcf
	open SH,">$shdir/annovar_stat.sh" or die"cant open annovar_stat SH to write\n";
	print SH<<END;
echo start stat - annovar at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:/home/rongzhengqin/lib:\$LD_LIBRARY_PATH && \\
export PYTHONPATH=/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/software/python2.7/bin/:/usr/bin/:/usr/bin/:/usr/bin/python2.7-config/:/usr/lib/python2.7/:/etc/python2.7/:/etc/python/:/usr/local/lib/python2.7/:/usr/include/python2.7:/usr/share/python:/home/lee/.local/lib/python2.7/site-packages/django/core/:/home/rongzhengqin/.local/lib/python2.7/site-packages/django:\$PYTHONPATH:/home/rongzhengqin/lib:/home/rongzhengqin/software/anaconda2/envs/gbcloud/lib/python2.7
export PATH=/home/rongzhengqin/software/anaconda2/bin:/opt/bio/hisat2-2.0.4:/opt/bio/samtools-1.3:/opt/bio/breakdancer-1.1.2/cpp:/opt/bin:/home/rongzhengqin/.local/lib/python2.7/site-packages/django/bin:\$JAVA_HOME/bin:\$ANT_HOME/bin:\$PYTHONPATH:\$PATH
#export CLASSPATH=/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:\$PERL5LIB:\$JAVA_HOME/lib:\$JAVA_HOME/jre/lib:\$ANT_HOME/lib:/opt/software/picard-2.0.1/dist/:\$R_LIBS:/home/rongzhengqin/R/x86_64-unknown-linux-gnu-library/3.1/:\$CLASSPATH:\$PYTHONPATH
export LD_LIBRARY_PATH=\$PYTHONPATH:/home/rongzhengqin/lib:/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/lib:/opt/lib64/:/opt/intel/mkl/lib/intel64/:/opt/boost/usr/lib64/:/opt/boost/usr/lib:\$LD_LIBRARY_PATH:\$PERL5LIB:\$R_LIBS:\$HOME/software/CNVnator_v0.3.3/src/yeppp-1.0.0/binaries/linux/x86_64:\$ROOTSYS/lib:/home/rongzhengqin/R/x86_64-unknown-linux-gnu-library/3.1/

## snp stat
which python && \\
echo \$PYTHONPATH && \\
cd $outdir && \\
/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'mut_sub_pattern'}->{cmd} *.snp.filter.vcf.fmt && \\
/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'varanno.stat'}->{cmd} *.snp.filter.vcf.fmt ensGene > SNP.anno.stat.xls && \\
/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'plot_varanno'}->{cmd} SNP.anno.stat.xls && \\
ls Annotation_Type_stat.* | while read i; do mv \${i} SNP_\${i} ;done  && \\

## InDel stat
#/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'mut_sub_pattern'}->{cmd} *.indel.vcf.fmt && \\
#/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'varanno.stat'}->{cmd} *.indel.vcf.fmt ensGene > INDEL.anno.stat.xls && \\
#/home/rongzhengqin/software/anaconda2/bin/python $Bin/$config->{software}->{'plot_varanno'}->{cmd} INDEL.anno.stat.xls && \\
#ls Annotation_Type_stat.* | while read i; do mv \${i} INDEL_\${i} ;done  && \\


echo finish annovar-stat at $time && \\
echo finish &> $shdir/annovar_stat.sh.ok
END
	close SH;
	$jobs{"$shdir/annovar_stat.sh"} = 1;

#push some file into out_json for the next module
$out_json->{result}->{snp_stat} = "$outdir/SNP.anno.stat.xls";
#$out_json->{result}->{snp_stat_pic} = "$outdir/SNP.anno.stat.xls";

	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.snp_indel.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "1G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


