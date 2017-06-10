#!/usr/bin/env python
#coding:utf-8

import sys,os
import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator,FormatStrFormatter
import numpy as np

def baseValue(df,name, space=150, x=None, y=None, ax=None, subplots=False, figsize=None, use_index=True, title=None, grid=True, legend=True, style=None, xticks=None, yticks=None, xlim=None, ylim=None, rot=None, fontsize=None, colormap=None):
    fig = df.plot.box(use_index=False,xticks=np.linspace(0,space, int(space/10)+1), title=r"Quality scores across all bases(Sanger / Illumina )", fontsize=fontsize, x=x, y=y, ax=ax, subplots=subplots, figsize=figsize, legend=legend, style=style, yticks=yticks, xlim=xlim, ylim=ylim, rot=rot, colormap=colormap, patch_artist=True)
    # set the xlim,ylim设置坐标轴范围
    #fig.xlim(0, space)
    fig.set_xticklabels(tuple([ str(int(i)) for i in np.linspace(0,150,16)]))
    """
    # 分别设置 x轴主刻度、主刻度文本格式和次刻度 
    xmajorLocator = MultipleLocator(10)
    xmajorFormatter = FormatStrFormatter('%3d')
    xminorLocator = MultipleLocator(5)

    # 同上 x轴设置y轴
    ymajorLocator = MultipleLocator(5)
    ymajorFormatter = FormatStrFormatter('%2d')
    #yminorLocator = MultipleLocator(5)

    # 设置x轴刻度文本
    fig.xaxis.set_major_locator(MultipleLocator(20))
    fig.xaxis.set_major_locator(xmajorFormatter)
    fig.xaxis.set_minor_locator(xminorLocator)
    
    # 设置y轴刻度文本
    fig.yaxis.set_major_formatter(ymajorLocator)
    fig.yaxis.set_major_formatter(ymajorFormatter)
    """
    fig.set_xlabel(r'Position in read(bp)')
    fig.set_ylabel(r'Base Values')

    
    # 开启网格
    fig.grid()
    #fig.xaxis.grid(True, which='major')
    #fig.yaxis.grid(True, which='major')
    
    #plt.show()
    plt.savefig(name+'.png')


df = pd.read_csv('Base_quality_value_distribution_by_read_position_1.txt', sep='\t')


df1 = df.iloc[:150, :]
df1 = df1.set_index(df1.iloc[:,0]).T.iloc[1:,:]
"""
for i in range(len(df1.iloc[0,:])):
    df1.iloc[:,i] = pd.to_numeric(df1.iloc[:,i], errors='coerce')
#df3 = df1.iloc[1:43, :]
"""
z = [{m:n  for (m,n) in zip( ['mean', 'med','q1','q3','whislo','whishi'], list(map(float,df1.iloc[42:,i])) )} for i in range(0,150) ]

ax = plt.subplot(111)
fig = ax.bxp(z,showfliers=False, positions=None, widths=None, vert=True, showmeans=True,meanline=True, manage_xticks=False)
ax.set_xlim((0,150))
ax.set_xticks(np.linspace(0,150,16))
ax.set_xticklabels(tuple([ str(int(i)) for i in np.linspace(0,150,16)]))
ax.set_yticks(np.linspace(0,40,9))
ax.set_yticklabels(tuple([ str(int(i)) for i in np.linspace(0,40,9)]))

for box in fig['boxes']:
    # change outline color
    box.set( color='DarkGreen', linewidth=2)
    # change fill corlor
    box.set( facecolor = 'Yellow' )

## change color and linewidth of the whiskers
for whisker in fig['whiskers']:
    whisker.set(color='DarkOrange', linewidth=2)

## change color and linewidth of the caps
for cap in fig['caps']:
    cap.set(color='Gray', linewidth=2)

## change color and linewidth of the medians
for median in fig['medians']:
    median.set(color='DarkBlue', linewidth=2)

## change the style of fliers and their fill
#for flier in bp['fliers']:
#    flier.set(marker='o', color='#e7298a', alpha=0.5)

plt.savefig("aa.png")  
#plt.clf()#清除图形 

"""
color = dict(boxes='DarkGreen', whiskers='DarkOrange', medians='DarkBlue', caps='Gray')
In [37]: df.plot.box(color=color, sym='r+')

for box in bp['boxes']:
    # change outline color
    box.set( color='#7570b3', linewidth=2)
    # change fill color
    box.set( facecolor = '#1b9e77' )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='#b2df8a', linewidth=2)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='#e7298a', alpha=0.5)
# /usr/local/lib/python2.7/matplotlib/matplotlib/axes/_axes.py
def bxp(self, bxpstats, positions=None, widths=None, vert=True, patch_artist=False, shownotches=False, showmeans=False,showcaps=True, showbox=True, showfliers=True, boxprops=None, whiskerprops=None, flierprops=None, medianprops=None, capprops=None, meanprops=None, meanline=False, manage_xticks=True, zorder=None):

"""
fig, axes = plt.subplots()

#[z.append([j,]*int(df4.iloc(j,i))) for i in range(len(df4.iloc[0,:i])) ]

for i in range(len(df4.iloc[0,:])):
    [z.append([j,] *int(df4.iloc[j,i])) for j in range(len(df4.iloc[:,i])) if int(df4.iloc[j,i])]
    data.iloc[:,i] = z
    z=[]

            
    [ lambda i,j:z+[j,] *int(df4.iloc[j,i]) for j in range(len(df4.iloc[:,i])) if int(df4.iloc[j,i])]

z +=[[j,] *int(df4.iloc[j,i]) for j in range(len(df4.iloc[:,i])) if int(df4.iloc[j,i])]
[lambda i,j:z+[j,] *int(df4.iloc[j,i]) for j in range(len(df4.iloc[:,i])) if int(df4.iloc[j,i])]

df2 = df.iloc[152:, :]
df2 = df2.set_index(df1.iloc[:,0])

