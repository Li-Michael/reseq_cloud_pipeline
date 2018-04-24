import sys,os
import statplot
import numpy as np
typex = []
data = []
f = file(sys.argv[1],"r")
outdir = os.path.dirname(sys.argv[1])
for line in f:
	if line.startswith("##"):continue
	if line.startswith("#"):
		sns = line.rstrip("\n").split("\t")[1:]
		continue
	arr = line.rstrip("\n").split("\t")
	typex.append(arr[0])
	data.append(map(int,arr[1:]))

f.close()

"""
 98         plot_data = np.asmatrix(np.float64(np.asarray((C_A_arr,C_T_arr,C_G_arr,T_A_arr,T_C_arr,T_G_arr))))
  99         stackv_bar_plot(plot_data,sample_arr,"SNP_substitution_pattern","Groups","Percentage",width=0.5,legends=labels,scale=1)
"""
plot_data = np.asmatrix(np.float64(np.asarray(data)))
statplot.stackv_bar_plot(plot_data,sns, os.path.join(outdir,"Annotation_Type_stat"),"Samples","Percentage",width=0.4,legends=typex,scale=1,orientation = "horizontal",rotation=0)


