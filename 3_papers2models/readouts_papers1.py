import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Load data
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/Experimental support.xlsx"
df = pd.read_excel(file_path)

# Convert column to string
df["pubmedID"] = df["pubmedID"].astype(str)
df["cell_line"] = df["cell_line"].astype(str).str.strip()

# Separate literature data from model predictions
df_lit = df[df["pubmedID"] != "Model"].copy()
df_model = df[df["pubmedID"] == "Model"].copy()

# 2. Aggregate Literature: Averages duplicates (e.g., Salimian_2011)
lit_summary = (
    df_lit.groupby(["reporter", "pubmedID", "cell_line"], observed=True)
    .agg(mean_val=("marker_per", "mean"), sem_val=("SEM", "mean"))
    .reset_index()
)

# --- Aggregate Model data too to completely eliminate duplicate matching bugs ---
model_summary = (
    df_model.groupby("reporter", observed=True)
    .agg(marker_per=("marker_per", "mean"))
    .reset_index()
)

# 3. MANUALLY SET YOUR REPORTERS ORDER HERE
# List your exact reporter strings in the sequence you want them to appear on the plot.
# Replace the placeholder names below with your actual Excel column values.
custom_reporter_order = ["pNDC80","pH3T3", "pH3S10"]

# Enforce categorical sequence on literature summary
lit_summary["reporter"] = pd.Categorical(lit_summary["reporter"], categories=custom_reporter_order, ordered=True)
lit_summary = lit_summary.sort_values("reporter").reset_index(drop=True)

# Assign a clean, unique vertical coordinate matching the sorted positions
lit_summary["y_pos"] = np.arange(len(lit_summary))

# Safe Merge: Match clean aggregated model rows to literature vertical positions
model_final = pd.merge(
    lit_summary[["reporter", "y_pos"]],
    model_summary,
    on="reporter",
    how="inner"
)

# 4. Setup the clean figure window
fig, ax_top = plt.subplots(figsize=(5, 3)) # Adjusted height slightly for multi-lane labels
sns.set_theme(style="ticks")
# ax_top = fig.add_axes([0.50, 0.15, 0.20, 0.65])

# --- COORDINATED LAYOUT TRACKS ---
reporter_offset = 0.26
lit_offset = 0.00
model_offset = -0.26

# --- CUSTOM INTER-ROW GRID LINES ---
ax_top.grid(False)
midpoint_offset = (lit_offset + model_offset) / 2 # -0.14

# for y in lit_summary["y_pos"]:
#     ax_top.axhline(y = y + midpoint_offset, color="#cccccc", linestyle="--", alpha=0.7, zorder=1)

# --- PLOT CLEAN DATA TRACKS ---
lit_plot = ax_top.errorbar(
    lit_summary["mean_val"],
    lit_summary["y_pos"] + lit_offset,
    xerr=lit_summary["sem_val"],
    fmt="o",
    color="#2b5c8f",
    markersize=8,
    capsize=5,
    label="Publication",
    zorder=3,
)

model_plot = ax_top.scatter(
    model_final["marker_per"],
    model_final["y_pos"] + model_offset,
    color="#d95f02",
    s=80,
    edgecolor="black",
    label="Model",
    zorder=4,
)

# --- AXIS FORMATTING AND MANUALLY TARGETED LABELS ---
ax_top.set_yticks(lit_summary["y_pos"])
ax_top.set_yticklabels([])
ax_top.set_ylabel("", labelpad=0)

# Dynamic text anchor position for left-side margin metadata
xmin, xmax = 0, 100
text_x_anchor = xmin - (xmax - xmin) * 0.05  

# Loop to map metadata text exactly onto structural data lanes
for _, row in lit_summary.iterrows():
    ax_top.text(
        x=-2, y=row["y_pos"] + reporter_offset, s=str(row["reporter"]),
        fontsize=11, fontweight="bold", color="black", ha="right", va="center"
    )
    ax_top.text(
        x=-2, y=row["y_pos"] + lit_offset, s=f"PMID: {row['pubmedID']}",
        fontsize=9, color="#2b5c8f", ha="right", va="center"
    )
    ax_top.text(
        x=-2, y=row["y_pos"] + model_offset, s="Model prediction",
        fontsize=9, fontweight="semibold", color="#d95f02", ha="right", va="center"
    )

        # On-plot Label for Cell Line directly above the literature data points
    ax_top.text(
        x=row["mean_val"], 
        y=row["y_pos"] + lit_offset + 0.12,  # Slid slightly upward from the literature point
        s=str(row["cell_line"]),
        fontsize=8, 
        fontstyle="italic", 
        color="#2b5c8f", 
        ha="center",       # Perfectly centered horizontally over the dot
        va="bottom"        # Anchored to sit nicely on top of the space
    )

# Set Y-axis padding limits & optionally invert if you want the first list item at the top
ax_top.set_ylim(-0.6, len(lit_summary) - 0.4)
# ax_top.invert_yaxis() # Put first element of custom_reporter_order at the top of the plot

# Top X-Axis Formatting
ax_top.set_xlabel("Phosphorylation stoichiometry", fontsize=12, labelpad=10)
ax_top.xaxis.set_ticks_position("top")
ax_top.xaxis.set_label_position("top")
ax_top.set_xlim(0, 100)

# Explicit, clean legend generation
# ax_top.legend(
#     [lit_plot, model_plot], ["Publication", "Model"],
#     loc="upper left", bbox_to_anchor=(1.05, 1.0), frameon=True
# )

# Remove unneeded plot boundaries
sns.despine(ax=ax_top, top=False, bottom=False, right=False, left=False)

# Save the figure with dynamic bounding box bounding calculations to prevent text clipping
plt.savefig(
    "/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/Readouts_celllines.pdf",
    format="pdf",
    bbox_inches="tight",
    dpi=300
)
plt.show()