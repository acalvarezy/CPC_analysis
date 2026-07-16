#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 2026
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re

#SIMULATIONS READOUTS COMPARISON - DCPC
def plot_across_models(species, plot_list, in_dir, location, timepoint, name_list = [], column = "Sum_Active", active = 'active',
                        name = None, name_plot="", name_folder =""):
    print("Plotting across models")

    #DCPC
    if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DCPC/{name_folder}"):
        pass
    else:
        os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DCPC/{name_folder}")
        print(f"Made folder {name_folder}")

    if len(name_list) == 0:
        name_list = plot_list 
    if active == 'all':
        tag = 0
        df = pd.DataFrame(columns=["model", "DCPC"])
        for n, p in zip(name_list,plot_list):
            tmpc = pd.DataFrame()
            for z in location:
                    if z in ['kt', 'ic', 'ch']:
                        tmp1 = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmp1['Time'] = 0.5*tmp1['Time']*24/60
                        tmp1['parameter'] = n
                        tmp1['all'] = tmp1[list(set(tmp1.columns).difference({"Time",'parameter'}))].sum(axis = 1)
                                     
                    else:
                        tmp2 = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmp2['all'] = tmp2[list(set(tmp2.columns).difference({"Time",'parameter'}))].sum(axis = 1)
                            
            tmpc['Time'] = tmp1['Time']
            tmpc['parameter'] = tmp1['parameter']
            tmpc['bg_corrected'] = tmp1['all'] - tmp2['all']
            model = re.search(r"ensemble_([^_]+)", n).group(1)
            DCPC = tmpc.loc[tmpc['Time'] == timepoint, 'bg_corrected'].values[0]

            df.loc[len(df)] = [model, DCPC]

        print(df)
        df.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1/plots/{name_plot}_{location[0]}_at_{timepoint}m.xlsx")

        fig = plt.figure(figsize = (15,7))
        sns.lineplot(data=df, x="model", y="DCPC", markersize=3, palette="magma", linewidth=3)
        plt.ylabel(fr'$\Delta CPC$ [$\mu$M]', fontsize=12)
        plt.xlabel("Model", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=7)
        # plt.tight_layout()

        if location[0] == "ic":
            plt.title(fr"$\Delta CPC$ at inner centromere ({timepoint} m)")

        elif location[0] == "ch":
            plt.title(fr"$\Delta CPC$ at cohesin stripe ({timepoint} m)")
        else: 
            plt.title(fr"$\Delta CPC$ at kinetochores ({timepoint} m)")    
        
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1/plots/{name_plot}_{location[0]}_at_{timepoint}m.pdf")
        plt.show()

name_folder = "folder"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1"
plot_list = [
            "ensemble_run101", "ensemble_run13", "ensemble_run37", 
    "ensemble_run32", "ensemble_run48", "ensemble_run76", "ensemble_run27", "ensemble_run81", 
    "ensemble_run57", "ensemble_run20", "ensemble_run59", "ensemble_run87", "ensemble_run23", 
    "ensemble_run53", "ensemble_run98", "ensemble_run73", "ensemble_run21", "ensemble_run29", 
    "ensemble_run95", "ensemble_run4", "ensemble_run24", "ensemble_run93", "ensemble_run85", 
    "ensemble_run40", "ensemble_run30", "ensemble_run60", "ensemble_run3", "ensemble_run77", 
    "ensemble_run100", "ensemble_run74", "ensemble_run34", "ensemble_run92", "ensemble_run19", 
    "ensemble_run96", "ensemble_run82", "ensemble_run12", "ensemble_run41", "ensemble_run83", 
    "ensemble_run84", "ensemble_run63", "ensemble_run55", "ensemble_run45", "ensemble_run46", 
    "ensemble_run61", "ensemble_run43", "ensemble_run36", "ensemble_run89", "ensemble_run8", 
    "ensemble_run65", "ensemble_run64", "ensemble_run79", "ensemble_run2", "ensemble_run1", 
    "ensemble_run50", "ensemble_run70", "ensemble_run18", "ensemble_run5", "ensemble_run44", 
    "ensemble_run90", "ensemble_run66", "ensemble_run97", "ensemble_run99", "ensemble_run16", 
    "ensemble_run10", "ensemble_run38", "ensemble_run15", "ensemble_run62", "ensemble_run51", 
    "ensemble_run78", "ensemble_run52", "ensemble_run56", "ensemble_run35", "ensemble_run54", 
    "ensemble_run17", "ensemble_run9", "ensemble_run31", "ensemble_run88", "ensemble_run86", 
    "ensemble_run49", "ensemble_run47", "ensemble_run14", "ensemble_run72", "ensemble_run22", 
    "ensemble_run28", "ensemble_run42", "ensemble_run25", "ensemble_run69", "ensemble_run58", 
    "ensemble_run75"
                                            ]

location = ["ch", #change region of interest
            "bg"
                ]

plot_across_models('CPC_all', plot_list, in_dir_, location, 5 ,name_plot="07_15_26_relaxed_cv0.1",active= 'all')

