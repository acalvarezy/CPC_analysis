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

#SIMULATIONS READOUTS COMPARISON - eDCPC
def plot_across_models(species, plot_list, in_dir, location, timepoint, name_list = [], column = "Sum_Active", active = 'active',
                        name = None, name_plot="", name_folder =""):
    print("Plotting across models")
    
    #eDCPC
    if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/eDCPC/{name_folder}"):
        pass
    else:
        os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/eDCPC/{name_folder}")
        print(f"Made folder {name_folder}")
    if len(name_list) == 0:
        name_list = plot_list 
    if active == 'all':
        tag = 0
        df = pd.DataFrame(columns=["state", "percentage", "eDCPC"])
        for n, p in zip(name_list,plot_list):
            tmpc = pd.DataFrame()
            for z in location:
                    if z == 'kt':
                        tmpkt = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmpkt['Time'] = 10*tmpkt['Time']
                        tmpkt['parameter'] = n
                        tmpkt['all'] = tmpkt[list(set(tmpkt.columns).difference({"Time",'parameter'}))].sum(axis = 1)

                    if z == 'ic':
                        tmpic = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmpic['parameter'] = n
                        tmpic['all'] = tmpic[list(set(tmpic.columns).difference({"Time",'parameter'}))].sum(axis = 1)

                    if z == 'bg':
                        tmpbg = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmpbg['parameter'] = n
                        tmpbg['all'] = tmpbg[list(set(tmpbg.columns).difference({"Time",'parameter'}))].sum(axis = 1)    
                                     
                    else:
                        tmpch = pd.read_csv(f"{in_dir}/{p}/data/data_{z}_{species}.csv", header = 0, index_col = None)
                        tmpch['parameter'] = n
                        tmpch['all'] = tmpch[list(set(tmpch.columns).difference({"Time",'parameter'}))].sum(axis = 1)

             
            tmpc['Time'] = tmpkt['Time']
            tmpc['parameter'] = tmpkt['parameter']
            tmpc['ecDCPC'] = (tmpic['all'] - tmpkt['all'] - tmpch['all'] + tmpbg['all']) / tmpbg['all']
            
          ####Here


            state = re.search(r"metacentric_([^_]+)_MCF", n).group(1)
            percentage = int(re.search(r"arms_([^_]+)P", n).group(1)) #TO EDIT depending on the simulation scan
            eDCPC = tmpc.loc[tmpc['Time'] == timepoint, 'ecDCPC'].values[0]

            df.loc[len(df)] = [state, percentage, eDCPC]

        print(df)
        print(len(df))
        df.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/ecDCPC/{name_plot}_{location[0]}_at_{timepoint}s.xlsx")

        fig = plt.figure(figsize = (5,4.5))
        sns.lineplot(data=df, x="percentage", y="ecDCPC", hue="state", marker="o", markersize=3, palette="magma", linewidth=3)
        plt.ylabel(fr'ecDCPC', fontsize=12)
        plt.xlabel("acH2A at the arms (%)", fontsize=12)
        plt.legend(title="Chromosome state")
        plt.title(fr"time = ({timepoint} s)")
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/ecDCPC/{name_plot}_{location[0]}_at_{timepoint}s.pdf")
        

        #DfcCPC
        if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DfcCPC/{name_folder}"):
                pass
        else:
            os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DfcCPC/{name_folder}")
            print(f"Made folder {name_folder}")
        df2 = pd.DataFrame(columns=["state", "percentage", "DfcCPC"])
        for i in range(0, len(df), 2): 
            state = "relaxed - tensed"
            percentage =  df['percentage'].iloc[i]
            DfcCPC =  df['fcCPC'].iloc[i] - df['fcCPC'].iloc[i+1]
            df2.loc[len(df2)] = [state, percentage, DfcCPC]

        print(df2)
        df2.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DfcCPC/{name_plot}_{location[0]}_at_{timepoint}s.xlsx")

        fig = plt.figure(figsize = (5,4.5))
        sns.lineplot(data=df2, x="percentage", y="DfcCPC", marker="o", markersize=3, palette="magma", linewidth=3)
        plt.ylabel(fr'$\Delta fcCPC$', fontsize=12)
        plt.xlabel("acH2A at the arms (%)", fontsize=12)
        if location[0] == "ic":
            plt.title(fr"$\Delta fcCPC$ at inner centromere ({timepoint} s)")
        else: 
            plt.title(fr"$\Delta fcCPC$ at kinetochores ({timepoint} s)")    
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/DfcCPC/{name_plot}_{location[0]}_at_{timepoint}s.pdf")


        #fcfcCPC
        if os.path.isdir(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/fcfcDCPC/{name_folder}"):
                pass
        else:
            os.makedirs(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/fcfcDCPC/{name_folder}")
            print(f"Made folder {name_folder}")

        df3 = pd.DataFrame(columns=["state", "percentage", "fcfcCPC"])
        for i in range(0, len(df), 2): 
            state = "relaxed - tensed"
            percentage =  df['percentage'].iloc[i]
            fcfcCPC =  df['fcCPC'].iloc[i] / df['fcCPC'].iloc[i+1]
            df3.loc[len(df3)] = [state, percentage, fcfcCPC]

        print(df3)
        df3.to_excel(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/fcfcCPC/{name_plot}_{location[0]}_at_{timepoint}s.xlsx")

        fig = plt.figure(figsize = (5.5,4.5))
        sns.lineplot(data=df3, x="percentage", y="fcfcCPC", marker="o", markersize=3, palette="magma", linewidth=3)
        plt.ylabel(fr'fcfcCPC', fontsize=12)
        plt.xlabel("acH2A at the arms (%)", fontsize=12)
        # plt.ylim(1.7,2)
        if location[0] == "ic":
            plt.title(fr"fcfcCPC at inner centromere ({timepoint} s)")
        else: 
            plt.title(fr"fcfcCPC at kinetochores ({timepoint} s)")    
        plt.savefig(f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CPC_readouts/fcfcCPC/{name_plot}_{location[0]}_at_{timepoint}s.pdf")


    else: 
        print("Check needed species or complete this code")


    
name_folder = "folder"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026"
plot_list = [
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_0P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_0P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_5P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_5P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_10P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_10P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_15P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_15P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_20P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_20P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_25P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_25P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_30P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_30P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_35P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_35P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_40P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_40P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_45P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_45P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_50P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_50P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_55P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_55P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_60P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_60P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_65P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_65P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_70P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_70P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_75P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_75P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_80P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_80P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_85P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_85P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_90P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_90P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_95P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_95P",
            "05_20_26_metacentric_relaxed_MCF10A_chr19_PMP1_acH2A_arms_100P",
            "05_20_26_metacentric_tensed_MCF10A_chr19_PMP1_acH2A_arms_100P"
                                            ]

location = ["kt",  #change region of interest
            "bg"
                ]

plot_across_models('CPC', plot_list, in_dir_, location, 200 ,name_plot="05_20_26_metacentric_MCF10A_chr19_PMP1",active= 'all')

