#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 21:40:23 2025
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
in_dir = "/Users/catalinaalvarez/Documents/CPC_plots_2026/deep_dive"
import os

#SIMULATIONS COMPARISON - Individual plotting of chromosome regions (IC or KT or BG) 
def plot_across_models(species, plot_list, in_dir,  name_list = [], location = 'ic',column = "Sum_Active", active = 'active',
                        name = None, name_plot="", name_folder =""):
    print("Plotting across models")
    if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/simulations_comparison/{name_folder}"):
        pass
    else:
        os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/simulations_comparison/{name_folder}")
        print(f"Made folder {name_folder}")
    # plot_list = sorted(plot_list)
    plot_data = pd.DataFrame()
    if len(name_list) == 0:
        name_list = plot_list
    if active == 'all':
        for n, p in zip(name_list,plot_list):
            tmp = pd.read_csv(f"{in_dir}/{p}/data/data_{location}_{species}.csv", header = 0, index_col = None)
            tmp['Time'] = 10*tmp['Time']
            tmp['parameter'] = n
            tmp['all'] = tmp[list(set(tmp.columns).difference({"Time",'parameter'}))].sum(axis = 1)
            plot_data = pd.concat([plot_data,tmp[['parameter','all', 'Time']]], ignore_index=True)
            column = 'all'
            plot_data = pd.concat([plot_data,tmp[['parameter',column, 'Time']]], ignore_index=True)  
                     
    else:
        if active == 'inactive' and column == 'Sum_Active':
            column = 'Sum_Inactive'
        if active == 'active' and column == 'Sum_Inactive':
            column = 'Sum_Active'  
        for p in plot_list:
            tmp = pd.read_csv(f"{in_dir}/{p}/data/data_{active}_{location}_{species}.csv", header = 0, index_col = None)
            tmp['Time'] = 10*tmp['Time']
            tmp['parameter'] = p
            plot_data = pd.concat([plot_data,tmp[['parameter',column, 'Time']]], ignore_index=True)

    fig = plt.figure(figsize = (4,3))
    print(plot_data.loc[plot_data["Time"]==500][column])
    ax = sns.lineplot(x = plot_data['Time'], y= plot_data[column], hue = plot_data['parameter'], palette="magma")
    ax.set_xlim(0,500)
    ax.set_ylim(0,470)

    plt.xlabel("Time (s)")
    if name is not None:
        plt.ylabel(f"{name} (uM)")
        plt.title(f"{name} at {location.upper()}")
    else:
        if column.startswith('Sum'):
            plt.ylabel(f"Total {active} {species} (uM)")
            plt.title(f"Total {active} {species} at {location.upper()}")
        else:
            plt.ylabel(f"{species} (uM)")
            plt.title(f"{species} at {location.upper()}")

#Change legend labels here following simulation order:
    L=ax.legend()
    L.get_texts()[0].set_text(r'SGO1 KO')
    L.get_texts()[1].set_text(r'SGO1 0.1x')
    L.get_texts()[2].set_text(r'SGO1 0.2x')
    L.get_texts()[3].set_text(r'SGO1 0.5x')
    L.get_texts()[4].set_text(r'SGO1 1x')
    L.get_texts()[5].set_text(r'SGO1 2x')
    L.get_texts()[6].set_text(r'SGO1 5x')
    L.get_texts()[7].set_text(r'SGO1 10x')


    sns.move_legend(ax, "best", labelspacing = 0.01, fontsize='7')
    plt.setp(plt.gca().get_legend().get_texts())
    # plt.legend(labelspacing=0.01, fontsize='7')
    plt.tight_layout()
    print("saving fig")
    plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/simulations_comparison/{name_plot}-{species}_loc-{location}.pdf")
    plt.show()
    plt.close()

name_folder = "cata"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/deep_dive"

plot_list = [
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_SGO1_KO",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scandown_0.1x",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scandown_0.2x",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scandown_0.5x",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scanup_2x",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scanup_5x",
            "06_04_26_metacentric_relaxed_MCF10A_chr19_PMP1_preboundSGO1_CPC_SGO1_scanup_10x"


            ]

# toplotsp = ["CPC", "CPCa_total", "pNDC80_total"]

# for x in toplotsp:
plot_across_models("pNDC80_total", plot_list, in_dir_, location='ic',name_plot="06_04_26_relaxed_prebound_SGO1scan",active= 'all')
plot_across_models("pNDC80_total", plot_list, in_dir_, location='kt',name_plot="06_04_26_relaxed_prebound_SGO1scan",active= 'all')
plot_across_models("pNDC80_total", plot_list, in_dir_, location='bg',name_plot="06_04_26_relaxed_prebound_SGO1scan",active= 'all')
plot_across_models("pNDC80_total", plot_list, in_dir_, location='ch',name_plot="06_04_26_relaxed_prebound_SGO1scan",active= 'all')


