#%%
import os
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SETUP DIRECTORIES & FILES ---
working_dir = '/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/08-26 All acetylation quantifications/07-25-26 H2A acetylation/Replicate 3'
#05-09-25 acetylation spreads
#05-12-25 H2A acetylation replicate 1
os.chdir(working_dir)

# --- READ DATA ---
df = pd.read_excel('all_data_master_summary.xlsx')

# --- Plot ratios per cell --- 
metrics = ["Mean", "Median", "uq75", "uq80", "uq90"]

for i in metrics:
    plt.figure(figsize=(8, 6))
    ax = sns.violinplot(data=df, x="cell", y=f"Ratio_{i}_Outside_Inside", palette= "viridis", cut=0, width=1.1)
    sns.swarmplot(data=df, x="cell", y="Ratio_Mean_Outside_Inside", color="black", size=4, alpha=0.5)
    ax.set_ylabel(f"{i} ratio (Outside/ Inside)")
    plt.savefig(f"Ratio_per_cell_{i}_violin.png", dpi=300) 
    plt.show()


# --- Plot ratios per chromosome length --- 
for i in metrics:
    plt.figure(figsize=(8, 6))    
    ax = sns.scatterplot(data=df, x="Chromosome_length", y=f"Ratio_{i}_Outside_Inside", hue = 'cell', palette="Paired", s=100, alpha = 0.9)
    ax.axhline(y=2, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.axhline(y=1.5, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.set_xlabel("Chromosome length", fontsize=14)
    ax.set_ylabel(f"{i} ratio (Outside CR/ inside CR)", fontsize=14)
    sns.move_legend(ax, loc="best", title="Cell")
    plt.savefig(f"{i}2length_distribution.png", dpi=300) 
    plt.show()


# --- Plot ratios per centromeric intensity --- 
for i in metrics:
    plt.figure(figsize=(8, 6))    
    ax = sns.scatterplot(data=df, x="Inside_Mean_acH2A", y=f"Ratio_{i}_Outside_Inside", hue = 'cell', palette="Paired", s=100, alpha = 0.9)
    ax.axhline(y=2, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.axhline(y=1.5, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.set_xlabel("Average centromere intensity", fontsize=14)
    ax.set_ylabel(f"{i} ratio (Outside CR/ inside CR)", fontsize=14)
    sns.move_legend(ax, loc="best", title="Cell")
    plt.savefig(f"{i}2centromereInt_distribution.png", dpi=300) 
    plt.show()

# --- Plot ratios per outside intensity --- 
for i in metrics:
    plt.figure(figsize=(8, 6))    
    ax = sns.scatterplot(data=df, x="Outside_Mean_acH2A", y=f"Ratio_{i}_Outside_Inside", hue = 'cell', palette="Paired", s=100, alpha = 0.9)
    ax.axhline(y=2, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.axhline(y=1.5, color="gray", linestyle="--", linewidth=1, label="_nolegend_")
    ax.set_xlabel("Average arms intensity", fontsize=14)
    ax.set_ylabel(f"{i} ratio (Outside CR/ inside CR)", fontsize=14)
    sns.move_legend(ax, loc="best", title="Cell")
    plt.savefig(f"{i}2armsInt_distribution.png", dpi=300) 
    plt.show()


# --- Plot centromeric intensity vs. chromosome length --- 
for i in metrics:
    plt.figure(figsize=(8, 6))    
    ax = sns.scatterplot(data=df, x="Chromosome_length", y=f'Inside_{i}_acH2A', hue = 'cell', palette="Paired", s=100, alpha = 0.9)
    ax.set_xlabel("Chromosome length", fontsize=14)
    ax.set_ylabel(f"{i} centromeric intensity", fontsize=14)
    sns.move_legend(ax, loc="best", title="Cell")
    plt.savefig(f"{i}_length2centromericIntensity.png", dpi=300) 
    plt.show()


# --- Plot centromeric intensity vs. arm intensities --- 
for i in metrics:
    plt.figure(figsize=(8, 6))    
    ax = sns.scatterplot(data=df, x=f'Inside_{i}_acH2A', y=f'Outside_{i}_acH2A', hue = 'cell', palette="Paired", s=100, alpha = 0.9)
    ax.axline((0, 0), slope=1, color='black', linestyle='--', zorder=0)
    ax.set_xlabel(f"{i} centromeric intensity", fontsize=14)
    ax.set_ylabel(f"{i} arms intensity", fontsize=14)
    sns.move_legend(ax, loc="best", title="Cell")
    plt.savefig(f"{i}_centromeric2arms_intensity.png", dpi=300) 
    plt.show()



#Data
# mean_inside = df['']
