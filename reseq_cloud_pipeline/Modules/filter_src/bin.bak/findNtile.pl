#!/usr/bin/perl -w
use strict;
use warnings;

=head1 NAME

findNtile.pl - This script is used to find out 'Tile Number' (Illumina) or 'FOV Number' (BGISEQ-500) from FASTQ file(s), which contains high 'N' proportion at one or more positions of reads. 

=head1 SYNOPSIS

findNtile.pl [options] --fq1 CL200003395_L01_16_1.fq.gz --fq2 CL200003395_L01_16_2.fq.gz

=head1 OPTIONS

=over 8

=item B<-1, --fq1 STR>

FASTQ file for read1

=item B<-f, --fc1 STR>

Base statistics file for read1, could be fqcheck format or fqStat.txt format [auto detected]

=item B<-2, --fq2 STR>

FASTQ file for read1

=item B<-r, --fc2 STR>

Base statistics file for read2, could be fqcheck format or fqStat.txt format [auto detected]

=item B<-t, --seqType INT>

Sequencing platform, 0-HiSeq2000, 1-HiSeq4000, 2-BGISEQ-500

=back

=head1 DESCRIPTION

B<This script> is used to find out 'Tile Number' (Illumina) or 'FOV Number' (BGISEQ-500) from FASTQ file(s), which contains high 'N' proportion at one or more positions of reads. It first read bases statistic file (could be fqcheck or fqStat.txt format) to find out if there are sequencing cycle(s) with 'N' proportion greater than 0.5%, if Yes, go through the FASTQ file and check if there are any Tile/FOV with 'N' proportion greater than 90% at such cycle(s), then output '--tile/fov' + TileNumber/FOVNumber; if No, output nothing

Example: findNtile.pl [options] --fq1 CL200003395_L01_16_1.fq.gz --fq2 CL200003395_L01_16_2.fq.gz

=head1 AUTHOR

Don't know who write the original version. 

=head1 REPORTING BUGS

Report bugs to <linzh@genomics.cn>.

=head1 UPDATE

create: 2016.8.25 - Rewritten by Lin Zhe.
update: 2016.8.31 - fix: modifity auto_find_stat_file, if fqStat.txt is not detective for BGISEQ-500, try to search .fqcheck

=cut

use Getopt::Long;
use Pod::Usage;
use Cwd qw(abs_path);
use File::Basename;
use Time::HiRes;
use POSIX qw/strftime/;

my ($fq1,$fc1,$fq2,$fc2,$tile_cutoff,$seqType,$help);
GetOptions(
    "1|fq1:s"=>\$fq1,
    "f|fc1:s"=>\$fc1,
    "2|fq2:s"=>\$fq2,
    "r|fc2:s"=>\$fc2,
    "s|swath:i"=>\$tile_cutoff,
    "t|seqType:i"=>\$seqType,
    "h|help"=>\$help) or pod2usage(1);

pod2usage(
    -verbose=>2,
    -noperldoc=>1,) if defined $help;

pod2usage(1) if !defined $fq1 or !defined $seqType;

# tile_cutoff: if there are $tile_cutoff number of tile in a swath is unusal, 
# then filter all tiles of this swath

if($seqType == 0){
    $tile_cutoff||=13;
}elsif($seqType == 1){
    $tile_cutoff||=23;
}elsif($seqType == 2){
    #TODO: Dose BGISEQ-500 need to consider SWATH like Hiseq?
    $tile_cutoff||=0;
}

my $N_rate_cutoff=0.5;

# #####
# Main
# #####

$fc1 = auto_find_stat_file($fq1, 1, $seqType) if(defined $fq1 and !defined $fc1);
$fc2 = auto_find_stat_file($fq2, 2, $seqType) if(defined $fq2 and !defined $fc2);

my $tile_fov = find_N_tile_fov($fq1, $fc1, $N_rate_cutoff);
$tile_fov .= find_N_tile_fov($fq2, $fc2, $N_rate_cutoff) if defined $fq2;

if($tile_fov ne ""){
    if($seqType == 0 or $seqType == 1){
        print "--tile $tile_fov";
    }elsif($seqType == 2){
        print "--fov $tile_fov";
    }
}else{
    print "";
}

