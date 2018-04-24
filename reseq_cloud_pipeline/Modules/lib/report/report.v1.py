#!/usr/bin/env python
# -*- coding: UTF=8 -*-
import sys
import mhtml
html_main = mhtml.simple_main(title="重测序项目基本分析结果")
sampleinfo = sys.argv[1]

#from GBCloud.processJson import *
#from GBCloud.autoRun import *

sns = []
"""
## decode json ##
#jsonConfigFile = sys.argv[1]
obj = getJson(jsonConfigFile)
inputObj = obj['input']
#configObj = obj['config']
outputObj = obj['output']
## get output ##
outdir, shdir, reportdir, jsondir = getOutput(outputObj)

for sample,value in inputObj["cleandata_multiple_lanes"].items():
	sns.append(sample)
"""
with open(sampleinfo, "r") as f:
	for line in f:
		if line.startswith("#"):continue
		arr = line.rstrip("\n").split("\t")
		sns.append(arr[0])

print("samples:",sns)

html_main.add_genebang_title("重测序项目基本分析结果")
statdir = './HELP/'
html_main.add_enter()
html_main.add_head_color("一、重测序项目生物信息分析基本流程", headlevel = 2)
html_main.add_line()
html_main.add_content(""">>> step 1. 下机数据质量控制，评估测序数据的可靠性""")
html_main.add_content(""">>> step 2. 将下机数据（reads）采用比对基因组，评估覆盖效率及测序深度""")
html_main.add_content(""">>> step 3. SNV(SNP/Short INDEL)检测和注释""")
html_main.add_content(""">>> step 4. 结构变异SV检测 """)
html_main.add_content(""">>> step 5. 拷贝数变异CNV检测""")
html_main.add_content(""">>> step 6. 群体主成分分析PCA""")
html_main.add_content(""">>> step 7. 群体结构structure分析""")
html_main.add_content(""">>> step 8. 群体系统进化树Phylogene分析""")
html_main.add_content_retract("""[1] 本项目结题报告中正文内容蓝色字体均为文件超级链接，点击可查看或者下载。""")
html_main.add_content_retract("""[2] 建议使用较新版本的火狐（Mozilla Firefox）浏览器、Google Chrome浏览器、Safari浏览器查看本项目结题报告，其他浏览器可能会由于页面代码不兼容而导致报告内容异常。""")


#html_main.add_head_line()
#html_main.add_enter()
#html_main.add_head_color("二、本项目实验设计",headlevel = 2)
#html_main.add_line()
#html_main.add_content(""">>> 本项目实验设计基本情况如下表所示：""")
#tmptable,tmpnote = mhtml.xls2table("%s"%sampleinfo)
#html_main.add_locate(str(tmptable))
#html_main.add_enter()
#html_main.add_head_line()

statdir="1.filter/"
html_main.add_head_color("三、结果展示及说明",headlevel = 2)
html_main.add_line()
html_main.add_head_color("1 测序数据进行数据过滤后质量评估", headlevel = 3)
html_main.add_content(""">>> 对下机的原始数据，进行数据质量评估,评测结果:(以其中一个样本为例，其他请见文件夹中filter下文件)""")

filter_stat = "filter_stat.xls"
filtertable, filternote = mhtml.xls2table("%s"%(statdir+filter_stat))
html_main.add_locate(str(filtertable))

html_main.add_content("*说明：*")
html_main.add_content_retract("""每个样本测序量均达到合同要求，且Q20，Q30指标也符合要求，测序原始数据的质量较好。""")
html_main.add_enter()
html_main.add_head_line()

