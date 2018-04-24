#!/opt/bio/perl/bin/perl -w
use strict;

my ($list, $outfile) = @ARGV;
open OUT, ">$outfile";
open LIST, "$list";

my %hash;
while(<LIST>){
	chomp;
	next if(/^#/);
	my $stat_file = $_;
	open IN,"$stat_file";
	while(<IN>){
		chomp;
		next if($_ =~ /^Type/ || $_ =~ /^\s*$/);
		my @tmp = split(/\t/, $_);
		if($tmp[0] =~ /\%/){
			$hash{$tmp[0]}[0] += 1;
		}
		else{
			$hash{$tmp[0]}[0] = 1;
		}
		for (my $i = 1; $i < @tmp; $i++){
			$hash{$tmp[0]}[$i] += $tmp[$i];
		}
	}
	close IN;
}
print OUT "Type\tRaw data\tClean data\n";
foreach my $key(sort keys %hash){
	print OUT "$key";
	for (my $j = 1; $j < @{$hash{$key}}; $j++){
		my $avg = $hash{$key}[$j] / $hash{$key}[0];
		if($avg =~ /\./){
			$avg = sprintf("%.2f", $avg);
		}
		print OUT "\t$avg";
	}
	print OUT "\n";
}
close OUT;

