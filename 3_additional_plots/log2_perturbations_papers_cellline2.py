import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set theme globally at the top to prevent layout interference
sns.set_theme(style="ticks")

# 1. Load and prepare data
file_path = r"/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/Experimental support.xlsx"
df = pd.read_excel(file_path)

# Convert column to string
df["pubmedID"] = df["pubmedID"].astype(str)

# --- PRESET THE REPORTER DISPLAY ORDER ---
# List your reporters in the exact order you want them to appear from BOTTOM to TOP on the plot
reporter_order = [
    "HASPIN inh",
    "BUB1 inh",
    "AURKB inh",
    # "Advection (M2)",
    # "Advection (M1)"
]

# Convert the column to a Categorical type with your custom sorting rules
df["reporter"] = pd.Categorical(df["reporter"], categories=reporter_order, ordered=True)

# --- APPLY LOG2 TRANSFORMATION TO DATA AND CI BOUNDS ---
df["marker_per_log2"] = np.log2(df["marker_per"])
df["Lower_CI_log2"] = np.log2(df["Lower_CI"])
df["Upper_CI_log2"] = np.log2(df["Upper_CI"])

# Separate transformed literature data from model predictions
df_lit = df[df["pubmedID"] != "Model"].copy()
df_model = df[df["pubmedID"] == "Model"].copy()

# 2. Aggregate unique literature rows (averaging triplicates into 1 row per reporter)
# Includes cell_line in the aggregation step
lit_summary = (
    df_lit.groupby(["reporter"], observed=False)
    .agg(
        mean_val=("marker_per_log2", "mean"),
        lower_val=("Lower_CI_log2", "mean"),
        upper_val=("Upper_CI_log2", "mean"),
        pubmedID=("pubmedID", "first"),
        cell_line=("cell_line", "first") 
    )
    .reset_index()
    .sort_values("reporter")
    .reset_index(drop=True)
)

# Force positive error distances for Matplotlib's asymmetric error mapping
xerr_lower = np.abs(lit_summary["mean_val"] - lit_summary["lower_val"])
xerr_upper = np.abs(lit_summary["upper_val"] - lit_summary["mean_val"])
asymmetric_error = np.vstack([xerr_lower, xerr_upper])

# Assign baseline sequential vertical positions (where the dashed lines will sit)
lit_summary["y_pos"] = np.arange(len(lit_summary))

# Vectorized Merge: Match model data to literature positions on the shared "reporter"
model_summary = pd.merge(
    lit_summary[["reporter", "y_pos"]],
    df_model[["reporter", "marker_per_log2"]],
    on="reporter",
    how="inner"
)

# 3. Setup the figure window and dual X-axes
fig, ax_top = plt.subplots(figsize=(8, 4)) 
ax_bottom = ax_top.twiny()

# --- CUSTOM INTER-ROW GRID LINES ---
ax_top.axvline(x=0, color="#cccccc", linestyle="--", alpha=0.7, zorder=1)

# # Horizontal tracks separating the reporter rows
# for y in lit_summary["y_pos"]:
#     ax_top.axhline(y=y + 0.5, color="#e0e0e0", linestyle="-", linewidth=0.5, zorder=1)

# --- COORDINATED LAYOUT TRACKS ---
reporter_offset = 0.28
lit_offset = 0.00
model_offset = -0.28

# --- PLOT LOG2 DATA WITH ASYMMETRIC CI ERROR BARS ---
lit_plot = ax_top.errorbar(
    lit_summary["mean_val"],
    lit_summary["y_pos"] + lit_offset, # Aligned perfectly with the PMID row
    xerr=asymmetric_error,
    fmt="o",
    color="#2b5c8f",
    markersize=9,
    capsize=5,
    label="Publication",
    zorder=3,
)

# --- PLOT MODEL PREDICTIONS ---
model_plot = ax_top.scatter(
    model_summary["marker_per_log2"],
    model_summary["y_pos"] + model_offset, # Aligned perfectly with the Model row
    color="#d95f02",
    s=90,
    edgecolor="black",
    label="Model",
    zorder=4,
)

