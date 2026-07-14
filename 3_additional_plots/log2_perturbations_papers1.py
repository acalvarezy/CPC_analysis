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
    "Advection (M2)",
    "Advection (M1)"
    # f"Advection\n(Measure 2)", 
    # f"Advection\n(Measure 1)"

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
lit_summary = (
    df_lit.groupby(["reporter"], observed=False)
    .agg(
        mean_val=("marker_per_log2", "mean"), 
        lower_val=("Lower_CI_log2", "mean"),
        upper_val=("Upper_CI_log2", "mean"),
        pubmedID=("pubmedID", "first")
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
fig, ax_top = plt.subplots(figsize =(10, 4)) 
ax_bottom = ax_top.twiny()                  

# Grid lines will draw exactly at integers (0, 1, 2...), matching the baseline
ax_top.grid(True, axis="y", linestyle="--", alpha=0.5)

# --- COORDINATED LAYOUT TRACKS ---
# Track 1: Reporter Name (Header above)
# Track 2: Publication Data Point & PMID Label (Middle slot)
# Track 3: Model Data Point & "Model prediction" Label (Bottom slot)
reporter_offset = 0.28
lit_offset = 0.00
model_offset = -0.28

# --- CUSTOM INTER-ROW GRID LINES ---
# Turn off standard grid so we can draw lines manually exactly between the data points
ax_top.grid(False)
midpoint_offset = (lit_offset + model_offset) / 2  # Computes the exact space between them (-0.14)

# for y in lit_summary["y_pos"]:
#     ax_top.axhline(y = y + midpoint_offset, color="#cccccc", linestyle="--", alpha=0.7, zorder=1)

ax_top.axvline(x = 0, color="#cccccc", linestyle="--", alpha=0.7, zorder=1)


# --- PLOT LOG2 DATA WITH ASYMMETRIC CI ERROR BARS ---
lit_plot = ax_top.errorbar(
    lit_summary["mean_val"],
    lit_summary["y_pos"] + lit_offset,  # Aligned perfectly with the PMID row
    xerr=asymmetric_error, 
    fmt="o",
    color="#2b5c8f",
    markersize=8,
    capsize=5,
    label="Publication",
    zorder=3,
)

# --- PLOT MODEL PREDICTIONS ---
model_plot = ax_top.scatter(
    model_summary["marker_per_log2"],  
    model_summary["y_pos"] + model_offset,  # Aligned perfectly with the Model row
    color="#d95f02",
    s=80,
    edgecolor="black",
    label="Model",
    zorder=4,
)

# --- AXIS FORMATTING AND LABELS ---

# Clear default labels to apply strict multi-level row alignment
ax_top.set_yticks(lit_summary["y_pos"])
ax_top.set_yticklabels([]) 
ax_top.set_ylabel("", labelpad=0) 

# --- Pushed x from -0.02 to -0.05 to create more horizontal buffer ---
label_padding_x = -0.05


# Loop to manually map labels directly to their structural data lanes
for _, row in lit_summary.iterrows():
    # Track 1: Primary bold header sitting above the data points
    ax_top.text(
        x=-0.02,                         
        y=row["y_pos"] + reporter_offset,           
        s=row["reporter"],               
        transform=ax_top.get_yaxis_transform(),  
        fontsize=11,                    
        fontweight="bold",
        color="black",                 
        ha="right",                      
        va="center"                         
    )
    
    # Track 2: Direct pairing with the blue publication point
    ax_top.text(
        x=-0.02,                         
        y=row["y_pos"] + lit_offset,           
        s=f"PMID: {row['pubmedID']}",               
        transform=ax_top.get_yaxis_transform(),  
        fontsize=9,                    
        color="#2b5c8f",     # Color-coded to match the marker exactly             
        ha="right",                      
        va="center"                         
    )
    
    # Track 3: Direct pairing with the orange model point
    ax_top.text(
        x=-0.02,                         
        y=row["y_pos"] + model_offset,           
        s="Model prediction",               
        transform=ax_top.get_yaxis_transform(),  
        fontsize=9,
        fontweight="semibold",
        color="#d95f02",     # Color-coded to match the marker exactly           
        ha="right",                      
        va="center"                         
    )

# Set Y-axis padding limits so the text/markers don't cut off at top or bottom boundaries
ax_top.set_ylim(-0.6, len(lit_summary) - 0.4)

# Top X-Axis Formatting
ax_top.set_xlabel("Centromeric CPC ($log_2$ Fold change)", fontsize=12, labelpad=10)
ax_top.xaxis.set_ticks_position("top")
ax_top.xaxis.set_label_position("top")

# Bottom X-Axis Cleanup
ax_bottom.set_xlim(ax_top.get_xlim())
ax_bottom.set_xticks([]) 
ax_bottom.set_xticklabels([])
ax_bottom.set_xlabel("", labelpad=0) 

# Explicit, clean legend generation
ax_top.legend(
    [lit_plot, model_plot], 
    ["Publication", "Model"], 
    loc="upper left",             
    bbox_to_anchor=(1.05, 1.0),   
    frameon=True
)

sns.despine(ax=ax_top, top=False, bottom=False, right=True)

# Adjust margins to allocate space on the left to prevent label clipping
plt.tight_layout()
fig.subplots_adjust(left=0.36)  # Expanded margin for "Model prediction" text width

# Save the figure
plt.savefig("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC PAPER/Supplementary material/Experimental support/perturbations_final2.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()