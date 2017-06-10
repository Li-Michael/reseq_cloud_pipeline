# -*- coding: UTF-8 -*-
import mhtml
import sys

cm_content = """####1. PIPELINE OF EXPERIMENT
###1.1 stardard pipeline
The pipeline of the experiment is illustrated in the figure bellow.<br />
<img src="RNAdenove_help/rna_denove_experiment_pipe.png"/>
Figure above shows the steps for the experiment pipeline. After extracting the total RNA from the samples, mRNA of eukaryotes is enriched by using the oligo (dT) magnetic beads and mRNA of prokaryotes is enriched just by removing rRNA from the total RNA. By using the fragmentation buffer, the mRNA is fragmented into short fragments (about 200 bp), then the first strand cDNA is synthesized by random hexamer-primer using the mRNA fragments as templates. Buffer, dNTPs, RNase H and DNA polymerase I are added to synthesize the second strand. The double strand cDNA is purified with QiaQuick PCR extraction kit and washed with EB buffer for end repair and poly (A) addition. Finally, sequencing adaptors are ligated to the fragments. The fragments are purified by Agarose gel electrophoresis and enriched by PCR amplification. The library products are ready for sequencing analysis via Illumina HiSeq<sup>TM</sup> 2000.
<br />图中描述的转录组测序的实验步骤:提取样品总RNA并使用DNase I消化DNA后，用带有Oligo（dT）的磁珠富集真核生物mRNA（若为原核生物，则用试剂盒去除rRNA后进入下一步）；加入打断试剂在Thermomixer中适温将mRNA打断成短片段，以打断后的mRNA为模板合成一链cDNA，然后配制二链合成反应体系合成二链cDNA，并使用试剂盒纯化回收、粘性末端修复、cDNA的3'末端加上碱基"A"并连接接头，然后进行片段大小选择，最后进行PCR扩增；构建好的文库用Agilent 2100 Bioanalyzer和ABI StepOnePlus Real-Time PCR System质检合格后，使用Illumina HiSeq<sup>TM</sup> 2000或其他测序仪（如有必要）进行测序
Ref: <br />
Vera, J.C., et al. , Rapid transcriptome characterization for a nonmodel organism using 454 pyrosequencing. Molecular Ecology.<br />
Ozsolak, F. and Milos, P.M. (2010) RNA sequencing: advances, challenges and opportunities, Nature Reviews Genetics, 12, 87-98.<br />
<br />
###1.2 strand-specific pipeline
Sometimes, we use the dUTP method to build the library, which can determine the orientation of transcripts.<br />
Different strand-specific RNA sequencing methods:<br />
<img src="RNAdenove_help/different_strands_methods.jpg"/>
Ref: Levin, J.Z., et al. (2010) Comprehensive comparative analysis of strand-specific RNA sequencing methods, Nat Methods, 7, 709-715. <br /><br />
####2. 转录本组装的主要信息分析流程
<ul><li>a. 数据质量控制与低质量数据过滤</li><li>b. 转录组组装拼接及组装指标统计</li><li>c. 转录本潜在的编码与非编码基因预测</li><li>d. 编码序列注释，NR、swissprot、trembl注释</li><li>e. 编码基因的功能注释，GO、eggNOG、KEGG注释</li><li>f. 非编码RNA序列注释，小RNA前体、已知的noncoding、其他RNA等</li></ul><br/>
####3. 数据质量控制
<pre>The clean reads should satisfy the following criteria:</pre>
<pre>	1) Remove reads with adaptors;</pre>
<pre>	2) Remove reads with unknown bases more than 10%;</pre>
<pre>	3) Remove low quality reads (which are defined as reads having more than 50% bases with quality value <= 5).</pre>
<pre>	4)	The Q20 of the clean reads should more than 85%;</pre>
<pre>	5)	The sequencing output size should meet the requirement of contract;</pre>
<pre>	6)	The GC content of clean reads should in a normal range(35%~65%).</pre>
If the clean reads following the QC criteria, we go through the further analysis, otherwise it should be resequencing or trimmed to meet the criteria.<br /><br />
####4. 转录组组装简介
Firgure beblow is the pipeline of de novo assembly. Transcriptome de novo assembly is carried out with short reads assembling program – Trinity.<br/>
Overview of Trinity<br/>
(a) Inchworm assembles the read data set (short black line, top) by greedily searching for paths in a k-mer graph (middle), resulting in a collection of linear contigs (color lines, bottom), with each k-mer present only once in the contigs.<br /> (b) Chrysalis pools contigs if they share at least one k-1-mer and reads span the join, and builds individual de Bruijn graphs from each pool (colored lines).<br /> (c) Butterfly takes each de Bruijn graph from Chrysalis (top), and trims spurious edges and compacts linear paths (middle). It then reconciles the graph with reads (dashed colored arrows, bottom) and pairs (not shown), and outputs one linear sequence for each splice form and/or paralogous transcript reflected in the graph (bottom, colored sequences).
Trinty组装步骤如下：<br/>
<img src="RNAdenove_help/trinity_pipeline.jpg" />
<br />
Inchworm 构建k-mer库，K=25。过滤低频k-mer选择最高频度的k-mer作为种子（不包括复杂度和单一的k-mers,一次用完即从k-mer库中剔除），用来Contig组装。以k-mer间overlap长度等于k-1对种子进行延伸，直到不能再延伸，形成线性Contig。
<br />
Chrysalis 把可能存在可变剪切及其他平行基因的Contigs聚类。每个Contig集定义成一个Component，对每个Component构建de Bruijn graphs。拿reads验证，看每个Component的reads支持情况。
<br />
Butterfly 合并在de Bruijn 图中有连续节点的线性路径，以形成更长的序列。剔除可能由于测序错误（只有极少reads支持）的分叉，使边均匀。用动态规划算法打分，鉴定被reads和read pairs支持的路径，剔除reads支持少的路径。
<br />
Trinty组装后得到各transcripts，首先使用Tgicl将其去冗余和进一步拼接，然后再对这些序列进行同源转录本聚类，得到最终的Unigene。如果同一物种做了多个样品测序，不同样品组装得到的Unigene也需要通过序列聚类软件做进一步序列拼接，去冗余处理，以及同源转录本聚类，得到尽可能长的非冗余Unigene。进行同源转录本聚类以后，Unigene分为两部分。一部分是clusters，同一个cluster里面有若干条相似度高（大于93%）的Unigene（以CL开头，CL后面接基因家族的编号）。其余的是singletons（以Unigene开头），代表单独的Unigene。
<br />组装及聚类拼接简单流程图<br />
<img src="RNAdenove_help/cluster_assembly.jpg" />
Ref:Haas, B.J., et al. (2013) De novo transcript sequence reconstruction from RNA-seq using the Trinity platform for reference generation and analysis, Nat Protoc, 8, 1494-1512.<br /><br />
####5. 转录本潜在的编码与非编码基因预测
To assess a transcript’s coding potential, in the CPC software, six features are extracted from the transcript’s nucleotide sequence.
<ul><li>a. LOG-ODDS SCORE</li><li>b. COVERAGE OF THE PREDICTED ORF</li><li>c. INTEGRITY OF THE PREDICTED ORF</li><li>d. NUMBER OF HITS</li><li>e. HIT SCORE</li><li>f. FRAME SCORE</li></ul>
Then, incorporate these six features into a support vector machine (SVM) machine learning classifier.
Ref: Kong, L., et al. (2007) CPC: assess the protein-coding potential of transcripts using sequence features and support vector machine, Nucleic Acids Research, 35, W345-W349.<br /><br />
"""

if __name__ == "__main__":
	c = cm_content.split("\n")	
	html_main = mhtml.simple_main(title="RNA denovo 帮助文档",css="../CSS")
	html_main.add_head("RNA denovo 帮助文档")
	html_main.add_enter()
	html_main.add_back1()
	html_main.add_enter()
	for line in c:
		if line.startswith("####"):
			html_main.add_head(line[4:],2)
			html_main.add_line()
			html_main.add_enter()
		elif line.startswith("###"):
			html_main.add_head(line[3:],3)
			html_main.add_enter()
		elif line.startswith("##"):
			html_main.add_head(line[2:],4)
			html_main.add_enter()
		else:
			html_main.add_content(line)
	f = file("RNAdenove_help.html","w")
	f.write(str(html_main))
	f.close()
	exit(0)
