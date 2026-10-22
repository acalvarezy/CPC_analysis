#%%
import os
import glob
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

# --- 1. SETUP DIRECTORIES & FILES ---
working_dir = '/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/08-26 All acetylation quantifications/07-25-26 H2A acetylation/Replicate 3'
#05-09-25 acetylation spreads
#05-12-25 H2A acetylation replicate 1
#Replicate 2
os.chdir(working_dir)

# Search for all relevant CSV files and for the background data
csv_files = [
    f for f in Path(working_dir).glob('MCF10A*(merged).csv') 
    if '_bg' not in f.name
]
print(csv_files)

bg_measurements = pd.read_excel("file_level_bg_summary.xlsx")
print(bg_measurements)

# Master list to hold data from ALL files
master_results_list = []
cell_number = 0

# --- 2. LOOP THROUGH EACH CSV FILE ---
for file_path in csv_files:
    cell_number = cell_number + 1
    file_name = os.path.basename(file_path)
    # Extracts the file name without the extension (.csv)
    base_name = os.path.splitext(file_name)[0]
    print(f"Processing: {file_name}...")
    
    # Read CSV data
    data = pd.read_csv(file_path, encoding='latin1')
    data = data.dropna(subset=['Parent ID'])
    chromosomes = data['Parent ID'].unique()

    # --- 3. LOOP THROUGH CHROMOSOMES IN THIS FILE ---
    all_corrected_data = []
    for i in chromosomes:
        mean_file = bg_measurements.loc[bg_measurements["Source_File"] == base_name, ["Mean_of_Chromosome_Means"]].values[0]

        chr_raw = data[(data['Parent ID'] == i) & (data['Channel'].isin(['DAPI', 'TRITC', 'Cy5']))]
        chr_df = chr_raw.pivot_table(index='Distance (µm)', columns='Channel', values='Intensity', aggfunc='mean').reset_index()
        chr_df = chr_df.dropna()  

        # 1. Catch completely empty dataframes early
        if chr_df.empty: 
            print(f"ID {i}: Missing Data") 
            continue 
        
        # 2. Check if 'TRITC' column actually exists before doing math
        if 'TRITC' not in chr_df.columns:
            print(f"ID {i}: Missing TRITC Channel")
            continue  # Skips to the next chromosome so the script doesn't crash

        # Complete the table associated to chromosome i and substract background signal from Cy5 values
        chr_df.insert(0,'chromosome', i)
        chr_df['Cy5_corrected'] = chr_df['Cy5'] - mean_file
        chr_df = chr_df.rename(columns={"Distance (µm)": "Distance_microns"})

        #Append the current DataFrame to your list
        all_corrected_data.append(chr_df)


# 3. Combine all collected DataFrames and export to CSV (outside the loop)
    if all_corrected_data:
        combined_df = pd.concat(all_corrected_data, ignore_index=True)
        combined_df.to_csv(f'{base_name}_bg_corrected.csv', index=False)
        print("Corrected csv files successfully generated'")
    else:
        print("No data was collected to save.")



# %%
