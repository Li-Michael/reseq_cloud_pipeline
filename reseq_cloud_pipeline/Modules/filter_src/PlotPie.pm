package PlotPie;

use strict;
use warnings;
use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(plotPie);

sub plotPie{
	my ($infile, $outfile, $radius) = @_;
###############################
# QC of raw reads(Zm_6h_C1)   #
# N       0.1                 #
# Adapter 0.1                 #
# Low Quality     0.1         #
# Clean Reads     11719140    #
###############################
	my $px = 10;
	my $total;
	my $width = $radius * 5;
	my $height = $radius * 3.6;
	my $xc = $radius * 2.5;
	my $yc = $radius * 2.1;
	open IN,"$infile";
	<IN>;
	while(<IN>){
		chomp;
		my @tmp = split(/\t/, $_);
		$total += $tmp[1];
	}
	close IN;
	
	my $count = 0;
	my ($angle, $text_anchor, $sx, $sy, @sectorX, @sectorY, $lx, $ly, @lineX, @lineY, @names, @flag, @text, @trim);
	open IN2,"$infile";
	my $title = <IN2>;
	chomp $title;
	my $no = 0;
	while(<IN2>){
		chomp;
		my @tmp = split(/\t/, $_);
		$count += $tmp[1] / 2;
		$angle = 360 * $count / $total;
		$lineX[$no][0] = $xc + $radius * sin(3.1415926535897932384626433832795*$angle/180);
		$lineY[$no][0] = $yc - $radius * cos(3.1415926535897932384626433832795*$angle/180);
		my $angle1 = 45 + int($angle / 90) * 90;
		$lineX[$no][1] = $lineX[$no][0] + $radius * 0.15 * sin(3.1415926535897932384626433832795*$angle1/180);
		$lineY[$no][1] = $lineY[$no][0] - $radius * 0.15 * cos(3.1415926535897932384626433832795*$angle1/180);
		if($no > 0 && $lineY[$no][1] - $lineY[$no-1][1] <= 1.5 * $px && $lineY[$no][1] - $lineY[$no-1][1] >= -1.5 * $px){
			push @trim, ($no - 1);
			for my $t(@trim){
				$lineY[$t][1] -= 1.2*$px;
				$lineY[$t][2] -= 1.2*$px;
				$lineY[$t][3] = $lineY[$t][2] + 0.3 * $px;
			}
		}
		my $angle2 = 90 + int($angle / 180) * 180;
		$lineX[$no][2] = $lineX[$no][1] + $radius * 0.75 * sin(3.1415926535897932384626433832795*$angle2/180);
		$lineY[$no][2] = $lineY[$no][1];
		$lineX[$no][3] = ($angle > 180) ? ($lineX[$no][2] - 0.3 * $px) : ($lineX[$no][2] + 0.3 * $px);
		$lineY[$no][3] = $lineY[$no][2] + 0.3 * $px;
#		push @lineX, $lx;
#		push @lineY, $ly;
		$text_anchor = ($angle >= 180) ? "end" : "start";
		push @text, $text_anchor;
		$count += $tmp[1] / 2;
		$angle = 360 * $count / $total;
		$sx = $xc + $radius * sin(3.1415926535897932384626433832795*$angle/180);
		$sy = $yc - $radius * cos(3.1415926535897932384626433832795*$angle/180);
		push @sectorX, $sx;
		push @sectorY, $sy;
		push @names, $tmp[0]."(".sprintf("%.2f", 100 * $tmp[1] / $total)."%)";
		$flag[$no] = ($tmp[1] / $total >= 0.5) ? "1,1" : "0,1";
		$no += 1;
	}
	close IN2;

#my @a = qw/200 377 138 20 75/;
#my @b = qw/20 231 369 194 71/;

	
	my @colors = ("#f6aea0", "#f5b68b", "#979797", "#5ca7ba", "#ffff00");
#	my @colors = ("red","orange","yellow","green","#00ced1","blue","purple");
#print STDERR "$sectorX[0]\n";
	open SVG,">$outfile";
print SVG<<END;
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg width="$width" height="$height" version="1.1" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="$width" height="$height" style="fill:#FFFFFF;fill-opacity:1;stroke:none;"/>
END

	my $col = 0;
	my $l = scalar @sectorX - 1;
#print STDERR "$l\n";
	for my $x2(0..$l){
		my $x1 = $x2 - 1;
		print SVG<<END;
<path d="M$xc,$yc L$sectorX[$x1],$sectorY[$x1] A$radius,$radius 0 $flag[$x2] $sectorX[$x2],$sectorY[$x2] z" style="fill:$colors[$col]; fill-opacity:1; stroke:NA; stroke-width:1"/>
END
		print SVG<<END;
<path d="M$lineX[$x2][0],$lineY[$x2][0] C$lineX[$x2][1],$lineY[$x2][1] $lineX[$x2][1],$lineY[$x2][1] $lineX[$x2][2],$lineY[$x2][2] M$lineX[$x2][2],$lineY[$x2][2] C$lineX[$x2][1],$lineY[$x2][1] $lineX[$x2][1],$lineY[$x2][1] $lineX[$x2][0],$lineY[$x2][0]" style="fill:#ffffff;stroke:$colors[$col];stroke-width:1"/>
END
		print SVG<<END;
<text x="$lineX[$x2][3]" y="$lineY[$x2][3]" fill="$colors[$col]" text-anchor="$text[$x2]" font-size="10px" font-weight="bold" font-family="Arial">$names[$x2]</text>
END
		$col += 1;
	}
my $xt = $xc;
my $yt = $yc - $radius * 1.8;
print SVG<<END;
<text x="$xt" y="$yt" fill="#000000" text-anchor="middle" font-size="15px" font-weight="bold" font-family="Arial">$title</text>
</svg>
END
	close SVG;
}
