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
	open SH,">$shdir/phylogene.sh" or die"cant open SH to write";
	print SH<<END;
echo start phylogenetic tree  at $time && \\
export LD_LIBRARY_PATH=/opt/bio/local/lib:\$LD_LIBRARY_PATH && \\

cd $outdir/
$Bin/$config->{software}->{'SNPhylo'}->{cmd} $soft_paras->{'SNPhylo'} -v $input->{cohort_list}->{group1} 

echo finish phylognetic tree at $time && \\
echo finish &> $shdir/phylogene.sh.ok
END
	close SH;
	$jobs{"$shdir/phylogene.sh"} = 1;
	#print LIST<<END;
	
	#push some file into out_json for the next module
	$out_json->{result}->{nw_tree}->{'ml'} = "$outdir/snphylo.output.ml.tree";
	$out_json->{result}->{nw_tree}->{'bs'} = "$outdir/snphylo.output.bs.tree";
	$out_json->{result}->{tree_fig}->{'ml'} = "$outdir/snphylo.output.ml.pdf";
	$out_json->{result}->{tree_fig}->{'bs'} = "$outdir/snphylo.output.bs.pdf";
	
	#close LIST;

## generate out json file ##
generate_json($out_json, "$jsondir/phylogenetic_tree.json");

# auto run function for each step
# main_paras->{run} is auto run flag; 'FALSE' means only generate script; 'TRUE' means auto run the module
if($main_paras->{run} eq "TRUE"){
	$step += 1;
	# shdir, %jobs, %run_jobs, step, total_step, vf, num_proc, project_id, project_version, module_name
	# only modify the 'vf', 'threads' and 'module_name'
	run_cloud($shdir, \%jobs, \%run_jobs, $step, $total_step, "4G", 1, $main_paras->{project_id}, $main_paras->{project_version}, "phylogene");
}

