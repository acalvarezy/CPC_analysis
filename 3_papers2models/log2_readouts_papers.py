import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline

# 1. LOAD DATA
# Replace 'your_new_file.xlsx' with your actual file path
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/06_26_26_drugresponse_SGO1_ic_at_25s.xlsx"
df = pd.read_excel(file_path)

# 2. SEABORN CONFIGURATION
sns.set_theme(style="whitegrid")
seaborn_color = "#2b5c8f"

# 3. EXTRACT VALUES & PRE-CALCULATED CI BOUNDARIES
y_fc_linear = df['FC'].to_numpy()
linear_lower = df['Lower_CI'].to_numpy()  # Your custom Lower CI column name
linear_upper = df['Upper_CI'].to_numpy()  # Your custom Upper CI column name

# 4. DIRECT LOG2 TRANSFORMATION
y_fc_log2 = np.log2(y_fc_linear)
log2_upper = np.log2(linear_upper)

# Handle lower bounds safely: if a lower limit is 0 or negative, log2 becomes NaN
log2_lower = np.where(linear_lower > 0, np.log2(linear_lower), np.nan)

# 5. CALCULATE EXACT ERROR BAR DISTANCES FOR MATPLOTLIB
# Matplotlib needs the distance FROM the center point to the edge
upper_error_distance = log2_upper - y_fc_log2

# If lower bound is NaN (invalid for log), match the upper distance to keep it clean
lower_error_distance = np.where(np.isnan(log2_lower), upper_error_distance, y_fc_log2 - log2_lower)
asymmetric_yerr = np.vstack([lower_error_distance, upper_error_distance])

# Clean up baseline reference values (if upper and lower match the center, error is 0)
asymmetric_yerr[:, (linear_upper == y_fc_linear) & (linear_lower == y_fc_linear)] = 0

# Clean strings for labels
x_conditions = df['percentage'].astype(str).tolist()
x_pmids = df['PMID'].astype(str).tolist()
x_indices = np.arange(len(x_conditions)) 

# 6. COMPUTE THE SMOOTH CURVE INTERPOLATION
x_smooth_indices = np.linspace(x_indices.min(), x_indices.max(), 300) 
spline = make_interp_spline(x_indices, y_fc_log2, k=2) 
y_smooth = spline(x_smooth_indices)

# 7. INITIALIZE THE PLOT CANVAS
fig, ax = plt.subplots(figsize=(8.5, 5))

# Plot the thin black smoothed trend line
ax.plot(x_smooth_indices, y_smooth, linestyle='-', color='black', linewidth=1.2)

# Plot data points with your exact direct-log2 confidence interval limits
ax.errorbar(x_indices, y_fc_log2, yerr=asymmetric_yerr, fmt='o', color=seaborn_color, 
            ecolor=seaborn_color, elinewidth=1.2, capsize=4, mfc=seaborn_color, 
            mec=seaborn_color, ms=7, zorder=5, label='Publication')

# 8. APPLY CUSTOM AXIS & GRID FORMATTING
ax.set_xticks(ticks=x_indices)
ax.set_xticklabels(labels=x_conditions, fontsize=12, fontweight='bold') 

# Draw the small, simple PMID text underneath using a stable layout offset
for idx, pmid in zip(x_indices, x_pmids):
    ax.text(idx, -0.08, f"(PMID: {pmid})", 
            fontsize=8.5, color='dimgray', ha='center', va='top', transform=ax.get_xaxis_transform())

# Configure major grid lines to be transparent black dotted lines
ax.grid(True, which='major', linestyle=':', color='black', alpha=0.3)

# Force all 4 sides of the plot frame box to be solid black lines
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')
    spine.set_linewidth(1.0)

# Set clean auto-padding margins
ax.margins(y=0.15)

# 9. ADD LABELS, TITLES, & LEGEND
# ax.set_xlabel('Condition / Dataset Reference', fontsize=11, labelpad=35) 
ax.set_ylabel('Centromeric CPC ($log_2$ Fold change)', fontsize=11, labelpad=10)
# ax.set_title('SGO1 Expression Analysis (Direct Log2 CI Boundaries)', fontsize=13, fontweight='bold', pad=15)
ax.legend(frameon=True, facecolor='white', edgecolor='none')

# 10. RENDER GRAPH CLEANLY
plt.tight_layout()
plt.savefig("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/SGO1_papers.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()