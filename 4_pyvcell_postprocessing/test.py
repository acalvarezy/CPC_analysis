"""
Add the cpc_ic column from the second file into ensemble_parameters,
matching rows by run number.

File 1 (ensemble_parameters.xls): has a 'run' column with integers (1, 2, 3, ...)
File 2 (..._all_loc-ic.xlsx): has a 'model' column with values like 'run13', 'run37',
    plus a 'Relaxed state' row that has no corresponding run number.

For each row in file 1, we look up the matching 'runN' entry in file 2 and pull
its cpc_ic value into a new column.
"""

import re
import pandas as pd

ENSEMBLE_FILE = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/ensemble_parameters_combined.xlsx"  
ICVALUES_FILE = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/plots/07_27_26_relaxed_cv0.1_ic_at_5m.xlsx"
OUTPUT_FILE = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/ensemble_parameters2DCPC_ic.xlsx"

# --- Load both files ---
df_ensemble = pd.read_excel(ENSEMBLE_FILE)
df_ic = pd.read_excel(ICVALUES_FILE)

# --- Build a run-number -> cpc_ic lookup from file 2 ---
# 'model' values look like 'run13' -> run number 13. Non-matching rows (e.g. 'Relaxed state') are skipped.
def extract_run_number(model_value): 
    match = re.fullmatch(r"run(\d+)", str(model_value).strip())
    return int(match.group(1)) if match else None

df_ic["run_number"] = df_ic["model"].apply(extract_run_number)
lookup = df_ic.dropna(subset=["run_number"]).set_index("run_number")["DCPC"]

unmatched_ic_rows = df_ic[df_ic["run_number"].isna()]["model"].tolist()
if unmatched_ic_rows:
    print(f"Note: rows in file 2 with no run number (skipped): {unmatched_ic_rows}")

# --- Map cpc_ic onto the ensemble dataframe by 'run' number ---
df_ensemble["DCPC"] = df_ensemble["run"].map(lookup)

missing = df_ensemble[df_ensemble["DCPC"].isna()]["run"].tolist()
if missing:
    print(f"Warning: no cpc_ic match found for run(s): {missing}")
else:
    print("All rows matched successfully.")

# --- Save result, keeping every original column plus the new one ---
df_ensemble["DCPC_nomr"] = df_ensemble["DCPC"]/df_ensemble["CPC_copiespc"]
df_ensemble.to_excel(OUTPUT_FILE, index=False)
print(f"Saved: {OUTPUT_FILE}")
print(f"Final shape: {df_ensemble.shape}")