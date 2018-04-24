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
my ($step, $total_step) = (0, 3);

# generate shell script for each step
#my ($seqType, $qualSys, $outType);
foreach my $sample(keys %{$input->{bam_list}}){
	`mkdir -p $outdir/$sample`;
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#`mkdir -p $outdir/$sample/$lane`;
	open SH,">$shdir/cnv.$sample.sh" or die"cant open SH to write";
	print SH<<END;
echo start CNV-calling $sample at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH:/home/rongzhengqin/software/root/lib:/home/rongzhengqin/software/CNVnator_v0.3.3/src/yeppp-1.0.0/binaries/linux/x86_64 && \\

$Bin/$config->{software}->{'CNVnator extractreads'}->{cmd} -root $outdir/$sample/$sample.root -genome $main_paras->{'reference_genome'} $soft_paras->{'CNVnator extractreads'} -tree $input->{bam_list}->{$sample}  && \\
$Bin/$config->{software}->{'CNVnator his'}->{cmd} -root $outdir/$sample/$sample.root $soft_paras->{'CNVnator his'}  && \\
$Bin/$config->{software}->{'CNVnator stat'}->{cmd} -root $outdir/$sample/$sample.root $soft_paras->{'CNVnator stat'}  && \\
$Bin/$config->{software}->{'CNVnator partition'}->{cmd} -root $outdir/$sample/$sample.root $soft_paras->{'CNVnator partition'}  && \\
$Bin/$config->{software}->{'CNVnator call'}->{cmd} -root $outdir/$sample/$sample.root $soft_paras->{'CNVnator call'} > $outdir/$sample/$sample.cnv.txt && \\
sed -i '1i\#CNV_type\\tcoordinates\\tCNV_size\\tnormalized_RD\\te-val1\\te-val2\\te-val3\\te-val4\\tq0' $outdir/$sample/$sample.cnv.txt  && \\

echo finish CNV-calling $sample  at $time && \\
echo finish &> $shdir/cnv.$sample.sh.ok
END
	close SH;
	$jobs{"$shdir/cnv.$sample.sh"} = 1;
	
	#push some file into out_json for the next module
	$out_json->{result}->{cnv_list}->{$sample} = "$outdir/$sample/$sample.cnv.txt";
}

## generate out json file ##
generate_json($out_json, "$jsondir/cnv.json");

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "CNV");
}

# step 2:
#foreach my $sample(keys %{$input->{bam_list}}){
	open SH,">$shdir/cnv.stat.sh";
	print SH<<END;
echo start cnv stat at $time && \\

cd $outdir && \\
$Bin/$config->{software}->{'stat'}->{cmd} $soft_paras->{'stat'} .\/*\/\*.cnv.txt && \\

echo finish cnv stat at $time && \\
echo finish &> $shdir/cnv.stat.sh.ok
END
	close SH;
	$jobs{"$shdir/cnv.stat.sh"} = 1;


#push some file into out_json for the next module
$out_json->{result}->{cnv_stat} = "$outdir/cnv.stat.xls";
	
## generate out json file ##
generate_json($out_json, "$jsondir/cnv.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "2G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "CNV");
}

=pod
# step 3:
	open SH,">$shdir/cohort.selectVariants.sh";
	print SH<<END;
echo start cohort_select_variants at $time && \\
java -Xmx4G -jar $Bin/$config->{software}->{'GATK SNP'}->{cmd} $soft_paras->{'GATK SNP'} -selectType SNP -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.snp.vcf && \\
java -Xmx4G -jar $Bin/$config->{software}->{'GATK INDEL'}->{cmd} $soft_paras->{'GATK INDEL'} -selectType INDEL -R $main_paras->{reference_genome} --variant $outdir/cohort.all.vcf -o $outdir/cohort.indel.vcf && \\
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
$out_json->{result}->{vcf_list}->{INDEL} = "$outdir/cohort.indel.vcf";
	
## generate out json file ##
generate_json($out_json, "$jsondir/GATK.cohort.snp_indel.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "GATK");
}
=cut
