import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 1. LOAD DATA
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/06_26_26_drugresponse_SGO1_ic_at_25s.xlsx"
df = pd.read_excel(file_path)

# Ensure string cleaning
df['percentage'] = df['percentage'].astype(str).str.strip()

# ==============================================================================
# EXPLICIT ORDERING AND MAPPING
# ==============================================================================
# 1. Separate the dataframe rows cleanly by category
df_kd = df[df['percentage'] == 'SGO1 knockdown'].copy()
df_ref = df[df['percentage'] == 'SGO1 reference'].copy()
df_oe = df[df['percentage'] == 'SGO1 overexpression'].copy()

# 2. Re-combine them in strict, predictable sequence
df_sorted = pd.concat([df_kd, df_ref, df_oe]).reset_index(drop=True)

# 3. Extract sorted arrays
y_fc_linear = df_sorted['FC'].to_numpy()
linear_lower = df_sorted['Lower_CI'].to_numpy()
linear_upper = df_sorted['Upper_CI'].to_numpy()
x_pmids = df_sorted['PMID'].astype(str).tolist()

# 4. Transform data
y_fc_log2 = np.log2(y_fc_linear)
log2_upper = np.log2(linear_upper)
log2_lower = np.where(linear_lower > 0, np.log2(linear_lower), np.nan)

# 5. Calculate error distances
upper_error_distance = log2_upper - y_fc_log2
lower_error_distance = np.where(np.isnan(log2_lower), upper_error_distance, y_fc_log2 - log2_lower)
asymmetric_yerr = np.vstack([lower_error_distance, upper_error_distance])
asymmetric_yerr[:, (linear_upper == y_fc_linear) & (linear_lower == y_fc_linear)] = 0

# ==============================================================================
# HARDCODED COORDINATE ALIGNMENT
# ==============================================================================
# X-Axis Ticks
group_ticks = [0.0, 1.0, 2.0]
group_labels = ['SGO1 k.d', 'SGO1 ref', 'SGO1 o.e']

# Exact scatter coordinates for each entry to stagger the first group (Knockdown)
stagger = 0.05
x_scatter_positions = np.array([0.0 - stagger, 0.0 + stagger, 1.0, 2.0])

# Exact line coordinates (Hits the average of the first two points at X=0)
kd_avg = np.mean(y_fc_log2[0:2])
x_line_positions = [0.0, 1.0, 2.0]
y_line_values = [kd_avg, y_fc_log2[2], y_fc_log2[3]]
# ==============================================================================

# 2. SEABORN CONFIGURATION
sns.set_theme(style="whitegrid")
seaborn_dark_orange = "#2b5c8f"

# 7. INITIALIZE THE PLOT CANVAS
fig, ax = plt.subplots(figsize=(8.5, 4.5))

# Plot the linear interpolation across the exact category slots
ax.plot(x_line_positions, y_line_values, linestyle='-', color='black', linewidth=1.2, zorder=1)

# Main data points with error bars
ax.errorbar(x_scatter_positions, y_fc_log2, yerr=asymmetric_yerr, fmt='o', color=seaborn_dark_orange, 
            ecolor=seaborn_dark_orange, elinewidth=1.2, capsize=4, mfc=seaborn_dark_orange, 
            mec=seaborn_dark_orange, ms=16, zorder=5, label='Reported data')

# 8. APPLY CUSTOM AXIS & GRID FORMATTING
ax.set_xticks(ticks=group_ticks)
ax.set_xticklabels(labels=group_labels, fontsize=16, fontweight='bold')
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_ylim(-0.9, 0.1)
ax.axhline(y=0, color="#cccccc", linestyle="--", alpha=0.7, zorder=1)


# ==============================================================================
# FIX: SINGLE COMBINED PMID LABEL FOR KNOCKDOWN Group
# ==============================================================================
# Center a combined string under the first group tick (X=0)
combined_kd_pmid = f"(PMID: {x_pmids[0]}, {x_pmids[1]})"
ax.text(0.0, -0.09, combined_kd_pmid, fontsize=14, color='dimgray', 
        ha='center', va='top', transform=ax.get_xaxis_transform())

# Label the reference point (X=1)
ax.text(1.0, -0.09, f"(PMID: {x_pmids[2]})", fontsize=14, color='dimgray', 
        ha='center', va='top', transform=ax.get_xaxis_transform())

# Label the overexpression point (X=2)
ax.text(2.0, -0.09, f"(PMID: {x_pmids[3]})", fontsize=14, color='dimgray', 
        ha='center', va='top', transform=ax.get_xaxis_transform())
# ==============================================================================

# Configure major grid lines to be transparent black dotted lines
ax.grid(False)

# Force all 4 sides of the plot frame box to be solid black lines
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')
    spine.set_linewidth(1.0)

# Set clean auto-padding margins
ax.margins(y=0.15)

# 9. ADD LABELS, TITLES, & LEGEND
ax.set_ylabel("Centromeric CPC ($log_2$ Fold change)", fontsize=16, labelpad=10)
ax.set_title("Experimental reports", fontsize=16)
# ax.legend(frameon=True, facecolor='white', edgecolor='none', loc='upper right')

# 10. RENDER GRAPH CLEANLY
plt.tight_layout()
plt.savefig("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/SGO1_papers_final4.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
