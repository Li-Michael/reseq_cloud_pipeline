#!/opt/bio/perl/bin/perl -w

use strict;
use Getopt::Long;
use File::Basename;
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

my $time = q{`date +%F' '%H:%M`};
my (%jobs, %run_jobs);

################# above this line is settled code #################

# must set the total_step of the module
my ($step, $total_step) = (0, 3);














