#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 13:40:07 2022

@author: catalinaalvarez
"""

import pandas as pd
import matplotlib.pyplot as plt
#from scipy.stats import f_oneway
#import numpy as np
#import scipy.stats as stats
import seaborn as sns
from statannotations.Annotator import Annotator

#Reading the raw data
data = pd.read_excel('/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/05-12-26 H2A acetylation quantifications/Western blots/07-31-26 HDACi replicates/09-03-26_acH2A-K118_stoichiometry.xlsx')
df = data.loc[data['treatment'] != 'DMSO']
df
# df = pd.melt(data,
#                   id_vars='treatment',
#                   var_name='ratio',
#                   value_name='replicate')

#df.head()

#%% Seaborn boxplot with statistics - two-tailed independent t-test - With datapoints
f = plt.figure(figsize=[7,7])
sns.set_style("white")
x="treatment"
y="normalized_percentage"
hue="replicate"
ax = sns.boxplot(data=df, x=x, y=y, palette = "Blues")
ax = sns.swarmplot(x=x,y=y, data=df,s=10, edgecolor="black", linewidth=0.5)
#ax = sns.swarmplot(x=x,y=y,hue=hue,data=data,s=10,palette=['yellow','seagreen', 'orange', 'turquoise', 'brown', 'peru', 'darkviolet', 'magenta'], edgecolor="black", linewidth=0.5)
#ax = sns.lineplot(data=data, x=x, y=y, hue=hue, palette=['yellow','seagreen', 'orange', 'turquoise', 'brown', 'peru', 'darkviolet', 'magenta'], estimator=None)
#ax = sns.stripplot(x=x, y=y, hue = hue, data=data, palette = "Greens", edgecolor="black", linewidth=0.5, jitter=True, size=14) # color=".3" makes points grey

annotator  = Annotator(ax, data=df, x=x, y=y,
                    pairs=[ ("G2 arrest", "G2 arrest + 2 uM ENT ")]) #("DMSO", "G2"), ("DMSO", "OA 0.5 uM"),
annotator.configure(test='t-test_ind', text_format='star', loc='inside')
annotator.apply_and_annotate()  
                 
plt.legend(fontsize=7, loc='upper right')
ax.set_xlabel('Treatment', fontsize=16)
ax.set_ylabel('H2A-K118 acetylation (%)', fontsize=16)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
plt.savefig('/Users/catalinaalvarez/Desktop/boxplot_acH2A-K118_stoichiometry.png', dpi=300)
plt.show()