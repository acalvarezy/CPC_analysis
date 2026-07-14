import matplotlib.pyplot as plt
import numpy as np

# Define time axis (0 to 8 minutes)
t = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

# Trace definitions
trace1 = np.array([4, 13.0, 10.3, 5.7, 2.8, 1.3, 0.6, 0.4, 0.3])
trace2 = np.array([4, 5.5, 10.0, 13, 13.5, 12.9, 9.5, 5.0, 1.5])

# ---- COLOR CONFIGURATION ----
# Edit these hex codes or use names like 'red', 'blue', 'black', 'green'
COLOR_1 = "#217AAE"  
COLOR_2 = "#ED3049"
# -----------------------------

# Initialize plot with explicit white backgrounds
fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
ax.set_facecolor('white')

# Plot lines without marker shapes
ax.plot(t, trace1, color=COLOR_1, linewidth=5)
ax.plot(t, trace2, color=COLOR_2, linewidth=5)

# Place text labels directly at the end of each data line
# x=8.2 adds a tiny gap after the last data point (t=8)
ax.text(0.5, 1, 'Proper attachments', color=COLOR_1, fontsize=24, va='center')
ax.text(5.5, 12, 'No attachments', color=COLOR_2, fontsize=24, va='center')

# Set constraints
ax.set_xlim(0, 8)
ax.set_ylim(0, 15)
ax.set_xlabel('time', fontsize=26)
ax.set_ylabel(r"$[CPC]_{ic}$", fontsize=26)

# Remove the grid completely
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Clean styling for the legend box
# ax.legend(fontsize=20, frameon=True, facecolor='white', edgecolor='none')
# ax.set_xticklabels([])
# ax.set_yticklabels([])
plt.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
plt.savefig("/Users/catalinaalvarez/Documents/GitHub/CPC_analysis/3_additional_plots/sketch2.pdf")
plt.show()
