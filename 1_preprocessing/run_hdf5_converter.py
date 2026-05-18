#%%

import os
import numpy as np
import subprocess

#Change working directory
new_directory_path = "/Users/catalinaalvarez/Documents/GitHub/CPC_analysis/1_preprocessing"
os.chdir(new_directory_path)

#Update the simulation data
models = np.array([
    "005_08_00 CPC_metacentric_tensed_MCF10A_chr19_PMP1"
	])


simulations = np.array([
	 "05_08_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_75P"
        ])
 
simID = np.array([ 
	"SimID_313182712_10__exported"
        ])

for i in range(len(models)):
	subprocess.run([
		"python",
		"hdf5_converter.py",
        	f"{simID[i]}.hdf5",
        	"/Users/catalinaalvarez/Documents/CPC_data_2026",
        	models[i],
        	simulations[i]
	])  

