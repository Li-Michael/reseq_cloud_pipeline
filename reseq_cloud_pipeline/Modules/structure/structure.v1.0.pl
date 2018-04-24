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
my ($step, $total_step) = (0, 1);

# generate shell script for each step
#my ($seqType, $qualSys, $outType);
foreach my $group(keys %{$input->{cohort_list}}){
	`mkdir -p $outdir/`;
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#`mkdir -p $outdir/$sample/$lane`;
	open SH,">$shdir/structure.$group.sh" or die"cant open SH to write";
	print SH<<END;
echo start structure $group at $time && \\
export PYTHONPATH=/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/software/python2.7/bin/:/usr/bin/:/usr/bin/:/usr/bin/python2.7-config/:/usr/lib/python2.7/:/etc/python2.7/:/etc/python/:/usr/local/lib/python2.7/:/usr/include/python2.7:/usr/share/python:/home/lee/.local/lib/python2.7/site-packages/django/core/:/home/rongzhengqin/.local/lib/python2.7/site-packages/django:\$PYTHONPATH:/home/rongzhengqin/lib:/home/rongzhengqin/software/anaconda2/envs/gbcloud/lib/python2.7
export PATH=/home/rongzhengqin/software/anaconda2/bin:/opt/bio/hisat2-2.0.4:/opt/bio/samtools-1.3:/opt/bio/breakdancer-1.1.2/cpp:/opt/bin:/home/rongzhengqin/.local/lib/python2.7/site-packages/django/bin:\$JAVA_HOME/bin:\$ANT_HOME/bin:\$PYTHONPATH:\$PATH
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$PYTHONPATH:/home/rongzhengqin/lib:/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/lib:/opt/lib64/:/opt/intel/mkl/lib/intel64/:/opt/boost/usr/lib64/:/opt/boost/usr/lib:\$LD_LIBRARY_PATH:\$PERL5LIB:\$R_LIBS:\$HOME/software/CNVnator_v0.3.3/src/yeppp-1.0.0/binaries/linux/x86_64:\$ROOTSYS/lib:/home/rongzhengqin/R/x86_64-unknown-linux-gnu-library/3.1/ && \\

cd $outdir && \\
$Bin/$config->{software}->{'vcftools'}->{cmd} $soft_paras->{'vcftools'} --vcf $input->{cohort_list}->{$group} --plink --out $outdir/$group && \\
$Bin/$config->{software}->{'plink'}->{cmd} $soft_paras->{'plink'} --file $outdir/$group --out $outdir/$group  && \\
#% for K in 1 2 3 4 5; do admixture --cv $outdir/$group/$group.ped \$K | tee log\${K}.out; done
for K in \$(seq 1 8);do  $Bin/$config->{software}->{'admixture'}->{cmd} $soft_paras->{'admixture'} $outdir/$group.bed \$K | tee $outdir/log\${K}.out; done  && \\
grep -h CV $outdir/log*.out > $outdir/CV.log && \\
/home/rongzhengqin/software/anaconda2/bin/python /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/structure/plotstructure.py $group  && \\

echo finish structure $group  at $time && \\
echo finish &> $shdir/structure.$group.sh.ok
END
	close SH;
	$jobs{"$shdir/structure.$group.sh"} = 1;
	#print LIST<<END;
#$outdir/$sample/$sample.stat
#END
	#push some file into out_json for the next module
	$out_json->{result}->{structure_list}->{$group}->{"P"} = "$outdir/$group/$group.P";
	$out_json->{result}->{structure_list}->{$group}->{"Q"} = "$outdir/$group/$group.Q";
	#}
	#close LIST;
}

## generate out json file ##
generate_json($out_json, "$jsondir/structure.json");

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 2, $main_paras->{project_id}, $main_paras->{project_version}, "structure");
}

=pod
# step 2:
my ($allgvcf, $samples);
foreach my $sample(keys %{$input->{bam_list}}){
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#$lane = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.dup.g.vcf";	
		$allgvcf .= " -V "."$outdir/$sample/$sample.bwa.sort.dup.g.vcf";
		$samples .=" ".$sample	
}
	open SH,">$shdir/cohort.all.sh";
	print SH<<END;
echo start cohort_calling $samples at $time && \\
#/opt/software/lib/jvm/java-1.8.0-openjdk-1.8.0.65-0.b17.el6_7.x86_64/bin/java  -Xmx35G -jar GenomeAnalysisTK.jar  -T GenotypeGVCFs -nt 1 -nct 1 -R hg38.fa --dbsnp dbsnp_144.hg38.vcf.gz -V DB195.bwa.sort.dedup.g.vcf -V DB.g.vcf -L chr23.interval_list
java -Xmx30G -jar $Bin/$config->{software}->{'GATK GenotypeGVCFs'}->{cmd} $soft_paras->{'GATK GenotypeGVCFs'} -R $main_paras->{reference_genome} $allgvcf -o $outdir/cohort.all.vcf && \\

echo finish cohort stat at $time && \\
echo finish &> $shdir/cohort.all.sh.ok
END
	close SH;
	$jobs{"$shdir/cohort.all.sh"} = 1;


#push some file into out_json for the next module
$out_json->{result}->{vcf_list} = "$outdir/cohort.vcf";
	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.cohort.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "30G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}


# step 3:
	open SH,">$shdir/cohort.selectVariants.sh";
	print SH<<END;
echo start cohort_select_variants at $time && \\
java -Xmx4G -jar $Bin/$config->{software}->{'GATK SNP'}->{cmd} $soft_paras->{'GATK SNP'} -selectType SNP -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.snp.vcf && \\
java -Xmx4G -jar $Bin/$config->{software}->{'GATK INDEL'}->{cmd} $soft_paras->{'GATK INDEL'} -selectType INDEL -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.indel.vcf && \\
#java -Xmx4g -jar $Bin/$config->{software}->{'GATK filterSNP'}->{cmd} $soft_paras->{'GATK filterSNP'} -R $main_paras->{reference_genome} --variant $outdir/cohort.snp.vcf --mask $outdir/cohort.indel.vcf --out $outdir/cohot.snp.filter.vcf
java -Xmx4g -jar $Bin/$config->{software}->{'GATK filterSNP'}->{cmd} $soft_paras->{'GATK filterSNP'} -R $main_paras->{reference_genome} --variant $outdir/cohort.snp.vcf --mask $outdir/cohort.indel.vcf --out $outdir/cohot.snp.filter.vcf
echo finish cohort_select_variants at $time && \\
echo finish &> $shdir/cohort.selectVariants.sh.ok
END
	close SH;
	$jobs{"$shdir/cohort.selectVariants.sh"} = 1;

#push some file into out_json for the next module
$out_json = ();
$out_json->{result}->{vcf_list}->{SNP} = "$outdir/cohort.snp.vcf";
$out_json->{result}->{vcf_list}->{SNP} = "$outdir/cohort.snp.filter.vcf";
	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.cohort.snp_indel.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}
=cut