statdir = "2.mapping/"
html_main.add_head_color("2 基因组比对情况统计", headlevel = 3)
html_main.add_content(">>> 序列比对背景及目的：")
html_main.add_content_retract("使用短序列比对软件bwa,将测序reads 比对到参考基因组上，bwa 具有快速、准确等特性，在重测序领域广泛使用。采用mem命令，其在比对大于70bp的数据时，具有较高的准确率。")
html_main.add_content(">>> 参考文献：")
html_main.add_content_retract("[1] Li, H. and Durbin, R. (2009) Fast and accurate short read alignment with Burrows-Wheeler transform, Bioinformatics, 25, 1754-1760.")
html_main.add_content(">>> 所使用软件参数:")
html_main.add_content_retract("[1] bwa, v.0.7.9, 参数：mem  -T 30 -h 5  -M ")
html_main.add_content(">>> 序列比对结果统计：比对结果以bam格式保存，项目交付后可申请下载（数据庞大）")
html_main.add_content_retract("""[1] 样本比对基因组统计结果如下表所示: """)
tmptable,tmpnote = mhtml.xls2table("2.mapping/MappingQC_stat.xls")
html_main.add_locate(str(tmptable))

html_main.add_enter()
html_main.add_head_line()

statdir = "3.GATK"
html_main.add_head_color("3 单核苷酸碱基多态性（SNP）及短片段插入缺失多态性（InDel）检测", headlevel = 3)
html_main.add_content(">>> 3.1 变异检测背景及目的：")
html_main.add_content_retract("一个物种内，不同个体间存在着大量的可遗传的多态性标记，通过观察及分析群体内的多态性遗传标记，有如下几个较重要的应用：如遗传图谱构建、种群结构与环境适应性分析、全基因组关联分析、数量或质量性状定位、分子辅助育种等等。可直接或间接的找到控制目标性状的基因或功能区域。")
html_main.add_content_retract("""此处，主要进行单核苷酸碱基多态性（<a href="https://en.wikipedia.org/wiki/Single-nucleotide_polymorphism">SNP</a>）位点和短片段插入缺失多态性（<a href="https://en.wikipedia.org/wiki/Indel">InDel</a>）检测。""")
html_main.add_content(">>> 多态性位点的鉴定:")
html_main.add_content_retract("""[1] 多态性位点鉴定：采用GATK检测单核苷酸碱基突变SNPs (Single-nucleotide polymorphism)及短序列插入缺失突变(Insertions and Deletions)""")
html_main.add_content_retract("""为了降低检测到的变异的假阳性, 对碱基质量>13 (base quality >13)及比对分值大于20的序列(Mapping Quality > 20)的测序数据。""")
html_main.add_content_retract("""[2] SNP InDel 鉴定采用软件：GATK的HaplotypeCaller/GenotypeGVCFs/SelectVariants工具进行SNP/INDEL的cohort calling，VariantFiltration工具对vcf进行过滤。参数:calling过程采用默认参数，可以根据项目情况进行调整; 
SNP过滤参数为：--clusterSize 3 --clusterWindowSize 10 -maskExtend 3 --filterName "highMQRankSum" --filterExpression "MQRankSum > -12.5" --filterName "lowFS" --filterExpression "FS < 20.0"  --filterName "highReadPosRankSum" --filterExpression "ReadPosRankSum > -8.0" --filterName "highMQ"  --filterExpression "MQ > 40.0" --filterName "highQD"  "--filterExpression "QD > 2.0"  --genotypeFilterName "highDP" --genotypeFilterExpression "DP > 8.0"；INDEL的过滤参数为：--filterExpression "MQ > 40.0" --filterName "highMQRankSum" --filterExpression "MQRankSum > -12.5"  --genotypeFilterExpression "DP > 8.0"。""")

