"""
acH2A Outside/Inside Ratio Analysis
====================================
Reproduces the full analysis pipeline performed on
`all_data_master_summary_R1-4.xlsx`:

  1. Load and inspect the data
  2. Per-replicate (R1-R4) linear-scale violin plots for all 5 ratio
     statistics (Mean, Median, UQ75, UQ80, UQ90)
  3. Log-scale violin plots for Mean and Median, by replicate
  4. Combined analysis: all replicates pooled together, Mean vs.
     Median ratio distributions (log scale)

Usage:
    python acH2A_ratio_analysis.py <path_to_xlsx> [output_dir]

Outputs (written to output_dir, default: current directory):
    - linear_ratios_stacked.png        (Section 2)
    - log_mean_median_by_replicate.png (Section 3)
    - combined_mean_median_violin.png  (Section 4)
"""

import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# SECTION 1: Load and inspect the data
# ---------------------------------------------------------------------------
def load_data(input_path: str) -> pd.DataFrame:
    """Load the master summary spreadsheet."""
    df = pd.read_excel(input_path)
    print(f"Loaded {len(df)} rows from {input_path}")
    print(f"Replicates found: {sorted(df['replicate'].unique())}")
    return df


# Ratio columns and their display labels, used throughout the script
RATIO_COLS = [
    "Ratio_Mean_Outside_Inside",
    "Ratio_Median_Outside_Inside",
    "Ratio_uq75_Outside_Inside",
    "Ratio_uq80_Outside_Inside",
    "Ratio_uq90_Outside_Inside",
]
RATIO_LABELS = ["Mean", "Median", "UQ75", "UQ80", "UQ90"]


def _violin_panel(ax, data, x, y, order, log_scale=False, title=""):
    """Helper: draw one violin + strip plot panel, optionally on log scale.

    If log_scale is True and the column contains non-positive values,
    those rows are dropped for this panel only (log is undefined for
    values <= 0), and the exclusion is noted in the panel title.
    """
    sub = data.dropna(subset=[y])
    suffix = ""

    if log_scale:
        n_dropped = (sub[y] <= 0).sum()
        if n_dropped > 0:
            sub = sub[sub[y] > 0]
            suffix = f" (log scale; {n_dropped} non-positive value(s) excluded)"
        else:
            suffix = " (log scale)"

    sns.violinplot(
        data=sub, x=x, y=y, order=order, hue=x,
        palette="Set2", cut=0, inner="box", ax=ax, legend=False,
    )
    sns.stripplot(
        data=sub, x=x, y=y, order=order,
        color="black", alpha=0.4, size=3, jitter=True, ax=ax,
    )
    if log_scale:
        ax.set_yscale("log")
    ax.set_title(f"{title}{suffix}")
    ax.set_xlabel(x.capitalize() if x != "replicate" else "Replicate")


# ---------------------------------------------------------------------------
# SECTION 2: Per-replicate linear-scale violin plots (all 5 ratios)
# ---------------------------------------------------------------------------
def plot_linear_by_replicate(df: pd.DataFrame, order, output_path: str):
    """
    Linear-scale violin plots of each ratio statistic, split by
    replicate (R1-R4), stacked vertically into one figure.
    """
    sns.set_theme(style="whitegrid", font_scale=1.05)
    fig, axes = plt.subplots(len(RATIO_COLS), 1, figsize=(7, 4.5 * len(RATIO_COLS)))

    for ax, col, lab in zip(axes, RATIO_COLS, RATIO_LABELS):
        _violin_panel(
            ax, df, x="replicate", y=col, order=order, log_scale=False,
            title=f"{lab} — Outside/Inside acH2A Ratio by Replicate",
        )
        ax.set_ylabel(f"Ratio (Outside/Inside), {lab} acH2A")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Section 2 saved: {output_path}")


# ---------------------------------------------------------------------------
# SECTION 3: Log-scale violin plots for Mean and Median, by replicate
# ---------------------------------------------------------------------------
def plot_log_mean_median_by_replicate(df: pd.DataFrame, order, output_path: str):
    """
    Log-scale violin plots of the Mean and Median ratios, split by
    replicate. Mean is strictly positive; Median has one non-positive
    value that is excluded for this log view (noted in the title).
    """
    sns.set_theme(style="whitegrid", font_scale=1.05)
    fig, axes = plt.subplots(2, 1, figsize=(7, 9))

    log_cols = RATIO_COLS[:2]     # Mean, Median
    log_labels = RATIO_LABELS[:2]

    for ax, col, lab in zip(axes, log_cols, log_labels):
        _violin_panel(
            ax, df, x="replicate", y=col, order=order, log_scale=True,
            title=f"{lab} — Outside/Inside acH2A Ratio by Replicate",
        )
        ax.set_ylabel(f"Ratio (Outside/Inside), {lab} acH2A")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Section 3 saved: {output_path}")


# ---------------------------------------------------------------------------
# SECTION 4: Combined analysis — all replicates pooled together
# ---------------------------------------------------------------------------
def plot_combined_mean_median(df: pd.DataFrame, output_path: str):
    """
    Pool all replicates (R1-R4) into a single group and compare the
    Mean vs. Median ratio distributions on a log scale.
    """
    mean_sub = df.dropna(subset=["Ratio_Mean_Outside_Inside"])
    median_sub = df.dropna(subset=["Ratio_Median_Outside_Inside"])
    n_dropped = (median_sub["Ratio_Median_Outside_Inside"] <= 0).sum()
    median_sub = median_sub[median_sub["Ratio_Median_Outside_Inside"] > 0]

    combined = pd.DataFrame({
        "Ratio": pd.concat(
            [mean_sub["Ratio_Mean_Outside_Inside"],
             median_sub["Ratio_Median_Outside_Inside"]],
            ignore_index=True,
        ),
        "Statistic": ["Mean"] * len(mean_sub) + ["Median"] * len(median_sub),
    })

    sns.set_theme(style="whitegrid", font_scale=1.1)
    fig, ax = plt.subplots(figsize=(7, 6))

    sns.violinplot(
        data=combined, x="Statistic", y="Ratio", hue="Statistic",
        palette="Set2", cut=0, inner="box", ax=ax, legend=False,
    )
    sns.stripplot(
        data=combined, x="Statistic", y="Ratio",
        color="black", alpha=0.4, size=3, jitter=True, ax=ax,
    )
    ax.set_yscale("log")
    ax.set_xlabel("")
    ax.set_ylabel("Ratio (Outside/Inside), acH2A")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Section 4 saved: {output_path} "
          f"(Median excluded {n_dropped} non-positive value(s))")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "all_data_master_summary_R1-4.xlsx"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(output_dir, exist_ok=True)

    df = load_data(input_path)
    order = sorted(df["replicate"].unique())

    plot_linear_by_replicate(
        df, order, os.path.join(output_dir, "linear_ratios_stacked.png")
    )
    plot_log_mean_median_by_replicate(
        df, order, os.path.join(output_dir, "log_mean_median_by_replicate.png")
    )
    plot_combined_mean_median(
        df, os.path.join(output_dir, "combined_mean_median_violin.png")
    )


if __name__ == "__main__":
    main()