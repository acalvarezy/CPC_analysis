import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.interpolate import make_interp_spline


# 1. Load and prepare data
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/06_26_26_drugresponse_SGO1_ic_at_25s.xlsx"
df = pd.read_excel(file_path)

# 2. Set the Seaborn theme and palette
# 'whitegrid' provides a clean background with subtle lines
sns.set_theme(style="whitegrid")
# Pick a nice modern palette (e.g., 'deep', 'muted', 'pastel', 'dark', 'colorblind')
colors = "#d95f02"

# 3. Get categorical labels and create temporary numeric indices
x_labels = df['percentage'].astype(str).tolist()
x_indices = np.arange(len(x_labels)) 
y_fc = df['FC'].to_numpy()
y_fclog2 = np.log2(y_fc)

# # 4. Generate a detailed grid for the smooth curve
# x_smooth_indices = np.linspace(x_indices.min(), x_indices.max(), 300) 
# spline = make_interp_spline(x_indices, y_fclog2, k=3)
# y_smooth = spline(x_smooth_indices)

# 5. Create the plot using Seaborn-optimized sizing
fig, ax = plt.subplots(figsize=(8, 5))

# Thin (linewidth=1.2) and solid black line trace
ax.plot(x_labels, y_fclog2, linestyle='-', color='black', linewidth=1.2)

# Clean, modern markers using Seaborn's muted palette accents
ax.scatter(x_indices, y_fclog2, color= sns.color_palette("dark")[1], s=150, zorder=3, label='Model prediction')
ax.set_xticks(ticks=x_indices)
ax.set_xticklabels(labels=x_labels, fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=14) 
ax.set_ylim(-0.9, 0.1)

# 6. GRID AND AXIS STYLING
ax.grid(True, which='both', linestyle=':', color='gray', alpha=0.3)

# Set the outer frame borders for a modern Seaborn aesthetic
for spine in ax.spines.values():
    spine.set_visible(True)        # Ensure all sides are visible
    spine.set_color('black')       # Force the contour color to black
    spine.set_linewidth(1.0)       # Set a clean, clear border thickness

# 7. Add labels, grid styling, and titles via Seaborn/Matplotlib rules
plt.xlabel('SGO1 concentration', fontsize=16, labelpad=10)
plt.ylabel("Centromeric CPC ($log_2$ Fold change)", fontsize=16, labelpad=10)
# plt.title('Categorical Percentage vs. FC (Smoothed)', fontsize=14, fontweight='bold', pad=15)

# # Clean up axes (removes the outer box border for a modern look)
# sns.despine(left=True, bottom=True)

plt.legend(frameon=True, facecolor='white', edgecolor='none')

# 8. Display the graph
plt.tight_layout()
plt.savefig("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/SGO1_model_final.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()