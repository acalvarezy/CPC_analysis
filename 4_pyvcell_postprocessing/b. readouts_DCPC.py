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
    if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/{name_folder}"):
        pass
    else:
        os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/{name_folder}")
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
            model = re.search(r"run([^_]+)", n).group(1)
            DCPC = tmpc.loc[tmpc['Time'] == timepoint, 'bg_corrected'].values[0]

            df.loc[len(df)] = [model, DCPC]

        print(df)
        df.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/plots/{name_plot}_{location[0]}_at_{timepoint}m.xlsx")

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
        
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2/plots/{name_plot}_{location[0]}_at_{timepoint}m.pdf")
        plt.show()

name_folder = "folder"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1_relaxed_test2"
plot_list = [
            "run101", "run7",
"run39",
"run26",
"run16",
"run32",
"run70",
"run11",
"run61",
"run23",
"run81",
"run48",
"run64",
"run78",
"run38",
"run40",
"run44",
"run55",
"run29",
"run36",
"run79",
"run15",
"run93",
"run91",
"run21",
"run59",
"run31",
"run5",
"run18",
"run67",
"run49",
"run57",
"run66",
"run53",
"run90",
"run6",
"run83",
"run63",
"run87",
"run73",
"run72",
"run88",
"run52",
"run51",
"run10",
"run17",
"run77",
"run25",
"run14",
"run96",
"run12",
"run54",
"run68",
"run80",
"run71",
"run8",
"run3",
"run9",
"run45",
"run34",
"run95",
"run24",
"run41",
"run60",
"run89",
"run28",
"run37",
"run1",
"run43",
"run65",
"run35",
"run97",
"run69",
"run33",
"run27",
"run99",
"run94",
"run20",
"run30",
"run13",
"run85",
"run84",
"run47",
"run56",
"run76",
"run22",
"run75",
"run50",
"run42",
"run58",
"run92",
"run19",
"run62",
"run2",
"run74",
"run98",
"run0",
"run86",
"run4",
"run46",
"run82"
                                            ]

location = ["ic", #change region of interest
            "bg"
                ]

plot_across_models('CPC_all', plot_list, in_dir_, location, 5 ,name_plot="07_27_26_relaxed_cv0.1",active= 'all')

