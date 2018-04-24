#!/opt/bio/perl/bin/perl -w
use strict;

use File::Basename;
use Cwd qw(fast_abs_path);
use Getopt::Long qw(:config posix_default no_ignore_case pass_through);
use FindBin qw($Bin);
use lib "$Bin/";
use PlotPie;


my ($filter_stat, $sample, $svg);
GetOptions(
        "filter_stat=s"      =>      \$filter_stat,
        "sample=s"           =>      \$sample,
        "svg=s"              =>      \$svg,
);

if(!$filter_stat || !$sample || !$svg){
	die;
}
open IN,"$filter_stat";
my $svg_src = "$svg.src";
open OUT,">$svg_src";
my %hash;
while(<IN>){
	chomp;
	my @tmp = split(/\t/, $_);
	if(/^Number of Reads/){
		$tmp[2] = ($tmp[2] == 0) ? 0.1 : $tmp[2];
		$hash{C} = "Clean Reads\t$tmp[2]";
	}
	elsif(/^Discard Reads related to N/){
		$tmp[1] = ($tmp[1] == 0) ? 0.1 : $tmp[1];
		$hash{N} = "N\t$tmp[1]";
	}
	elsif(/^Discard Reads related to low qual/){
		$tmp[1] = ($tmp[1] == 0) ? 0.1 : $tmp[1];
		$hash{L} = "Low Quality\t$tmp[1]";
	}
	elsif(/^Discard Reads related to Adapter/){
		$tmp[1] = ($tmp[1] == 0) ? 0.1 : $tmp[1];
		$hash{A} = "Adapter\t$tmp[1]";
	}
}
close IN;
print OUT<<END;
QC of raw reads($sample)
$hash{N}
$hash{A}
$hash{L}
$hash{C}
END
close OUT;
plotPie($svg_src, $svg, "100");
my $png = $svg;
$png =~ s/.svg$/.png/g;
system("convert -density 300 $svg $png");

