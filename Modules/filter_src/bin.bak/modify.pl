#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin qw($Bin);
use File::Basename;
use Cwd qw(abs_path);

my ($path,$key,$N,$Q,$p,$type,$memory,$output,$help,%info,$total,$num,$rate);
#$N||=0.05;
#$Q||="10,0.5";
#$p ||= 0;"N:s"=>\$N, "Q:s"=>\$Q, "A:f"=>\$p,
$type = "PE";
GetOptions(
  "path:s"=>\$path,"key:s"=>\$key, "type:s"=>\$type, "output:s"=>\$output, "help|?"=>\$help,);
usage() if(!defined $path  || !defined $key|| defined $help);
my $new_key = basename($key);
$new_key =~ s/_1\.fq\.gz//;
$key=$new_key;
open BSSQ, "<$path/Basic_Statistics_of_Sequencing_Quality.txt" or die $!;
open OUT, ">$output.stat" or die $!;
open SFR, "<$path/Statistics_of_Filtered_Reads.txt" or die $!;

modify();


sub modify
{
	if ($type eq "SE") {print OUT "--------------\t".$key ."_1.fq.gz\n";}else{print OUT "--------------\ttotal\t$key\_1.fq.gz\t$key\_2.fq.gz\n";}
	while (<BSSQ>) 
	{
		next if (/^\s*$/);
		s/\(%\)//g;
		s/%//g;
		s/\(/\t/g;
		s/\)/\t/g;
		s/\t+/\t/g;
		my @tab = split/\t+/,$_;
		for (my $i=0;$i < @tab ;$i++) { $tab[$i] =~ s/\s+$//; $tab[$i] =~ s/^\s+//;}
		if (/^Read\s*length/) 
		{
			if ($type eq "SE") {$info{"len"} = $tab[1] . "\n";}else{$info{"len"} = $tab[2] . "+" . $tab[4] ."\t" . $tab[2] . "\t" . $tab[4] . "\n";}
			next;
		}elsif(/^Total\s*number\s*of\s*reads/)
		{
			if ($type eq "SE") 
			{
				print OUT "total treads\t$tab[3]\n";
				$info{"clean reads"} = "clean reads :\t$tab[3]\t";
				$total = $tab[1];
				$info{"rawN"} = $total;
				$info{"raw_reads"} = "total reads\t$total\n";;
			}else
			{
				$total  = $tab[3] + $tab[7];
				my $clean = $total/2;
				$info{"clean reads"} = "clean reads :\t$clean\t";
				print OUT "total reads\t$tab[3]\t$tab[3]\t$tab[7]\n";
				$total  = $tab[1] + $tab[5];
				$info{"rawN"} = $total/2;
				$info{"raw_reads"} = "total reads\t$tab[1]\t$tab[1]\t$tab[5]\n";
			}
			$info{"total reads before filter"} = "filter step info:\ntotal reads before filter  :\t". $info{"rawN"}. "\n";
			next;
		}elsif(/^Total\s*number\s*of\s*bases/)
		{
			if ($type eq "SE") 
			{
				print OUT "total reads nt\t$tab[3]\n";
				$info{"raw_reads_nt"} = "total reads nt\t$tab[1]\n";;
			}else
			{
				$total  = $tab[3] + $tab[7];
				print OUT "total reads nt\t$total\t$tab[3]\t$tab[7]\n";
				$total  = ($tab[1] + $tab[5]);
				$info{"raw_reads_nt"} = "total reads nt\t$total\t$tab[1]\t$tab[5]\n";
			}
			print OUT "reads len\t" . $info{"len"};next;
		}elsif(/^Number\s*of\s*filtered\s*bases/)
		{
				$info{"filterNum"} = $tab[1];
				$info{"filterR"} = $tab[2];
				my $cleanR = 100-$info{"filterR"};
				$info{"clean reads"} .= $cleanR . "%\n";next;
		}elsif(/^Number of base C/)
		{
			if ($type eq "SE") 
			{
				$info{"clean_GC"} = $tab[3];
				$info{"clean_GC_R"} = $tab[4];
				$info{"raw_GC"} = $tab[1];
				$info{"raw_GC_R"} = $tab[2];
			}else
			{
				$info{"clean_GC_1"} = $tab[3];
				$info{"clean_GC_2"} = $tab[7];
				$info{"clean_GC_1_R"} = $tab[4];
				$info{"clean_GC_2_R"} = $tab[8];
				$info{"raw_GC_1"} = $tab[1];
				$info{"raw_GC_2"} = $tab[5];
				$info{"raw_GC_1_R"} = $tab[2];
				$info{"raw_GC_2_R"} = $tab[6];
			}
			next;
		}elsif(/^Number of base G/)
		{
			if ($type eq "SE") 
			{
				$info{"clean_GC"} += $tab[3];
				$info{"clean_GC_R"} += $tab[4];
				$info{"raw_GC"} += $tab[1];
				$info{"raw_GC_R"} += $tab[2];
				$num = $info{"clean_GC"};
				$rate = $info{"clean_GC_R"};
				$info{"clean_GC_num"} = "GC  number\t" . $num . "\n";
				$info{"clean_GC_rate"} = "GC  percentage\t" . $rate ."%\n";
				$num = $info{"raw_GC"};
				$rate = $info{"raw_GC_R"};
				$info{"raw_GC_num"} = "GC  number\t" . $num .  "\n";
				$info{"raw_GC_rate"} = "GC  percentage\t" . $rate . "%\n";
			}else
			{
				$info{"clean_GC_1"} += $tab[3];
				$info{"clean_GC_2"} += $tab[7];
				$info{"clean_GC_1_R"} += $tab[4];
				$info{"clean_GC_2_R"} += $tab[8];
				$info{"raw_GC_1"} += $tab[1];
				$info{"raw_GC_2"} += $tab[5];
				$info{"raw_GC_1_R"} += $tab[2];
				$info{"raw_GC_2_R"} += $tab[6];
			
			$num = $info{"clean_GC_1"} + $info{"clean_GC_2"};
			$rate = sprintf "%0.2f", ($info{"clean_GC_1_R"} + $info{"clean_GC_2_R"})/2;
			$info{"clean_GC_num"} = "GC  number\t" . $num . "\t" . $info{"clean_GC_1"} . "\t" . $info{"clean_GC_2"} . "\n";
			$info{"clean_GC_rate"} = "GC  percentage\t" . $rate . "%\t" . $info{"clean_GC_1_R"} . "%\t" . $info{"clean_GC_2_R"} . "%\n";
			$num = $info{"raw_GC_1"} + $info{"raw_GC_2"};
			$rate = sprintf "%0.2f", ($info{"raw_GC_1_R"} + $info{"raw_GC_2_R"})/2;
			$info{"raw_GC_num"} = "GC  number\t" . $num . "\t" . $info{"raw_GC_1"} . "\t" . $info{"raw_GC_2"} . "\n";
			$info{"raw_GC_rate"} = "GC  percentage\t" . $rate . "%\t" . $info{"raw_GC_1_R"} . "%\t" . $info{"raw_GC_2_R"} . "%\n";
			}
			next;
		}elsif(/^Number of base N/)
		{
			if ($type eq "SE") 
			{
				$info{"clean_N"} = $tab[3];
				$info{"clean_N_R"} = $tab[4];
				$info{"raw_N"} = $tab[1];
				$info{"raw_N_R"} = $tab[2];
				$num = $info{"clean_N"};
				$rate = $info{"clean_N_R"}; 
				$info{"clean_N_num"} = "N  number\t" . $num . "\n";
				$info{"clean_N_rate"} = "N  percentage\t" . $rate . "%\n";
				$num = $info{"raw_N"} ;
				$rate = $info{"raw_N_R"} ;
				$info{"raw_N_num"} = "N  number\t" . $num . "\n";
				$info{"raw_N_rate"} = "N  percentage\t" . $rate . "%\n";
			}else
			{
				$info{"clean_N_1"} = $tab[3];
				$info{"clean_N_2"} = $tab[7];
				$info{"clean_N_1_R"} = $tab[4];
				$info{"clean_N_2_R"} = $tab[8];
				$info{"raw_N_1"} = $tab[1];
				$info{"raw_N_2"} = $tab[5];
				$info{"raw_N_1_R"} = $tab[2];
				$info{"raw_N_2_R"} = $tab[6];
				$num = $info{"clean_N_1"} + $info{"clean_N_2"};
				$rate = sprintf "%0.2f", ($info{"clean_N_1_R"} + $info{"clean_N_2_R"})*0.5; 
				$info{"clean_N_num"} = "N  number\t" . $num . "\t" . $info{"clean_N_1"} . "\t" . $info{"clean_N_2"} . "\n";
				$info{"clean_N_rate"} = "N  percentage\t" . $rate . "%\t" . $info{"clean_N_1_R"} . "%\t" . $info{"clean_N_2_R"} . "%\n";
				$num = $info{"raw_N_1"} + $info{"raw_N_2"};
				$rate = sprintf "%0.2f", ($info{"raw_N_1_R"} + $info{"raw_N_2_R"})*0.5;
				$info{"raw_N_num"} = "N  number\t" . $num . "\t" . $info{"raw_N_1"} . "\t" . $info{"raw_N_2"} . "\n";
				$info{"raw_N_rate"} = "N  percentage\t" . $rate . "%\t" . $info{"raw_N_1_R"} . "%\t" . $info{"raw_N_2_R"} . "%\n";
			}
			next;
		}elsif(/^Number of base calls with quality value of 20 or higher/)
		{
			if ($type eq "SE") 
			{
				$info{"clean_Q20"} = $tab[5];
				$info{"clean_Q20_R"} = $tab[6];
				$info{"raw_Q20"} = $tab[3];
				$info{"raw_Q20_R"} = $tab[4];
				$num = $info{"clean_Q20"};
				$rate = $info{"clean_Q20_R"};
				$info{"clean_Q20_num"} = "Q20  number\t" . $num. "\n";
				$info{"clean_Q20_rate"} = "Q20  percentage\t" . $rate . "%\n";
				$num = $info{"raw_Q20"};
				$rate = $info{"raw_Q20_R"} ;
				$info{"raw_Q20_num"} = "Q20  number\t" . $num. "\n";
				$info{"raw_Q20_rate"} = "Q20  percentage\t" . $rate .  "%\n";
			}else
			{
				$info{"clean_Q20_1"} = $tab[5];
				$info{"clean_Q20_2"} = $tab[9];
				$info{"clean_Q20_1_R"} = $tab[6];
				$info{"clean_Q20_2_R"} = $tab[10];
				$info{"raw_Q20_1"} = $tab[3];
				$info{"raw_Q20_2"} = $tab[7];
				$info{"raw_Q20_1_R"} = $tab[4];
				$info{"raw_Q20_2_R"} = $tab[8];
				$num = $info{"clean_Q20_1"} + $info{"clean_Q20_2"};
				$rate = sprintf "%0.2f",  ($info{"clean_Q20_1_R"} + $info{"clean_Q20_2_R"})/2+0.005;
				$info{"clean_Q20_num"} = "Q20  number\t" . $num . "\t" . $info{"clean_Q20_1"} . "\t" . $info{"clean_Q20_2"} . "\n";
				$info{"clean_Q20_rate"} = "Q20  percentage\t" . $rate . "%\t" . $info{"clean_Q20_1_R"} . "%\t" . $info{"clean_Q20_2_R"} . "%\n";
				$num = $info{"raw_Q20_1"} + $info{"raw_Q20_2"};
				$rate = sprintf "%0.2f", ($info{"raw_Q20_1_R"} + $info{"raw_Q20_2_R"})/2+0.005;
				$info{"raw_Q20_num"} = "Q20  number\t" . $num . "\t" . $info{"raw_Q20_1"} . "\t" . $info{"raw_Q20_2"} . "\n";
				$info{"raw_Q20_rate"} = "Q20  percentage\t" . $rate . "%\t" . $info{"raw_Q20_1_R"} . "%\t" . $info{"raw_Q20_2_R"} . "%\n";
			}
			print OUT $info{"clean_Q20_num"};
			print OUT $info{"clean_Q20_rate"};
			print OUT $info{"clean_GC_num"};
			print OUT $info{"clean_GC_rate"};
			print OUT $info{"clean_N_num"};
			print OUT $info{"clean_N_rate"}."\n\n";
			if ($type eq "SE") 
			{print OUT "before filter\n--------------\t".$key ."_1.fq.gz\n";}
			else{print OUT "before filter\n--------------\ttotal\t$key\_1.fq.gz\t$key\_2.fq.gz\n";}
			print OUT $info{"raw_reads"} . $info{"raw_reads_nt"} . "reads len\t" . $info{"len"} . $info{"raw_Q20_num"} . $info{"raw_Q20_rate"} .$info{"raw_GC_num"} . $info{"raw_GC_rate"} .  $info{"raw_N_num"} . $info{"raw_N_rate"} . "\n\n" . $info{"total reads before filter"} . "\n";
			last;
		}
	}
	while (<SFR>) 
	{
		next if(/^\s*$/);
		s/\(%\)//g;
		s/%//g;
		s/\(/\t/g;
		s/\)/\t/g;
		s/\t+/\t/g;
		my @tab = split/\t+/,$_;
		for (my $i=0;$i < @tab ;$i++) { $tab[$i] =~ s/\s+$//; $tab[$i] =~ s/^\s+//;}
		$total = $info{"rawN"}; 
		if (/^Reads with adapter/) 
		{
			if ($type eq "SE") {$rate = sprintf "%0.2f", $tab[1]/$total*100;print OUT "1,filter adapter <y/n> : y\t" . $tab[1] . "\t" . $rate. "%\n";next;}
			$num = ($tab[1] - 2* $tab[3])/2;
			my $rate1 = sprintf "%0.2f", $tab[3]/$total*100;
			$rate = sprintf "%0.2f", $num/$total*100;
			print OUT "1,filter adapter <y/n> : y\t" . $tab[3] . "\t" . $rate1 . "%\t" . $num . "\t" . $rate . "%\n";
		}elsif(/^Reads with low quality/)
		{
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			if($type eq "SE"){ my $b = sprintf "%0.2f", $tab[1]/$total*100; $info{"lowQ"} = "6, filter low quality\t" . $tab[1] .  "\t" .$b."%\n";next;}
			my $new = $tab[1]/2;
			$info{"lowQ"} = "6, filter low quality\t" . $new .  "\t" .$rate."%\n" ;
		}elsif(/^Reads with low mean quality/)
		{
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			if($type eq "SE") {my $b= sprintf "%0.2f", $tab[1]/$total*100;$info{"lowMQ"} = "7, filter low average quality\t" . $tab[1] . "\t" . $b."%\n";next;}
			my $new = $tab[1]/2;
			$info{"lowMQ"} = "7, filter low average quality\t" . $new . "\t" . $rate."%\n";
		}elsif(/^Reads with duplications/)
		{
			my $new = $tab[1]/2;
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			if($type eq "SE") {my $b= sprintf "%0.2f", $tab[1]/$total*100;$info{"dup"} = "8, filter duplications\t\t" . $tab[1] . "\t" . $b."%\n";next;}
			$info{"dup"} = "8, filter duplications\t" . $new . "\t" .$rate."%\n";
		}elsif(/^Read with n rate exceed/)
		{
			my $new = $tab[1]/2;
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			if($type eq "SE") 
			{
				my $b= sprintf "%0.2f", $tab[1]/$total*100; 
				$info{"N"} = "4, filter N\t" . $tab[1] . "\t" .$b."%\n";next;
			}
			$info{"N"} = "4, filter N \t" . $new . "\t" .$rate."%\n";
		}elsif(/^Read with small insert size/)
		{
			my $new = $tab[1]/2;
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			if($type eq "SE") 
			{
				my $b= sprintf "%0.2f", $tab[1]/$total*100;
				$info{"insert"} = "2,filter small instert size\t" . $tab[1] . "\t" .$b."%\n";
				next;
			}
			$info{"insert"} = "2,filter small instert size\t" . $new .  "\t" .$rate."%\n";
		}elsif(/^Reads with PolyA /)
		{
			my $new = $tab[1]/2;
			$rate =  sprintf "%0.2f", $tab[1]/$total/2*100;
			$info{"polyA"} = "5, filter poly A\t" . $new .  "\t" .$rate."%\n";
			if($type eq "SE") {my $b= sprintf "%0.2f", $tab[1]/$total*100;$info{"polyA"} = "5, filter poly A\t" . $tab[1] . "\t" .$b."%\n";}
			print OUT $info{"insert"};
			print OUT "3, trimed reads\t0\t0.00%\n";
			print OUT $info{"N"} . $info{"polyA"} .$info{"lowQ"} .  $info{"lowMQ"}  . $info{"dup"};
			print OUT $info{"clean reads"};
		}
	}
}
close OUT;
close BSSQ;
close SFR;
exit 0;


sub usage{
  die qq/
Usage: modify.pl  [options]
            used to modify the result of SOAPnuke
Options: -path <s>   the result of SOAPnuke stat files
         -type <s>            set the sequencing type, which can be  "SE" or "PE", default is [PE] 
         -output  <s>    output prefix
          -key  <s>   origin fq1 name
         -help|?           help information
\n/;
}



=pod
         -N  <f>    filter reads which the high N rate, default [0.05]
         -Q  <s>    (low quality,low quality rate) (0~50,0~1) (<=,>), default [10,0.5]
         -A  <f>         filter poly A, percent of A, 0 means do not filter (default: [0])
=cut