html_main.add_content(""">>> SNP分析结果及说明：""")
html_main.add_content_retract("采用上述方法鉴定SNP及INDEL,鉴定到SNP及INDEL多态性位点及各样本基因型结果:""")
html_main.add_content_retract("""[1] 鉴定到的所有的SNP位点: <a href="%s/cohort.snp.filter.vcf">请点击查看</a>"""%(statdir))
html_main.add_content_retract("""[2] 鉴定到的所有的INDEL位点: <a href="%s/total.indel.fmt.xls">请点击查看</a>"""%(statdir))
html_main.add_content_retract("""* 文件结果说明: <a href="HELP/variant/var_mat.html">请点击查看</a>""",2)
html_main.add_enter()
html_main.add_content(">>> 3.2 SNP突变频谱分析：")
html_main.add_content_retract("""单核苷酸碱基突变包含如下6种基本类型： C>A/G>T（互补原则）, C>G/G>C, C>T/G>A, T>A/A>T,T>C/A>G, T>G/A>C，又可以根据发生替换的碱基类型分成2大类，嘌呤和嘧啶间的替换称为颠换（transversion），嘌呤与嘌呤之间或嘧啶与嘧啶之间的替换称为转换（transition）。根据各类型的点突变的数量，对样本进行聚类分析，可以观察样本在点突变水平上的相似程度，不同遗传背景或不同性状样本（如癌症的体细胞突变）一般会呈现聚类现象""")
html_main.add_content("分析结果如下：")
html_main.add_content_retract("[1] SNP突变类型数目汇总统计:")
html_main.add_locate("""<img src="%s/total_snp_substitution.png" width="65%%" /><a href="%s/total_snp_substitution.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_content_retract("[2] SNP突变频谱，堆积图")
html_main.add_locate("""<img src="%s/SNP_substitution_pattern.png" width="65%%" /><a href="%s/SNP_substitution_pattern.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_content_retract("""[3] 对应的表格: """)
tmptable,tmpnote = mhtml.xls2table("%s/Mutation_pattern.xls"%statdir)
html_main.add_locate(str(tmptable))
html_main.add_content(tmpnote)
html_main.add_content_retract("[4] SNP突变频谱及样本聚类结果")
html_main.add_locate("""<img src="%s/SNP_substitution_Mutation_Spectrum.png" width="65%%" /><a href="%s/SNP_substitution_Mutation_Spectrum.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_enter()

#statdir = "4.SNVanno"
#html_main.add_head_color("4 功能注释", headlevel = 3)
html_main.add_content(""">>> 3.3 SNV注释分析：""")
#html_main.add_content_retract("""(1) 对于人类：注释包括如下数据库:基于refGene对变异位点所在的区域进行注释；该变异位点相关的转录本；描述 UTR、splicing、ncRNA_splicing 或 intergenic 区域的变异情况；外显子区的 SNV or InDel 变异类型；氨基酸改变情况；dbSNP144数据库等。""")
html_main.add_content_retract("""(1) 非人类样本：仅注释embl 基因结构（即ensGene）""")
html_main.add_content(""">>> 注释结果：详细说明请点击<a href="./HELP/variant/human_var_anno.readme.rtf">查看</a>""")
html_main.add_content_retract("""[1] 对SNP进行功能注释，所有位点的注释结果见：<a href="%s/cohort.snp.filter.vcf.fmt.ensGene.variant_function">点击查看</a>"""%statdir)
html_main.add_content_retract("""[2] 分样本注释结果路径：<a href="%s/">点击查看</a>"""%statdir)
html_main.add_content_retract("""[3] 各样本Gene区域注释情况汇总,类型说明:<a href="./HELP/variant/refgene_annotation.readme.html">查看</a>""")
html_main.add_locate("""<img src="%s/SNP_Annotation_Type_stat.png" width="65%%" /><a href="%s/SNP_Annotation_Type_stat.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_content_retract("""上图对应的表格：<a href="%s/SNP.anno.stat.xls">点击查看</a>"""%statdir)
html_main.add_enter()

#statdir = "5.INDELanno"
#html_main.add_head_color("5 InDel突变位点功能注释", headlevel = 3)
html_main.add_content(""">>> 3.4 InDel注释分析：""")
html_main.add_content_retract("""[1]  对InDel进行功能注释，所有位点的注释结果见：<a href="%s/cohort.indel.filter.vcf.fmt.ensGene.variant_function">点击查看</a>"""%statdir)
html_main.add_content_retract("""[2] 分样本注释结果路径：<a href="%s/">点击查看</a>"""%statdir)
html_main.add_content_retract("""[3] 各样本Gene区域注释情况汇总,类型说明:<a href="./HELP/variant/refgene_annotation.readme.html">查看</a>""")
html_main.add_locate("""<img src="%s/INDEL_Annotation_Type_stat.png" width="65%%" /><a href="%s/INDEL_Annotation_Type_stat.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_content_retract("""上图对应的表格：<a href="%s/INDEL.anno.stat.xls">点击查看</a>"""%statdir)
html_main.add_enter()
html_main.add_head_line()

statdir = "4.CNV"
html_main.add_head_color("4 基因组范围内拷贝数变异CNV检测", headlevel = 3)
html_main.add_content(""">>> CNV（copy number variations）指基因组上1kb-5Mb级别之间的DNA片段拷贝数变异；已知一半的CNV与coding区域有重叠，这些变异直接影响CNV区域的基因剂量补偿，影响基因表达水平、很多CNV与许多性状有关，如水稻粒长、品质。人类疾病，如癌症、自闭症等复杂疾病有关。可通过CNVnator进行检测，即通过基因组上不同的reads 覆盖深度，判断潜在的拷贝数增加和拷贝数减少。""")
html_main.add_content_retract("""采用RD(read depth)-based 方法检测拷贝数变异。大致过程如下：a) 计算基因组上每个窗口范围内的RD水平 b)校正，考虑GC含量引入的偏差 c)拷贝数估计，并计算gain和loss区域 d) 将拷贝数相同的区域合并到一起。一般对 单样本 或 成对样本（case/control）检测CNV，后者的假阳性率远低于前者。""")
html_main.add_content(">>> CNV区域鉴定：")
html_main.add_content_retract("""采用CNVnator v0.3.3, 参数：-unique; -his:100; -stat:100; -partition:100; -call:100。""")

html_main.add_content(">>> 参考文献：")
html_main.add_reference("""[1] Abyzov A, Urban AE, Snyder M, Gerstein M. CNVnator: An approach to discover, genotype, and characterize typical and atypical CNVs from family and population genome sequencing. Genome Res. 2011 Jun;21(6):974-84. """)

html_main.add_content(">>> 结果及说明：")
html_main.add_content_retract("""[1] CNV区域检测结果:""")
for sn in sns:
	html_main.add_content_retract("""样本%s, 其检测到的CNV区域结果：<a href="%s/%s.cnv.txt">点击查看</a>"""%(sn,statdir,sn),2)
	html_main.add_enter()	
html_main.add_content_retract("""[2] CNV统计结果: <a href="%s/cnv.stat.xls">点击查看</a>"""%statdir)

html_main.add_enter()
html_main.add_head_line()

statdir = "5.SV"
html_main.add_head_color("5 基因组范围内结构变异SV检测", headlevel = 3)
html_main.add_content(""">>> SV（结构变异）指基因组水平上大片段的插入、缺失、倒置、易位等序列。可利用BreakDancer软件，进行插入（INS）、缺失（DEL）、倒置(INV)、染色体内部迁移(ITX)、染色体间的迁移的检测(CTX)。为保证结果的可靠性过滤去掉PE reads支持数小于2的SV结果。""")
html_main.add_content(">>> 方法说明：使用breakdancer 来查找整合的片段大概的位置，使用默认参数。通过自主开发的程序找到精确的插入位点。")
#html_main.add_content_retract("""分析基本流程，见下图：""")
#html_main.add_locate("""<img src="./HELP/variant/virus_genome_scan.png" width="65%" />""")
#html_main.add_content(""">>> 插入片段检测结果：""")
#html_main.add_content_retract("""[1] 插入位点识别结果：<a href="%s/rice_plasmid_SV.xlsx">点击查看</a>"""%statdir)
for sn in sns:
	html_main.add_content_retract("""样本%s, 其检测到的基因组整合位点关系图: <a href="%s/%s.sv.txt">点击查看</a>"""%(sn,statdir,sn))
	#html_main.add_content_retract("""样本%s, plasmid 转基因片段测序reads（即整合到基因组上的片段）覆盖图: <a href="%s/%s.insert.svg">点击查看</a>"""%(sn,statdir,sn))
html_main.add_content_retract("""[2] CNV统计结果: <a href="%s/sv.stat.xls">点击查看</a>"""%statdir)
html_main.add_enter()
html_main.add_head_line()

statdir = "6.PCA"
html_main.add_head_color("6 群体主成分分析PCA", headlevel = 3)
html_main.add_content(""">>> 主成分分析（PCA）是一种纯数学的运算方法，可以将多个相关变量经过线形转换选出较少个数的重要变量。PCA应用到很多学科，在遗传学当中，主要用于聚类分析，它是基于个体基因组SNP差异程度，按照不同性状特征将个体按主成分进行聚类成不同的亚群，同时用于和其它方法做相互验证。研究种群的PCA图如图7。仅针对个体数n=xx的常染色体数据，忽略高于2个等位基因位点以及错配数据。""")
html_main.add_content(">>> 方法说明：使用CGTA 来计算，保留前三个维度，取前两个维度多图。")
html_main.add_content(""">>> PCA分析结果：""")
html_main.add_content_retract("""[1] PCA聚类结果：<a href="%s/pca.group1.eigenvec">点击查看</a>"""%statdir)
html_main.add_content_retract("""[2] PCA结果见下图: """)
html_main.add_locate("""<img src="%s/pca.group1.png" width="65%%" /><a href="%s/pca.group1.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_enter()
html_main.add_head_line()


