## readme

# 1. 在项目目录下创建report目录，进入report目录，创建如下目录
mkdir report && cd report/
mkdir 1.filter 2.mapping 3.GATK 4.CNV 5.SV 6.PCA 7.structure 8.phylogene

# 2. 将每个部分的output的项目报告中文件链接在项目目录下的report
# ln $outdir/filter/output/xx.xx 1.filter/


#3. 在report目录下运行
cp -r /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib/report/CSS .
cp -r /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib/report/HELP .
python /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Modules/lib/report/report.v1.py /its1/rongzhengqin/pipeline/Animal_And_Plant_Resequencing/Example/GATK/output/cohort.snp.filter.sample_list.xls
