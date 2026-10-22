#%%
import os
import glob
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SETUP DIRECTORIES & FILES ---
working_dir = '/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/08-26 All acetylation quantifications/07-25-26 H2A acetylation/Replicate 3'
#05-09-25 acetylation spreads
#05-12-25 H2A acetylation replicate 1
#Replicate 2
os.chdir(working_dir)

# CHANGED: Search for all relevant CSV files
csv_files = glob.glob("MCF10A*bg_corrected.csv")

# Master list to hold data from ALL files
master_results_list = []
cell = 0

# Collects labels for any inside/outside slice that was empty, so we can
# print one clean summary at the end instead of a warning per occurrence.
skipped_log = []


def safe_quantile(data, q, label=""):
    """Return np.quantile(data, q), or NaN (and log it) if data is empty."""
    if len(data) == 0:
        skipped_log.append(label)
        return np.nan
    return np.quantile(data, q)


def safe_ratio(numerator, denominator):
    """Divide numerator/denominator, returning NaN if denominator is 0 or NaN."""
    if denominator is None or np.isnan(denominator) or denominator == 0:
        return np.nan
    return numerator / denominator


# --- 2. LOOP THROUGH EACH CSV FILE ---
for file_path in csv_files:
    cell = cell + 1
    file_name = os.path.basename(file_path)
    # Extracts the file name without the extension (.csv)
    base_name = os.path.splitext(file_name)[0]
    print(f"Processing: {file_name}...")
    
    # Read CSV data
    data = pd.read_csv(file_path, encoding='latin1')
    data = data.dropna(subset=['chromosome'])
    chromosomes = data['chromosome'].unique()

    # Configure grid dimensions
    num_chromosomes = len(chromosomes)
    num_cols = 4  
    num_rows = int(np.ceil(num_chromosomes / num_cols))

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 4 * num_rows))

    # FIXED: plt.subplots only returns a bare Axes (not an array) when
    # nrows == 1 AND ncols == 1. Since num_cols is fixed at 4, axes is
    # always array-like here, so np.atleast_1d + flatten handles every
    # grid shape correctly (including any future 1x1 case) without the
    # old num_chromosomes == 1 special-case, which double-wrapped the
    # array and broke indexing.
    axes = np.atleast_1d(axes).flatten()

    global_handles, global_labels = [], []
    threshold = 0.3

    # --- 3. LOOP THROUGH CHROMOSOMES IN THIS FILE ---
    for idx, i in enumerate(chromosomes):
        ax = axes[idx]  
        chr_df= data[(data['chromosome'] == i)]

        if chr_df.empty:
            ax.set_title(f"ID {i}: Missing Data")
            ax.axis('off')  
            continue

        # --- FIND MAX PEAK AND CUTOFF ---
        max_value = chr_df['TRITC'].max()
        cutoff_value = max_value * threshold

        # --- SEPARATE INSIDE VS OUTSIDE DATA ---
        inside_mask = chr_df['TRITC'] >= cutoff_value
        inside_df = chr_df[inside_mask]
        outside_df = chr_df[~inside_mask]

        # --- CALCULATE MULTIPLE CENTRAL TENDENCIES AND CHROMOSOME LENGTH ---
        mean_inside = inside_df['Cy5_corrected'].mean()
        mean_outside = outside_df['Cy5_corrected'].mean()
        ratio_mean = mean_outside / mean_inside if mean_inside != 0 else 0
        
        median_inside = inside_df['Cy5_corrected'].median()
        median_outside = outside_df['Cy5_corrected'].median()
        ratio_median = median_outside / median_inside if median_inside != 0 else 0

        uq75_inside = safe_quantile(inside_df['Cy5_corrected'], 0.75, label=f"{file_name} chr {i} (inside, 75th)")
        uq75_outside = safe_quantile(outside_df['Cy5_corrected'], 0.75, label=f"{file_name} chr {i} (outside, 75th)")
        ratio_uq75 = safe_ratio(uq75_outside, uq75_inside)

        uq80_inside = safe_quantile(inside_df['Cy5_corrected'], 0.8, label=f"{file_name} chr {i} (inside, 80th)")
        uq80_outside = safe_quantile(outside_df['Cy5_corrected'], 0.8, label=f"{file_name} chr {i} (outside, 80th)")
        ratio_uq80 = safe_ratio(uq80_outside, uq80_inside)

        uq90_inside = safe_quantile(inside_df['Cy5_corrected'], 0.90, label=f"{file_name} chr {i} (inside, 90th)")
        uq90_outside = safe_quantile(outside_df['Cy5_corrected'], 0.90, label=f"{file_name} chr {i} (outside, 90th)")
        ratio_uq90 = safe_ratio(uq90_outside, uq90_inside)

        chr_length = chr_df['Distance_microns'].iloc[-1]

        # --- APPEND TO MASTER LIST ---
        master_results_list.append({
            'Source_File': file_name,
            'cell': cell,
            'Chromosome': i,
            'Chromosome_length': chr_length,
            'Inside_Mean_acH2A': round(mean_inside, 2),
            'Outside_Mean_acH2A': round(mean_outside, 2),
            'Ratio_Mean_Outside_Inside': round(ratio_mean, 4),
            'Inside_Median_acH2A': round(median_inside, 2),
            'Outside_Median_acH2A': round(median_outside, 2),
            'Ratio_Median_Outside_Inside': round(ratio_median, 4),
            'Inside_uq75_acH2A': round(uq75_inside, 2),
            'Outside_uq75_acH2A': round(uq75_outside, 2),
            'Ratio_uq75_Outside_Inside': round(ratio_uq75, 4),
            'Inside_uq80_acH2A': round(uq80_inside, 2),
            'Outside_uq80_acH2A': round(uq80_outside, 2),
            'Ratio_uq80_Outside_Inside': round(ratio_uq80, 4),
            'Inside_uq90_acH2A': round(uq90_inside, 2),
            'Outside_uq90_acH2A': round(uq90_outside, 2),
            'Ratio_uq90_Outside_Inside': round(ratio_uq90, 4)
        })

        # --- PLOT ON TARGET AXIS ---
        sns.lineplot(data=chr_df, x="Distance_microns", y="TRITC", color="orange", label="ACA", ax=ax)
        sns.lineplot(data=chr_df, x="Distance_microns", y="Cy5_corrected", color="magenta", label="acH2A", ax=ax)
        plt.ylim(0, 1500)
        
        if not global_handles and ax.get_legend():
            global_handles, global_labels = ax.get_legend_handles_labels()

        ax.scatter(inside_df['Distance_microns'], inside_df['Cy5_corrected'], color='black', marker='x', s=30, zorder=5)
        ax.set_ylim(0, 1500)
        
        stats_text = (
            f"Mean inside: {round(mean_inside, 2)}\n"
            f"Mean outside: {round(mean_outside, 2)}\n"
            f"Mean Ratio: {round(ratio_mean, 2)}\n"
            f"Median Ratio: {round(ratio_median, 2)}\n"
            f"Upper-q Ratio: {round(ratio_uq75, 2)}"
        )
        ax.text(0.05, 0.5, stats_text, fontsize=8, transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3'))

        ax.set_title(f"Chromosome {round(i)}", fontsize=11)
        ax.set_xlabel("Length (µm)", fontsize=10)
        ax.set_ylabel("Intensity", fontsize=10)
        
        # --- Keep legend ONLY for the very first plot panel (idx == 0) ---
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
        else:
            if ax.get_legend():
                ax.get_legend().remove()

    # --- 4. CLEAN UP EXTRA SUBPLOTS AND SAVE INDIVIDUAL GRAPH ---
    for extra_idx in range(num_chromosomes, len(axes)):
        axes[extra_idx].axis('off')

    fig.suptitle(f"Intensities quantifications around a {round(threshold*100)}% ACA peak ({base_name})", fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 

    # Saves plot named exactly after the source CSV file
    plt.savefig(f"plot_{base_name}.png", dpi=300) 
    plt.close(fig) 

# --- 5: SAVE AGGREGATED DATA TO ONE MASTER FILE ---
if master_results_list:
    master_df = pd.DataFrame(master_results_list)
    cols = ['Source_File'] + [col for col in master_df.columns if col != 'Source_File']
    master_df = master_df[cols]
    
    # Generates a single master Excel file containing all the combined data
    master_df.to_excel("all_data_master_summary.xlsx", index=False)
    print("\nAll files processed! Master data table exported successfully.")
else:
    # CHANGED: Alert error string references CSVs instead of Excel files
    print("\nNo matching CSV files were found.")

# --- 6: SINGLE SUMMARY WARNING FOR ANY SKIPPED (EMPTY) QUANTILE CALCULATIONS ---
if skipped_log:
    warnings.warn(
        f"{len(skipped_log)} inside/outside slice(s) had no data and were set to NaN:\n"
        + "\n".join(skipped_log)
    )