statdir = "7.structrue"
html_main.add_head_color("7 群体结构structure分析", headlevel = 3)
html_main.add_content(""">>> 群体遗传结构指遗传变异在物种或群体中的一种非随机分布。按照地理分布或其他标准可将一个群体分为若干亚群，处于同一亚群内的不同个体亲缘关系较高，而亚群与亚群之间则亲缘关系稍远。群体结构分析有助于理解进化过程，并且可以通过基因型和表型的关联研究确定个体所属的亚群。在群体世系推断分析之后，可以将样本按区域或种群进行划分。""")
html_main.add_content(""">>> 方法说明：使用plink对vcf进行格式转化，利用Admixture来进行群体结构分析,其中K取值范围维1～8。""")
html_main.add_content(""">>> structure分析结果：""")
html_main.add_content_retract("""[1] structure结果见下图：""")
html_main.add_locate("""<img src="%s/structure.png" width="65%%" /><a href="%s/structure.svg">SVG矢量图</a>"""%(statdir,statdir))
html_main.add_content_retract("""[2] structure详细结果：<a href="%s/">点击查看</a>"""%statdir)
html_main.add_enter()
html_main.add_head_line()


statdir = "8.phylogene"
html_main.add_head_color("8 群体系统进化树Phylogene分析", headlevel = 3)
html_main.add_content(""">>> 系统进化树(phylogenetic tree，又称evolutionary tree进化树)就是描述群体间进化顺序的分支图或树，表示群体间的进化关系。根据群体的物理或遗传学特征等方面的共同点或差异可以推断出它们的亲缘关系远近。""")
html_main.add_content(""">>> 方法说明：使用plink对vcf进行格式转化，利用Admixture来进行群体结构分析,其中K取值范围维1～8。""")
html_main.add_content(""">>> Phylogene分析结果：""")
html_main.add_content_retract("""[1] phylogene结果见：""")
html_main.add_locate("""<a href="%s/snphylo.output.ml.tree">phylogenetic tree结果文件</a>"""%statdir)
html_main.add_locate("""<a href="%s/snphylo.output.bs.tree">bootstrap analysis结果文件</a>"""%(statdir))
html_main.add_content_retract("""[2] phylogene详细结果：<a href="%s/">点击查看</a>"""%statdir)
html_main.add_enter()
html_main.add_head_line()

html_main.add_enter()


#html_main.add_head_color("四、附录", headlevel = 2)
#html_main.add_line()
#html_main.add_head_color("1 基因组文件来源说明", headlevel = 3)
#html_main.add_content(""">>> 基因组文件：Oryza_sativa.IRGSP-1.0.27.dna_sm.toplevel.fa；下载网站: EMBL, ftp.ensemblgenomes.org""")


with open('reseq_basic_analysis.html', 'w') as fp:
	fp.write(html_main.str_top(height = 400,width=600))
