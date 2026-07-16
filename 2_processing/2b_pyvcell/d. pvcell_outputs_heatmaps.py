import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load data ---
df = pd.read_excel("/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1/ensemble_parameters2DCPC_ic.xlsx")

# Identify parameter columns: from 'Dcyt' to 'Kmplk1' inclusive
cols = list(df.columns)
start = cols.index("Dcyt")
end = cols.index("Kmplk1")
param_cols = cols[start:end + 1]

# Run labels: pull the "ensemble_runN" tail from result_dir
def run_label(path):
    m = re.search(r'(run\d+)$', str(path))
    return m.group(1) if m else str(path)

run_labels = df["result_dir"].apply(run_label)

# Build parameter matrix: rows = parameters, columns = runs
param_matrix = df[param_cols].T
param_matrix.columns = run_labels
param_matrix.index.name = "parameter"

# Readout vector aligned to the same run columns
cpc_ic = pd.Series(df["DCPC_nomr"].values, index=run_labels)

# Order runs (columns) from lowest to highest cpc_ic
order = cpc_ic.sort_values().index
param_matrix = param_matrix[order]
cpc_ic = cpc_ic[order]

# Z-score each parameter (row-wise) so all parameters are visually comparable
# despite very different scales/units.
# z_matrix = param_matrix.sub(param_matrix.mean(axis=1), axis=0).div(param_matrix.std(axis=1), axis=0)

# Normalization with Log2 FC to the reference model (run101)
reference_run = "run101"

if reference_run not in param_matrix.columns:
    raise ValueError(f"{reference_run} not found in run columns")

ref_values = param_matrix[reference_run]

# Guard against zero/negative reference values (log2 of ratio requires positive values)
if (ref_values <= 0).any():
    bad_params = ref_values[ref_values <= 0].index.tolist()
    raise ValueError(f"Reference run has non-positive values for parameters: {bad_params}")

log2fc_matrix = np.log2(param_matrix.div(ref_values, axis=0))


# --- Column color annotation from cpc_ic ---
cmap_readout = sns.color_palette("viridis", as_cmap=True)
norm = matplotlib.colors.Normalize(vmin=cpc_ic.min(), vmax=cpc_ic.max())
col_colors = cpc_ic.map(lambda v: cmap_readout(norm(v)))
col_colors.name = "CPC_ic"

# Set a symmetric range for the log2FC colorbar
# max_abs = np.nanmax(np.abs(log2fc_matrix.values))
# vlim = np.ceil(max_abs)  # round up, or pick a fixed value like 4 or 5

g = sns.clustermap(
    log2fc_matrix,
    row_cluster=True,
    col_cluster=False,
    col_colors=col_colors,
    cmap="RdBu_r",
    center=0,
    # vmin=-vlim,
    # vmax=vlim,
    figsize=(16, 12),
    xticklabels=True,
    yticklabels=True,
    cbar_kws={"label": f"log2FC vs {reference_run}"},
    dendrogram_ratio=(0.12, 0.02),
    colors_ratio=0.02,
)

g.ax_heatmap.set_xlabel("run")
g.ax_heatmap.set_ylabel("parameter")
plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, fontsize=6)
plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0, fontsize=8)

# --- Highlight one specific run label ---
highlight_run = "run101"  # <-- set the run you want highlighted
 
for label in g.ax_heatmap.get_xticklabels():
    if label.get_text() == highlight_run:
        label.set_color("black")
        label.set_backgroundcolor("yellow")
        label.set_fontweight("bold")


g.fig.suptitle("Ensemble parameters (clustered) vs. run, annotated by DCPC", y=1.02, fontsize=13)

# Add a separate colorbar for the cpc_ic column-color annotation
cax = g.fig.add_axes([1.02, 0.4, 0.02, 0.4])
sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap_readout)
sm.set_array([])
cbar = g.fig.colorbar(sm, cax=cax)
cbar.set_label("Normalized DCPC")

g.savefig("/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1/ensemble_nomrparameters_ic_heatmap.pdf", dpi=200, bbox_inches="tight")
print("done")