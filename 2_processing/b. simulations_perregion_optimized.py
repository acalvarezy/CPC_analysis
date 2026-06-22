#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_across_models(
    species,
    plot_list,
    in_dir,
    name_list=[],
    location="ic",
    column="Sum_Active",
    active="active",
    name=None,
    name_plot="",
    name_folder="",
    custom_palette=None,
):  # Default is set to None
    print(f"Plotting across models for {location.upper()}")

    out_dir = f"/Users/catalinaalvarez/Documents/CPC_plots_2026/simulations_comparison/{name_folder}"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    plot_data = pd.DataFrame()

    if len(name_list) == 0:
        name_list = plot_list

    if active == "all":
        column = "all"
        for n, p in zip(name_list, plot_list):
            file_path = f"{in_dir}/{p}/data/data_{location}_{species}.csv"
            if not os.path.exists(file_path):
                continue

            tmp = pd.read_csv(file_path, header=0, index_col=None)
            tmp["Time"] = tmp["Time"]*(0.5*24/60)
            tmp["parameter"] = n

            data_cols = list(
                set(tmp.columns).difference({"Time", "parameter", "Unnamed: 0"})
            )
            tmp["all"] = tmp[data_cols].sum(axis=1)

            plot_data = pd.concat(
                [plot_data, tmp[["parameter", "all", "Time"]]],
                ignore_index=True,
            )
    else:
        if active == "inactive" and column == "Sum_Active":
            column = "Sum_Inactive"
        if active == "active" and column == "Sum_Inactive":
            column = "Sum_Active"

        for n, p in zip(name_list, plot_list):
            file_path = (
                f"{in_dir}/{p}/data/data_{active}_{location}_{species}.csv"
            )
            if not os.path.exists(file_path):
                continue

            tmp = pd.read_csv(file_path, header=0, index_col=None)
            tmp["Time"] = 10 * tmp["Time"]
            tmp["parameter"] = n
            plot_data = pd.concat(
                [plot_data, tmp[["parameter", column, "Time"]]],
                ignore_index=True,
            )

    if plot_data.empty:
        return

    fig = plt.figure(figsize=(4, 3))

    # FALLBACK LOGIC
    # If custom_palette is provided, use it. Otherwise, fall back to "magma".
    chosen_palette = custom_palette if custom_palette is not None else "magma"

    ax = sns.lineplot(
        data=plot_data,
        x="Time",
        y=column,
        hue="parameter",
        palette=chosen_palette,  # Pass the resolved palette choice here
    )

    # plt.xlabel("Time (s)")
    
    if species == "pNDC80_total":
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 470)
        plt.xlabel("Time (m)")
    else:
        if species == "CPCa_total":
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 16)
            plt.xlabel("Time (s)")
        else: 
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 25)
            plt.xlabel("Time (m)")

    if name is not None:
        plt.ylabel(f"{name} (uM)")
        plt.title(f"{name} at {location.upper()}")
    else:
        if column.startswith("Sum"):
            plt.ylabel(f"Total {active} {species} (uM)")
            plt.title(f"Total {active} {species} at {location.upper()}")
        else:
            plt.ylabel(f"{species} (uM)")
            plt.title(f"{species} at {location.upper()}")

    L = ax.legend()
    legend_texts = L.get_texts()
    for i, text_obj in enumerate(legend_texts):
        if i < len(name_list):
            text_obj.set_text(name_list[i])

    sns.move_legend(ax, "best", labelspacing=0.01, fontsize="7")
    plt.tight_layout()

    save_path = f"/Users/catalinaalvarez/Documents/CPC_plots_2026/simulations_comparison/{name_plot}-{species}_loc-{location}.pdf"
    plt.savefig(save_path)
    plt.show()
    plt.close()
    	
# Simulation setup
name_folder = "cata"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/deep_dive"

plot_list = [
    "06_13_26_metacentric_relaxed_MCF10A_chr19_PMP1",
    "06_13_26_metacentric_transition_tensed_MCF10A_chr19_PMP1_t_0",
    "06_14_26_metacentric_relaxed_MCF10A_chr19_PMP1_noacetylation"

    

]

clean_names = [
    r"Relaxed state",
    r"Tensed state",
    r"No acetylation"

    
    # # r"SGO1 50%",
    # fr"SGO1 25% + 50% PLK1 inh",
    # fr"SGO1 25% + 70% PLK1 inh",
    # fr"SGO1 25% + 90% PLK1 inh",
    # fr"SGO1 25% + 97% PLK1 inh",
    # fr"SGO1 25% + 99% PLK1 inh",
    # fr"SGO1 25% + 100% PLK1 inh"
   
]

# 🎨 CUSTOM GRADIENT PALETTE DEFINITION
# Maps clean labels directly to specific hex colors.
# Scan-down gets a blue gradient (darker = lower concentration).
# Scan-up gets a red gradient (darker = higher concentration).
sgo1_palette = {
    r"SGO1 KO": "#08306b",  # Extremely dark blue
    r"SGO1 0.1x": "#2171b5",  # Medium dark blue
    r"SGO1 0.2x": "#6baed6",  # Medium blue
    r"SGO1 0.5x": "#bdd7e7",  # Light blue
    r"SGO1 1x": "#737373",  # Reference Model -> Slate Gray
    r"SGO1 2x": "#fee0d2",  # Light red / coral
    r"SGO1 5x": "#ef3b2c",  # Medium bright red
    r"SGO1 10x": "#67000d",  # Extremely dark crimson red

}

# Executing plots across locations
locations = ["ic", "kt", "bg", "ch"]
for loc in locations:
    plot_across_models(
        species="CPC",
        plot_list=plot_list,
        in_dir=in_dir_,
        name_list=clean_names,
        location=loc,
        name_plot="06_21_26_relaxed_tensed_noacH2A",
        active="all",
        name_folder=name_folder,
        custom_palette="magma",  # Injected custom palette
    )