# --- AXIS FORMATTING AND LABELS ---
ax_top.set_yticks(lit_summary["y_pos"])
ax_top.set_yticklabels([])
ax_top.set_ylabel("", labelpad=0)

# --- EXTERNAL MARGIN LABELS (REPORTER, PMID, & MODEL) ---
transform_fixed = ax_top.get_yaxis_transform()
label_x_position = -0.04  # Positions labels cleanly outside left axis wall

for _, row in lit_summary.iterrows():
    # Track 1: Primary bold header sitting above the data points
    ax_top.text(
        x=label_x_position,
        y=row["y_pos"] + reporter_offset,
        s=row["reporter"],
        transform=transform_fixed,
        fontsize=16,
        fontweight="bold",
        color="black",
        ha="right",
        va="center"
    )
    
    # Track 2: PMID left on the axis track, aligned with the blue publication data row
    ax_top.text(
        x=label_x_position,
        y=row["y_pos"] + lit_offset,
        s=f"PMID: {row['pubmedID']}",
        transform=transform_fixed,
        fontsize=14,
        color="#2b5c8f", 
        ha="right",
        va="center"
    )
    
    # Track 3: Direct pairing with the orange model point
    # ax_top.text(
    #     x=label_x_position,
    #     y=row["y_pos"] + model_offset,
    #     s="Model prediction",
    #     transform=transform_fixed,
    #     fontsize=9,
    #     fontweight="semibold",
    #     color="#d95f02",
    #     ha="right",
    #     va="center"
    # )

# --- INTERNAL PLOT LABELS (CELL LINE ONLY ABOVE BLUE MARKERS) ---
for _, row in lit_summary.iterrows():
    text_x = row["mean_val"]
    text_y = row["y_pos"] + lit_offset + 0.12  # Placed slightly above the marker [1]
    
    ax_top.text(
        x=text_x,
        y=text_y,
        s=row['cell_line'],
        transform=ax_top.transData, # Locks directly to graph coordinate numbers
        fontsize=14,
        fontweight="medium",
        color="#2b5c8f",            # Color matched to blue marker [1]
        ha="center",                # Horizontally centers text over data marker [1]
        va="bottom",
        zorder=5,
        # Semi-transparent backing so error bar tracks don't cross through text lines
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8)
    )
    
for _, row in model_summary.iterrows():
    ax_top.text(
        x=row["marker_per_log2"],
        y=row["y_pos"] + model_offset - 0.12,  # Slid slightly downward from the model point
        s="Model",
        fontsize=14,
        fontweight="semibold",
        color="#d95f02",
        ha="center",                           # Perfectly centered horizontally under the dot
        va="top"                               # Anchored to sit nicely below the point
    )


# Set Y-axis padding limits so the text/markers don't cut off at boundaries
ax_top.set_ylim(-0.6, len(lit_summary) - 0.4)

# Top X-Axis Formatting
ax_top.set_xlabel("Centromeric CPC ($log_2$ Fold change)", fontsize=16, labelpad=10)
ax_top.xaxis.set_ticks_position("top")
ax_top.xaxis.set_label_position("top")
ax_top.tick_params(axis='x', labelsize=14)

# Bottom X-Axis Cleanup
ax_bottom.set_xlim(ax_top.get_xlim())
ax_bottom.set_xticks([])
ax_bottom.set_xticklabels([])
ax_bottom.set_xlabel("", labelpad=0)

# Explicit, clean legend generation
# ax_top.legend(
#     [lit_plot, model_plot],
#     ["Publication", "Model"],
#     loc="upper left",
#     bbox_to_anchor=(1.05, 1.0),
#     frameon=True
# )

sns.despine(ax=ax_top, top=False, bottom=False, right=True)

# Restored the wide left margin since PMID/Model text is back on the axis frame
plt.tight_layout()
fig.subplots_adjust(left=0.38) 

# Save the figure
plt.savefig(
    "/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/Perturbation_uplow.pdf",
    format="pdf",
    bbox_inches="tight",
    dpi=300
)
plt.show()