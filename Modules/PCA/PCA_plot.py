#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import mplconfig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pca_eig = sys.argv[1]
df = pd.read_csv(pca_eig, sep=" ")

df1 = df.set_index(['2'])
fig, ax = plt.subplots(figsize=(10,8))
group = list(set(df1.index))
colors, linestyles, markers = mplconfig.styles(len(group))

for i in range(len(group)):
    ax.scatter(x=df1.loc[group[i],'eigenvector1'], y=df1.loc[group[i], 'eigenvector2'], s=plt.rcParams['lines.markersize']**2.5, c=colors[i], marker=markers[i], label=group[i])

# tidy up the figure
ax.grid(True)
ax.legend(loc='best')
ax.set_title('PCA Analysis')
ax.set_xlabel('eigenvector1')
ax.set_ylabel('eigenvector2')

plt.savefig( os.path.join(os.path.dirname(pca_eig), os.path.splitext(os.path.basename(pca_eig))[0]+".svg"), format="svg")
plt.savefig( os.path.join(os.path.dirname(pca_eig), os.path.splitext(os.path.basename(pca_eig))[0]+".png"), format="png")

