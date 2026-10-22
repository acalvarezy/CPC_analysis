#%%
import os
import glob
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
csv_files = glob.glob("MCF10A*bg.csv")

# Master list to hold data from ALL files
master_results_list = []

# --- 2. LOOP THROUGH EACH CSV FILE ---
for file_path in csv_files:
    file_name = os.path.basename(file_path)
    # Extracts the file name without _bg and the extension (.csv)
    base_name = file_name.rsplit(' bg.csv', 1)[0]
    print(f"Processing: {file_name}...")
    
    # Read CSV data
    data = pd.read_csv(file_path, encoding='latin1')
    data = data.dropna(subset=['Parent ID'])

    chromosomes = data['Parent ID'].unique()

    # Configure grid dimensions
    num_chromosomes = len(chromosomes)
    num_cols = 4  
    num_rows = int(np.ceil(num_chromosomes / num_cols))

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 4 * num_rows))
    
    if num_chromosomes == 1:
        axes = np.array([axes])
    else:
        axes = axes.flatten()  

    global_handles, global_labels = [], []

    # --- 3. LOOP THROUGH CHROMOSOMES IN THIS FILE ---
    for idx, i in enumerate(chromosomes):
        ax = axes[idx]  
        
        chr_raw = data[(data['Parent ID'] == i) & (data['Channel'].isin(['TRITC', 'Cy5']))]
        chr_df = chr_raw.pivot_table(index='Distance (µm)', columns='Channel', values='Intensity', aggfunc='mean').reset_index()
        chr_df = chr_df.dropna()  

        if chr_df.empty:
            ax.set_title(f"ID {i}: Missing Data")
            ax.axis('off')  
            continue

        # --- CALCULATE MULTIPLE CENTRAL TENDENCIES ---
        mean = chr_df['Cy5'].mean()
        median = chr_df['Cy5'].median()
        quartile = np.quantile(chr_df['Cy5'], 0.75)

        # --- PLOT ON TARGET AXIS ---
        sns.lineplot(data=chr_df, x="Distance (µm)", y="TRITC", color="orange", label="ACA", ax=ax)
        sns.lineplot(data=chr_df, x="Distance (µm)", y="Cy5", color="magenta", label="acH2A", ax=ax)
        
        if not global_handles and ax.get_legend():
            global_handles, global_labels = ax.get_legend_handles_labels()
        
        stats_text = (
            f"Mean acH2A-K118: {round(mean, 2)}\n"
            f"Median acH2A-K118: {round(median, 2)}\n"
            f"Upper-quartile acH2A-K118: {round(quartile, 2)}"
        )
        ax.text(0.05, 0.3, stats_text, fontsize=8, transform=ax.transAxes,
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


        # --- APPEND TO MASTER LIST ---
        master_results_list.append({
            'Source_File': base_name,
            'Chromosome': i,
            'Mean': round(mean, 2),
            'Median': round(median, 2),
            'Upper-quartile': round(quartile, 2),

                            })            

    # --- 4. CLEAN UP EXTRA SUBPLOTS AND SAVE INDIVIDUAL GRAPH ---
    for extra_idx in range(num_chromosomes, len(axes)):
        axes[extra_idx].axis('off')

    fig.suptitle(f"Background intensities along the chromosome length ({base_name})", fontsize=14, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 

    # Saves plot named exactly after the source CSV file
    plt.savefig(f"plot_{base_name}_bg.png", dpi=300) 
    plt.close(fig) 

# --- 5: AGGREGATE PER FILE & SAVE TO EXCEL ---
print(master_results_list)

if master_results_list:
    # Convert list to data frame
    chr_df = pd.DataFrame(master_results_list)
    
    # Group by file name and average the chromosome metrics
    file_summary_df = chr_df.groupby('Source_File', as_index=False).agg({
        'Mean': 'mean',
        'Median': 'mean',
        'Upper-quartile': 'mean'
    })
    
    # Clean up column names and round the final outputs
    file_summary_df = file_summary_df.rename(columns={
        'Mean': 'Mean_of_Chromosome_Means',
        'Median': 'Mean_of_Chromosome_Medians',
        'Upper-quartile': 'Mean_of_Chromosome_Upper-quartiles',
    })
    file_summary_df['Mean_of_Chromosome_Means'] = file_summary_df['Mean_of_Chromosome_Means'].round(2)
    file_summary_df['Mean_of_Chromosome_Medians'] = file_summary_df['Mean_of_Chromosome_Medians'].round(2)
    file_summary_df['Mean_of_Chromosome_Upper-quartiles'] = file_summary_df['Mean_of_Chromosome_Upper-quartiles'].round(2)
    
    # Generates a single master Excel file grouped per file
    file_summary_df.to_excel("file_level_bg_summary.xlsx", index=False)
    print("\nAll files processed! Per-file background summary exported successfully.")
else:
    print("\nNo matching CSV files were found or files contained no data.")





