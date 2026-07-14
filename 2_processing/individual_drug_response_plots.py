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
        df = pd.DataFrame(columns=["state", "percentage", "DCPC"])
        i = 0
        for n, p in zip(name_list,plot_list):
            tmpc = pd.DataFrame()
            for z in location:
                    if z in ['kt', 'ic']:
                        tmp1 = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmp1['Time'] = tmp1['Time']
                        tmp1['parameter'] = n
                        tmp1['all'] = tmp1[list(set(tmp1.columns).difference({"Time",'parameter'}))].sum(axis = 1)
                                     
                    else:
                        tmp2 = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmp2['all'] = tmp2[list(set(tmp2.columns).difference({"Time",'parameter'}))].sum(axis = 1)
                            
            tmpc['Time'] = tmp1['Time']
            tmpc['parameter'] = tmp1['parameter']
            tmpc['bg_corrected'] = tmp1['all'] - tmp2['all']
            state = haplotype[i]
            percentage = inhibition[i] #TO EDIT depending on the simulation scan

            DCPC = tmpc.loc[tmpc['Time'] == timepoint, 'bg_corrected'].values[0]

            df.loc[len(df)] = [state, percentage, DCPC]
            i = i + 1

        print(df)
        df.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DCPC/{name_plot}_{location[0]}_at_{timepoint}s.xlsx")

        fig = plt.figure(figsize = (6,4.5))
        sns.lineplot(data=df, x="percentage", y="DCPC", hue="state", marker="o", markersize=3, palette="magma", linewidth=3)
        plt.ylabel(fr'Total CPC ($\mu$M)', fontsize=12)
        plt.xlabel("SGO1 concentration (%)", fontsize=12)
        plt.legend(title="Chromosome state")
        # plt.gca().invert_yaxis()
        if location[0] == "ic":
            plt.title(fr"$\Delta CPC$ at inner centromere ({timepoint*24/(2*60)} )")
        else: 
            plt.title(fr"$\Delta CPC$ at kinetochores ({timepoint*24/(2*60)} m)")    
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DCPC/{name_plot}_{location[0]}_at_{timepoint}s.pdf")


    else: 
        print("Check needed species or complete this code")


name_folder = "folder"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/deep_dive"
plot_list = [
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_KO",
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_scan_0.1x",
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_scan_0.2x",
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_scan_0.5x",
            "06_13_26_metacentric_relaxed_MCF10A_chr19_PMP1",
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_scan_2x",
            "06_15_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_scan_5x"

        ]
            

haplotype = [
          "Relaxed",
          "Relaxed",
          "Relaxed",
          "Relaxed",
          "Relaxed",
          "Relaxed",
          "Relaxed"

        
         ]

inhibition = [
            0,
            0.1,
            0.2,
            0.5,
            1,
            200,
            500
              
              ]
                                        

location = ["ic", #change region of interest
            "bg"
                ]

plot_across_models('CPC', plot_list, in_dir_, location, 25 ,name_plot="06_26_26_drugresponse_SGO1",active= 'all')