# #####
# SUB
# #####

sub auto_find_stat_file{
    #
    # Auto detect base stat file, if seqtype is 2 for BGISEQ-500, 
    # the base stat file should named by replaced .gz as .fqStat.txt.
    # otherwise, it would be 1.fqcheck for read 1 and 2.fqcheck for read 2
    #

    my ($fq, $pe_num, $seqType) = @_;
    my $fc = "";

    log_it("$fq dose not exists", "ERROR") if !-f $fq;

    my $fq_dir = dirname(abs_path($fq));
    my $fq_name = basename($fq);

    if($seqType == 0 or $seqType == 1){
        $fc = "$fq_dir/$pe_num.fqcheck";
    }else{
        $fc = "$fq_dir/$fq_name";
        $fc =~ s/\.gz$/\.fqStat\.txt/;

        #
        # if fqStat.txt is not exists for BGISEQ-500 (this could happend for
        # RNA-seq after remove rRNA), try to search .fqcheck
        #
        $fc = "$fq_dir/$pe_num.fqcheck" if !-f $fc;
    }

    log_it("$fc dose not exists (SeqType: $seqType)", "ERROR") if !-f $fc;

    return $fc;
}

sub find_N_tile_fov{
    #
    # find out which tile or fov contain(s) unusal N proportion
    #

    my ($fq, $fc, $N_cutoff) = @_;
    my (%Ncycle, %Ntile, $total_base);

    open FC,"< $fc" or log_it("Can not open $fc:$!", "ERROR");
    my $fc_first_line = <FC>;
    my $is_fqStat_format = 0;
    $is_fqStat_format = 1 if $fc_first_line =~ /^#Name/;

    #scan the stat file and find out which cycles contain unusual N rate
    while(<FC>){
        last if !$is_fqStat_format and /^$/; #there is an empty line which indicate the end of stat in fqcheck format
        next if /^#|^\s+|^Total|^Standard/;

        if($is_fqStat_format){ # is fqStat.txt format
            my ($pos, $a_cnt, $c_cnt, $g_cnt, $t_cnt, $n_cnt) = split /\s+/;
            my $n_pct = sprintf "%.2f", $n_cnt/($a_cnt + $c_cnt + $g_cnt + $t_cnt + $n_cnt)*100;
            $Ncycle{$pos} = $n_pct if $n_pct > $N_cutoff;
        }else{ # is fqcheck format
            my ($base, $pos, $a_pct, $c_pct, $g_pct, $t_pct, $n_pct) = split /\s+/;
            $Ncycle{$pos} = $n_pct if $n_pct > $N_cutoff;
        }
    }
    close FC;

    #If there are any unusual cycles with N, then scan the whole FASTQ and find out if 
    #there are any tile/fov contain more than 90% Ns of those unusual cycles.
    my $tile_fov_string = "";
    if(keys %Ncycle){
        open FQ,"gzip -dc $fq|" or log_it("Can not open $fq: $!", "ERROR");

        my $n=0;

        while(<FQ>){
            my $read_id=$_;chomp $read_id;
            my $seq=<FQ>;chomp $seq;
            <FQ>;
            <FQ>;

            $n++;
            #downsampling to improve speed, same approach was used by the preversion
            next if ($n-1) % 50 != 0;

            #Parse tile/fov number from read id 
            my $tile="";
            if($seqType == 0){
                $tile=(split /\:/,$read_id)[2]; 
            }elsif($seqType == 1){ #Hiseq 4000
                $tile=(split /\:/,$read_id)[4];
            }elsif($seqType == 2){ #BGISEQ-500
                if($read_id =~ /(C\d{3}R\d{3})/){
                    $tile=$1;
                }
            }

            log_it("Can not parse tile/fov number from read id: $read_id", "ERROR") if !defined $tile;

            #my @base=split //,$seq;
            #Count total number of each kinde of bases at those unusual cycle(s) tile(fov) by tile(fov)
            foreach my $cycle(keys %Ncycle){
                my $base = substr $seq, $cycle-1, 1;
                #$Ntile{$tile}{$cycle}{$base[$cycle-1]}++;
                $Ntile{$tile}{$cycle}{$base}++;
            }
        }
        close FQ;

        my %filter_tile;
        foreach my $tile(keys %Ntile) {
            foreach my $cycle (keys %{$Ntile{$tile}}) {
                $Ntile{$tile}{$cycle}{'A'}||=0;
                $Ntile{$tile}{$cycle}{'T'}||=0;
                $Ntile{$tile}{$cycle}{'C'}||=0;
                $Ntile{$tile}{$cycle}{'G'}||=0;
                $Ntile{$tile}{$cycle}{'N'}||=0;

                #total_base is different from previsou version of findNtile.pl which didn't include N
                my $total_base = $Ntile{$tile}{$cycle}{'A'}+$Ntile{$tile}{$cycle}{'T'}+
                $Ntile{$tile}{$cycle}{'C'}+$Ntile{$tile}{$cycle}{'G'}+$Ntile{$tile}{$cycle}{'N'};

                if($Ntile{$tile}{$cycle}{'N'} > $total_base*0.9){ 
                    if($seqType == 0){
                        if($tile<1200){
                            $filter_tile{'1'}{$tile}="";
                        }elsif($tile<1300){
                            $filter_tile{'2'}{$tile}="";
                        }elsif($tile<2100){
                            $filter_tile{'3'}{$tile}="";
                        }elsif($tile<2200){
                            $filter_tile{'4'}{$tile}="";
                        }elsif($tile<2300){
                            $filter_tile{'5'}{$tile}="";
                        }elsif($tile<2400){
                            $filter_tile{'6'}{$tile}="";
                        }
                    }elsif($seqType == 1){
                        if($tile<1200){
                            $filter_tile{'1'}{$tile}="";
                        }elsif($tile<2100){
                            $filter_tile{'2'}{$tile}="";
                        }elsif($tile<2200){
                            $filter_tile{'3'}{$tile}="";
                        }elsif($tile<2300){
                            $filter_tile{'4'}{$tile}="";
                        }
                    }elsif($seqType == 2){ 
                        #TODO: BGISEQ-500 FOV is as same as tile of Hiseq, what about swath
                        $filter_tile{'1'}{$tile} = "";
                    }
                }
            }
        }

        my %swath=();
        my $max;
        if($seqType == 0){
            $max=6;
            %swath=(1=>[1101..1116],2=>[1201..1216],3=>[1301..1316],4=>[2101..2116],5=>[2201..2216],6=>[2301..2316]);
        }elsif($seqType == 1){
            $max=4;
            %swath=(1=>[1101..1128],2=>[1201..1228],3=>[2101..2128],4=>[2201..2228]);
        }

        if($seqType == 2){
            $tile_fov_string.=join ",",keys %{$filter_tile{'1'}};
        }else{
            for(my $i=1;$i<=$max;$i++){
                if(keys %{$filter_tile{$i}}>=$tile_cutoff){ 
                    $tile_fov_string.=join ",",@{$swath{$i}};
                    $tile_fov_string.=",";
                }elsif(keys %{$filter_tile{$i}}>0){
                    $tile_fov_string.=join ",",keys %{$filter_tile{$i}};
                    $tile_fov_string.=",";
                }
            }
        }
        if (!defined $tile_fov_string) {
            $tile_fov_string = " ";
        }
        $tile_fov_string=~s/\,$//;
    }

    return $tile_fov_string;
}

sub log_it {
    my ($message, $level) = @_;
    $level ||= "INFO";
    my ( $time, $ms ) = Time::HiRes::gettimeofday();
    my $logtimestamp = strftime("%Y-%m-%d %H:%M:%S", localtime($time));

    $ms = sprintf("%03d", $ms / 1000);
    my $msg = sprintf("[findNtile %s.%03d %5s] %s\n", $logtimestamp, $ms, $level, $message);

    if($level eq "INFO"){
        print STDERR $msg;
    }elsif($level eq "ERROR"){
        print STDERR $msg;
        exit 1;
    }
}
