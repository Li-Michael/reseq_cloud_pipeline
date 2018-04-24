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
	`mkdir -p $outdir`;
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	#foreach my $lane(keys %{$input->{bam_list}->{$sample}} ){
	#`mkdir -p $outdir/$sample/$lane`;
	open SH,">$shdir/PCA.$group.sh" or die"cant open SH to write";
	print SH<<END;
echo start PCA $group at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\
export PYTHONPATH=/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/software/python2.7/bin/:/usr/bin/:/usr/bin/:/usr/bin/python2.7-config/:/usr/lib/python2.7/:/etc/python2.7/:/etc/python/:/usr/local/lib/python2.7/:/usr/include/python2.7:/usr/share/python:/home/lee/.local/lib/python2.7/site-packages/django/core/:/home/rongzhengqin/.local/lib/python2.7/site-packages/django:\$PYTHONPATH:/home/rongzhengqin/lib:/home/rongzhengqin/software/anaconda2/envs/gbcloud/lib/python2.7
export PATH=/home/rongzhengqin/software/anaconda2/bin:/opt/bio/hisat2-2.0.4:/opt/bio/samtools-1.3:/opt/bio/breakdancer-1.1.2/cpp:/opt/bin:/home/rongzhengqin/.local/lib/python2.7/site-packages/django/bin:\$JAVA_HOME/bin:\$ANT_HOME/bin:\$PYTHONPATH:\$PATH
export LD_LIBRARY_PATH=\$PYTHONPATH:/home/rongzhengqin/lib:/its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib:/opt/lib:/opt/lib64/:/opt/intel/mkl/lib/intel64/:/opt/boost/usr/lib64/:/opt/boost/usr/lib:\$LD_LIBRARY_PATH:\$PERL5LIB:\$R_LIBS:\$HOME/software/CNVnator_v0.3.3/src/yeppp-1.0.0/binaries/linux/x86_64:\$ROOTSYS/lib:/home/rongzhengqin/R/x86_64-unknown-linux-gnu-library/3.1/

cd $outdir && \\
$Bin/$config->{software}->{'vcftools'}->{cmd} $soft_paras->{'vcftools'} --vcf $input->{cohort_list}->{$group} --plink --out $outdir/$group && \\
$Bin/$config->{software}->{'plink'}->{cmd} $soft_paras->{'plink'} --file $outdir/$group --out $outdir/$group  && \\
#gcta --bfile tmp --make-grm --autosome --out tmp
$Bin/$config->{software}->{'gcta'}->{cmd} --bfile $outdir/$group --make-grm --out $outdir/$group  && \\
#gcta --grm tmp --pca 3 --out pcatmp
$Bin/$config->{software}->{'gcta'}->{cmd} $soft_paras->{'gcta'} --grm $outdir/$group --pca 3 --out $outdir/pca.$group  && \\
sed -i '1i\\1 2 eigenvector1 eigenvector2 eigenvector3' $outdir/pca.$group.eigenvec
python $Bin/$config->{software}->{'PCA_plot'}->{cmd} $outdir/pca.$group.eigenvec && \\

echo finish PCA $group  at $time && \\
echo finish &> $shdir/PCA.$group.sh.ok
END
	close SH;
	$jobs{"$shdir/PCA.$group.sh"} = 1;
	#print LIST<<END;
#$outdir/$sample/$sample.stat
#END
	#push some file into out_json for the next module
	$out_json->{result}->{pca_stat}->{$group} = "$outdir/$group/pca.$group.eigenvec";
	$out_json->{result}->{pca_fig}->{$group}->{"svg"} = "$outdir/$group/pca.$group.svg";
	$out_json->{result}->{pca_fig}->{$group}->{"png"} = "$outdir/$group/pca.$group.png";
	#}
	#close LIST;
}

## generate out json file ##
generate_json($out_json, "$jsondir/pca.json");

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "PCA");
}


# step 2:
foreach my $group(keys %{$input->{cohort_list}}){
	open SH,">$shdir/report.sh";
	print SH<<END;
echo start prepare report at $time && \\

cd $reportdir && \\
ln -s $outdir/pca.$group.eigenvec .
ln -s $outdir/pca.$group.png .
ln -s $outdir/pca.$group.svg .

echo finish report at $time && \\
echo finish &> $shdir/report.sh.ok
END
	close SH;
	$jobs{"$shdir/report.sh"} = 1;

}
#push some file into out_json for the next module
#$out_json->{result}->{vcf_list} = "$outdir/cohort.vcf";
	
## generate out json file ##
#generate_json($out_json, "$jsondir/GATK.cohort.json");

if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "1G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "PCA");
}

