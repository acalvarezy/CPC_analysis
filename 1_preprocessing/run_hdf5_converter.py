#%%

import os
import numpy as np
import subprocess

#Change working directory
new_directory_path = "/Users/catalinaalvarez/Documents/GitHub/CPC_analysis/1_preprocessing"
os.chdir(new_directory_path)

#Update the simulation data
models = np.array([
    "03_31_26_metacentric_realaxed_MCF10A_chr19_PMP1"
	])


simulations = np.array([
	"03_31_26_metacentric_relaxed_MCF10A_chr19_PMP1_kppsall=0.01s"
        ])
 
simID = np.array([ 
	"SimID_309083866_0__exported"
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

