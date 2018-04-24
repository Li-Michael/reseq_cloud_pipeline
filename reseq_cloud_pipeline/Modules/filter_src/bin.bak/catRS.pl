my $list=shift;
my $out=shift;
my $sample=shift;
open OUT,">$out" or die $!;
open LIST,$list or die $!;

my (%nr,%ds,%n1,%n2,%l1,%l2,%gc1,%gc2,%q201,%q202,%q301,%q302,$dn,$dl,$da);

while(<LIST>)
{
	chomp;
	next if(/^#/);
	my $stat=$_;
	open IN,$stat or die $!;
	while(<IN>)
	{
		chomp;
		next if(($_ =~ /^Type/) || ($_ =~ /^\s*$/));
		my @arr=split /\t/,$_;
		if($arr[0] =~ /^Number/)
		{$nr{'r'}+=$arr[1];$nr{'n'}+=$arr[2];}
		elsif($arr[0] =~ /^Data/)
		{
			$ds{'r'}+=$arr[1];
			$ds{'n'}+=$1 if($arr[2] =~ /^(\d+)/);
		}
		elsif($arr[0] =~ /^N.+fq1/)
		{$n1{'r'}+=$arr[1];$n1{'n'}+=$arr[2];}
		elsif($arr[0] =~ /^N.+fq2/)
		{$n2{'r'}+=$arr[1];$n2{'n'}+=$arr[2];}
		elsif($arr[0] =~ /^GC.+fq1/)
		{push @{$gc1{'r'}},$arr[1];push @{$gc1{'n'}},$arr[2];}
		elsif($arr[0] =~ /^GC.+fq2/)
		{push @{$gc2{'r'}},$arr[1];push @{$gc2{'n'}},$arr[2];}
		elsif($arr[0] =~ /^Q20.+fq1/)
		{push @{$q201{'r'}},$arr[1];push @{$q201{'n'}},$arr[2];}
		elsif($arr[0] =~ /^Q20.+fq2/)
		{push @{$q202{'r'}},$arr[1];push @{$q202{'n'}},$arr[2];}
		elsif($arr[0] =~ /^Q30.+fq1/)
		{push @{$q301{'r'}},$arr[1];push @{$q301{'n'}},$arr[2];}
		elsif($arr[0] =~ /^Q30.+fq2/)
		{push @{$q302{'r'}},$arr[1];push @{$q302{'n'}},$arr[2];}
		elsif($arr[0] =~ /^Discard.+N/)
		{$dn+=$arr[1];}
		elsif($arr[0] =~ /^Discard.+qual/)
		{$dl+=$arr[1];}
		elsif($arr[0] =~ /^Discard.+Adapter/)
		{$da+=$arr[1];}
	}
	close IN;
}
close LIST;

my $per=100*$ds{'n'}/$ds{'r'};
my $gc=0.5*(&getr(@{$gc1{'n'}})+&getr(@{$gc2{'n'}}));
my $rb=$ds{'r'}/1000000;
my $cb=$ds{'n'}/1000000;
print OUT "Sample\t$sample\t\n";
print OUT "Raw reads\t$nr{'r'}\n";
printf OUT "Raw bases (Mb)\t%.2f\t\n",$rb;
print OUT "Clean reads\t$nr{'n'}\n";
printf OUT "Clean bases (Mb)\t%.2f\t\n",$cb;
printf OUT "Clean data rate (%)\t%.2f\t\n",$per;
print OUT "Clean read1 Q20 (%)\t".&getr(@{$q201{'n'}})."\n";
print OUT "Clean read2 Q20 (%)\t".&getr(@{$q202{'n'}})."\n";
print OUT "Clean read1 Q30 (%)\t".&getr(@{$q301{'n'}})."\n";
print OUT "Clean read2 Q30 (%)\t".&getr(@{$q302{'n'}})."\n";
printf OUT "GC content (%)\t%.2f\t\n",$gc;

close OUT;

sub getr
{
	my $aver=0;
	my @ttmp=@_;
	return $ttmp[0] if(@ttmp == 1);
	map{$aver += $_} @ttmp;
	
	if($aver !~ /\./)
	{
		 $aver = sprintf("%d", $aver/($#_ + 1) );
	}else{
		$aver = sprintf("%.2f", $aver / ($#_ + 1) );
	}
	return $aver;
}
