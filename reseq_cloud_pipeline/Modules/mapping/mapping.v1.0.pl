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
# step 1
# my ($seqType, $qualSys, $outType);
foreach my $sample(keys %{$input->{cleandata_multiple_lanes}}){
	`mkdir -p $outdir/$sample`;
	open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	foreach my $lane(keys %{$input->{cleandata_multiple_lanes}->{$sample}} ){
		`mkdir -p $outdir/$sample/$lane`;
		open SH,">$shdir/bwa.$sample.$lane.sh" or die "cant open SH to write\n";
		print SH<<END;
echo start mapping $sample $lane at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

$Bin/$config->{software}->{'bwa mem'}->{cmd} $soft_paras->{'bwa mem'} -M -R '\@RG\\tID:BasePedia\\tPL:illumina\\tPU:${lane}\\tLB:sequence\\tSM:${sample}' $main_paras->{reference_genome}  $input->{cleandata_multiple_lanes}->{$sample}->{$lane}->[0]  $input->{cleandata_multiple_lanes}->{$sample}->{$lane}->[1] | $Bin/$config->{software}->{'samtools sort'}->{cmd} $soft_paras->{'samtools sort'} - -o $outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam  && \\
#$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam && \\

echo finish mapping $sample $lane at $time && \\
echo finish &> $shdir/bwa.$sample.$lane.sh.ok
END
		close SH;
		$jobs{"$shdir/bwa.$sample.$lane.sh"} = 1;
		print LIST<<END;
$outdir/$sample/$lane/$lane.stat
END
		# push some file into out_json for the next module
		$out_json->{result}->{bam_list}->{$sample}->{$lane} = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam";
	}
	close LIST;
}

## generate out json file ##
generate_json($out_json, "$jsondir/bam_list.json");

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "8G", 4, $main_paras->{project_id}, $main_paras->{project_version}, "mapping");
}


# step 2:
# merge bam  %jobs=();
foreach my $sample(keys %{$input->{cleandata_multiple_lanes}}){
	my @lanes = keys %{$input->{cleandata_multiple_lanes}->{$sample}};
	foreach my $lane(@lanes){
		$lane = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam";
	}
	if($#lanes){
		my $lanes = join(" ",@lanes);
		open SH,">$shdir/merge.$sample.sh" or die"cant open merge SH to write";
		print SH<<END;
echo start merge_bam $sample at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

$Bin/$config->{software}->{'samtools merge'}->{cmd} $soft_paras->{'samtools merge'} -c -p $outdir/$sample/$sample.bwa.sort.bam $lanes  && \\             
$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$sample.bwa.sort.bam && \\
 
echo finish merge $sample bam at $time && \\
echo finish &> $shdir/merge.$sample.sh.ok
END
	close SH;
	$jobs{"$shdir/merge.$sample.sh"} = 1;

}
	# samples have not lanes, ln -s $sample.$lane.bwa.sort.bam ../
	else{
		open SH,">$shdir/merge.$sample.sh";
	    print SH<<END;
echo start merge "ln -s bam" $sample at $time && \\
ln -s $lanes[0] $outdir/$sample/$sample.bwa.sort.bam 
$Bin/$config->{software}->{'samtools index'}->{cmd} $soft_paras->{'samtools index'} $outdir/$sample/$sample.bwa.sort.bam && \\
 
echo finish merge $sample stat at $time && \\
echo finish &> $shdir/merge.$sample.sh.ok
END

		close SH;
		$jobs{"$shdir/merge.$sample.sh"} = 1;
 
		# push some file into out_json for the next module
		$out_json->{result}->{bam_list}->{$sample} = "$outdir/$sample/$sample.bwa.sort.dup.bam";
	}
}

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 2, $main_paras->{project_id}, $main_paras->{project_version}, "mapping");
}


# step3:
# generate shell script for mapping QC
#foreach my $sample(keys %{$input->{cleandata_multiple_lanes}}){	
#}
#my @samples = keys %{$input->{cleandata_multiple_lanes}};
#foreach my $sample(@samples){
#	$sample = "$outdir/$sample/$sample.bwa.sort.bam";
#}
#my $samples = join(" ",@samples);

	open SH,">$shdir/mappingQC.sh" or die "can\'t open mappingQC SH to write\n";
	print SH<<END;
echo start MappingQC at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\
python $Bin/$config->{software}->{'mappingQC'}->{cmd} $output->{workspace}/@ARGV  && \\

cd $reportdir && \\
ln -s $outdir/MappingQC_stat.xls . && \\
echo finish MappingQC at $time && \\
echo finish &> $shdir/mappingQC.sh.ok
END

	close SH;
	$jobs{"$shdir/mappingQC.sh"} = 1;

# push some file into out_json for the next module
$out_json->{result}->{"map_stat"} = "$outdir/mappingQC_stat.xls";

## generate out json file ##
generate_json($out_json, "$jsondir/bam_list.json");


# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "mapping");
}


=pod
#step 2:
# generate shell script for mapping QC
#my ($seqType, $qualSys, $outType);
foreach my $sample(keys %{$input->{cleandata_multiple_lanes}}){
	#open LIST,">$outdir/$sample/$sample.stat.list"or die "open LIST failed $!\n";
	foreach my $lane(keys %{$input->{cleandata_multiple_lanes}->{$sample}} ){
		open SH,">$shdir/stats.$sample.$lane.sh" or die"cant open SH to write";
		print SH<<END;
echo start stat $sample $lane at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\
$Bin/$config->{software}->{'samtools flagstat'}->{cmd} $soft_paras->{'samtools flagstat'} $outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam > $outdir/$sample/$lane/$sample.${lane}.flagstat && \\
$Bin/$config->{software}->{'samtools stats'}->{cmd} $soft_paras->{'samtools stats'} $outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam > $outdir/$sample/$lane/$sample.${lane}.stats && \\
echo finish stats $sample $lane at $time && \\
echo finish &> $shdir/stats.$sample.$lane.sh.ok
END
		close SH;
		$jobs{"$shdir/stats.$sample.$lane.sh"} = 1;
#$outdir/$sample/$lane/$lane.stat
END
		# push some file into out_json for the next module
		#$out_json->{result}->{bam_list_multiple_lanes}->{$sample}->{$lane} = "$outdir/$sample/$lane/$sample.${lane}.bwa.sort.bam";
	}
	close LIST;
}

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	# count the step
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, threads, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "2G", 2, $main_paras->{project_id}, $main_paras->{project_version}, "mapping");
}

=cut
