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
):
    print(f"Plotting across models for {location.upper()}")
    
    out_dir = f"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1/{name_folder}"
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
            tmp["Time"] = tmp["Time"] * (0.5 * 24 / 60)
            tmp["parameter"] = n
            
            data_cols = list(set(tmp.columns).difference({"Time", "parameter", "Unnamed: 0"}))
            tmp["all"] = tmp[data_cols].sum(axis=1)
            plot_data = pd.concat([plot_data, tmp[["parameter", "all", "Time"]]], ignore_index=True)
    else:
        if active == "inactive" and column == "Sum_Active":
            column = "Sum_Inactive"
        if active == "active" and column == "Sum_Inactive":
            column = "Sum_Active"
            
        for n, p in zip(name_list, plot_list):
            file_path = f"{in_dir}/{p}/data/data_{active}_{location}_{species}.csv"
            if not os.path.exists(file_path):
                continue
            tmp = pd.read_csv(file_path, header=0, index_col=None)
            tmp["Time"] = 10 * tmp["Time"]
            tmp["parameter"] = n
            plot_data = pd.concat([plot_data, tmp[["parameter", column, "Time"]]], ignore_index=True)

    if plot_data.empty:
        print(f"No data found for {location.upper()} - skipping plot.")
        return
    
    #Data processing for parameters analysis
    sub = plot_data[plot_data['Time'] == 5.0][['parameter', 'all']].rename(
    columns={'parameter': 'model', 'all': 'cpc_ic'})
    sub = sub.reset_index(drop=True)
    
    sub.to_excel(f"{out_dir}/{name_plot}-{species}_loc-{location}.xlsx", index=False)

    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)

    # --- PALETTE LOGIC ---
    unique_params = plot_data["parameter"].unique()
    num_lines = len(unique_params)
    base_palette_name = custom_palette if custom_palette is not None else "magma"

    if isinstance(base_palette_name, dict):
        chosen_palette = base_palette_name.copy()
    else:
        color_list = sns.color_palette(base_palette_name, num_lines)
        chosen_palette = {param: color_list[i] for i, param in enumerate(unique_params)}

    if len(unique_params) > 0:
        first_category = unique_params[0]
        chosen_palette[first_category] = "black"

    # Lineplot execution (legend=False removes the massive legend container)
    sns.lineplot(
        data=plot_data,
        x="Time",
        y=column,
        hue="parameter",
        palette=chosen_palette,
        linewidth=0.5,
        ax=ax,
        legend=False,
    )

    # Dynamic Axes Formatting
    if species == "pNDC80_total":
        max_x = 20
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, 470)
        plt.xlabel("Time (m)")
    elif species == "CPC_all":
        max_x = 20
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, 27)
        plt.xlabel("Time (s)")
    else:
        max_x = 10
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, 25)
        plt.xlabel("Time (m)")

    # --- INLINE TRACE LABELS LOGIC ---
    # Loop through each parameter trace to inject text inside the axis boundaries
    for param in unique_params:
        trace_data = plot_data[plot_data["parameter"] == param]
        if trace_data.empty:
            continue
            
        # Extract the final point of the data frame to position the label
        last_row = trace_data.sort_values(by="Time").iloc[-1]
        x_pos = last_row["Time"]
        y_pos = last_row[column]
        
        # Don't place text beyond the set x limit window
        if x_pos > max_x:
            x_pos = max_x - (max_x * 0.05)
            # Interpolate or approximate Y at max_x if needed, 
            # but using last point works well if data ends near max_x
        
        # Pull styling instructions based on control vs ensemble line
        line_color = chosen_palette.get(param, "gray")
        font_wt = "bold" if param == "Relaxed state" else "normal"
        font_sz = 6 if param == "Relaxed state" else 5
        
        # Add text trace to plot right next to the line endpoint
        ax.text(
            x=x_pos + (max_x * 0.01), 
            y=y_pos, 
            s=param, 
            color=line_color, 
            fontsize=font_sz, 
            weight=font_wt,
            va="center",
            ha="left"
        )

    # Dynamic Labels Formatting
    if name is not None:
        plt.ylabel(f"{name} (uM)")
        plt.title(f"{name} at {location.upper()}")
    elif column.startswith("Sum"):
        plt.ylabel(f"Total {active} {species} (uM)")
        plt.title(f"Total {active} {species} at {location.upper()}")
    else:
        plt.ylabel(f"{species} (uM)")
        plt.title(f"{species} at {location.upper()}")

    save_path = f"{out_dir}/{name_plot}-{species}_loc-{location}.pdf"
    plt.savefig(save_path)
    plt.show()
    plt.close()

# Simulation setup
name_folder = "plots"
in_dir_ = "/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1"

plot_list = [
    "06_13_26_metacentric_relaxed_MCF10A_chr19_PMP1", "ensemble_run13", "ensemble_run37", 
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

clean_names = [
    "Relaxed state", "run13", "run37", "run32", "run48", "run76", "run27", "run81", "run57", 
    "run20", "run59", "run87", "run23", "run53", "run98", "run73", "run21", "run29", "run95", 
    "run4", "run24", "run93", "run85", "run40", "run30", "run60", "run3", "run77", "run100", 
    "run74", "run34", "run92", "run19", "run96", "run82", "run12", "run41", "run83", "run84", 
    "run63", "run55", "run45", "run46", "run61", "run43", "run36", "run89", "run8", "run65", 
    "run64", "run79", "run2", "run1", "run50", "run70", "run18", "run5", "run44", "run90", 
    "run66", "run97", "run99", "run16", "run10", "run38", "run15", "run62", "run51", "run78", 
    "run52", "run56", "run35", "run54", "run17", "run9", "run31", "run88", "run86", "run49", 
    "run47", "run14", "run72", "run22", "run28", "run42", "run25", "run69", "run58", "run75"
]

locations = ["ic", "kt", "bg", "ch"]
for loc in locations:
    plot_across_models(
        species="CPC_all",
        plot_list=plot_list,
        in_dir=in_dir_,
        name_list=clean_names,
        location=loc,
        name_plot="07_14_26_relaxed_Chr9_CV0.1",
        active="all",
        name_folder=name_folder,
        custom_palette="husl",
    )