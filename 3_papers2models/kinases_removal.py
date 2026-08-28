import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/kinases_removal.xlsx"
df = pd.read_excel(file_path)
print(df)

# ---- COLOR CONFIGURATION ---- #
COLOR_1 = "#2b5c8f"
COLOR_2 = "#d95f02"
# ----------------------------- #

fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')

# ---- DATA FILTERING & PLOTTING ---- #
# We drop rows where Time or the specific metric is NA to keep lines continuous.

# 1. DMSO Paper
df_dmso_paper = df.dropna(subset=['Time', 'DMSO_paper'])
plt.scatter(df_dmso_paper['Time'], df_dmso_paper['DMSO_paper'], color=COLOR_1, s=150, zorder=3, label = "PMID: 38614097")
plt.plot(df_dmso_paper['Time'], df_dmso_paper['DMSO_paper'], color=COLOR_1, linestyle='-', linewidth=3, zorder=2, label='DMSO')

# 2. Kinase Removal Paper
df_krem_paper = df.dropna(subset=['Time', 'kremoval_paper'])
plt.scatter(df_krem_paper['Time'], df_krem_paper['kremoval_paper'], color=COLOR_1, s=150, zorder=3)
plt.plot(df_krem_paper['Time'], df_krem_paper['kremoval_paper'], color=COLOR_1, linestyle=':', linewidth=4, zorder=2, label='5-ITU + BAY')

# # 3. DMSO Model
# df_dmso_model = df.dropna(subset=['Time', 'DMSO_model'])
# plt.scatter(df_dmso_model['Time'], df_dmso_model['DMSO_model'], color=COLOR_2, s=150, zorder=3, label='Model')
# plt.plot(df_dmso_model['Time'], df_dmso_model['DMSO_model'], color=COLOR_2, linestyle='-', linewidth=3, zorder=2)

# 4. Kinase Removal Model
df_krem_model = df.dropna(subset=['Time', 'kremoval_model2'])
plt.scatter(df_krem_model['Time'], df_krem_model['kremoval_model2'], color=COLOR_2, s=150, zorder=3, label='Model + bivalent binding')
plt.plot(df_krem_model['Time'], df_krem_model['kremoval_model2'], color=COLOR_2, linestyle=':', linewidth=4, zorder=2)


# Set constraints
ax.set_xlim(-10, 38)
ax.set_ylim(-0.2, 2)
ax.set_xlabel('Time (minutes)', fontsize=18)
ax.set_ylabel(r"Normalized centromeric CPC", fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.axvline(x=27, color="#cccccc", linestyle="--", alpha=0.7, zorder=1, linewidth=3)
leg = plt.legend(fontsize=15)
# leg = plt.legend(title="PMID: 38614097", title_fontsize=16, fontsize=15)
# leg.get_title().set_weight('bold')
plt.tight_layout() # Ensures labels fit nicely in the PDF
plt.savefig("/Users/catalinaalvarez/Documents/GitHub/CPC_analysis/3_papers2models/kinases_removal_paperFig5HI_ivalues_model2_0m_2.pdf")
plt.show()