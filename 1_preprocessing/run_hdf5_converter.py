#%%
import os
import numpy as np
import subprocess

#Change working directory
new_directory_path = "/Users/catalinaalvarez/Documents/GitHub/CPC_analysis/1_preprocessing"
os.chdir(new_directory_path)

#Update the simulation data
models = np.array([
    "006_13_26 CPC_metacentric_relaxed_MCF10A_chr19_PMP1_fortransition"
	])


simulations = np.array([
	"06_14_26_metacentric_relaxed_MCF10A_chr19_PMP1_noacetylation"
        ])
 
simID = np.array([ 
	"SimID_317052736_0__exported"
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

