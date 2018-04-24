#!/opt/bio/perl/bin/perl -w

use strict;
use Getopt::Long;
use Cwd qw(abs_path fast_abs_path);
use FindBin '$Bin';
use File::Basename;

my ($infiles,$samples,$outfile,$help_flag);
GetOptions("infiles:s"=>\$infiles,"samples:s"=>\$samples,"outfile:s"=>\$outfile,"help"=>\$help_flag);
if(!defined $infiles || !defined $samples || !defined $outfile || defined $help_flag){
	die;
}

my %hash;
my @files = split(/,/, $infiles);
my @sams = split(/,/, $samples);
for my $i(0..$#files){
	open IN,"$files[$i]";
###################################################
# Type    Raw data        Clean data              #
# Number of Reads 24688652        22851396        #
# Data Size       2468865200      2285139600      #
# N of fq1        23216   15320                   #
# N of fq2        35772   16594                   #
# GC(%) of fq1    49.88   49.91                   #
# GC(%) of fq2    50.08   50.03                   #
# Q20(%) of fq1   98.92   99.23                   #
# Q20(%) of fq2   96.56   96.84                   #
# Q30(%) of fq1   97.25   97.62                   #
# Q30(%) of fq2   93.09   93.32                   #
# Discard Reads related to N      1896            #
# Discard Reads related to low qual       0       #
# Discard Reads related to Adapter        1835360 #
###################################################
	while(<IN>){
		chomp;
		my @tmp = split(/\t/, $_);
		if(@tmp == 3){
			$hash{$tmp[0]}{$sams[$i]}{raw} = $tmp[1];
			$hash{$tmp[0]}{$sams[$i]}{clean} = $tmp[2];
		}
	}
	close IN;
}
open OUT,">$outfile";
print OUT "Sample\tRaw Data(GB)\tClean Data(GB)\tClean Data Ratio(%)\tClean Data Q20(%)\tClean Data Q30(%)\tGC Content(%)\n";
for my $sam(@sams){
	my $clean_ratio = sprintf("%.2f", 100 * $hash{"Data Size"}{$sam}{clean} / $hash{"Data Size"}{$sam}{raw});
	$hash{"Data Size"}{$sam}{raw} = sprintf("%.2f", $hash{"Data Size"}{$sam}{raw} / 1024 / 1024 / 1024);
	$hash{"Data Size"}{$sam}{clean} = sprintf("%.2f", $hash{"Data Size"}{$sam}{clean} / 1024 / 1024 / 1024);
	$hash{"Q20"}{$sam}{clean} = sprintf("%.2f", ($hash{"Q20(%) of fq1"}{$sam}{clean} + $hash{"Q20(%) of fq2"}{$sam}{clean}) / 2);
	$hash{"Q30"}{$sam}{clean} = sprintf("%.2f", ($hash{"Q30(%) of fq1"}{$sam}{clean} + $hash{"Q30(%) of fq2"}{$sam}{clean}) / 2);
	$hash{"GC"}{$sam}{clean} = sprintf("%.2f", ($hash{"GC(%) of fq1"}{$sam}{clean} + $hash{"GC(%) of fq2"}{$sam}{clean}) / 2);
	print OUT join("\t", $sam, $hash{"Data Size"}{$sam}{raw}, $hash{"Data Size"}{$sam}{clean}, $clean_ratio, $hash{"Q20"}{$sam}{clean}, $hash{"Q30"}{$sam}{clean}, $hash{"GC"}{$sam}{clean})."\n";
}
close OUT;

