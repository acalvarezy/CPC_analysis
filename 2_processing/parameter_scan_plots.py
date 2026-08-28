import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import numpy as np
in_dir = "/Users/catalinaalvarez/Documents/cpc_plots_2023"
#import matplotlib as m
import os

# PARAMETERS SCAN PLOT
def lineplot(species, in_dir, sim_prefix, name_scan, num_scans, xmax = None, xmin = 0, log = False,
              location = 'ic',column = "Sum_Active", active = 'active', name = None, suffix = "",
              highlight = None, name_folder = "", palette = sns.color_palette("crest", as_cmap=True)):

    if os.path.isdir(f"/Users/catalinaalvarez/Documents/cpc_plots_2023/figures/lineplot_param_scans/{name_folder}"):
        pass
    else:
        os.makedirs(f"/Users/catalinaalvarez/Documents/cpc_plots_2023/figures/lineplot_param_scans/{name_folder}")
    plot_data = pd.DataFrame()

    if log:
        param_range = np.logspace(start = np.log10(xmin), stop = np.log10(xmax), num = num_scans, endpoint = True)
    else:
        if xmax is not None:
            step = (xmax - xmin) / (num_scans - 1)
            param_range = np.arange(start=xmin, stop=xmax+step, step=step)
        else:
            param_range = np.arange(num_scans)

    if active == 'all':
        for i in range(num_scans):
            # if i == 5: continue
            param = param_range[i]
            tmp = pd.read_csv(f"{in_dir}/{sim_prefix}{i}/data/data_{location}_{species}.csv", header=0,
                              index_col=None)
            tmp['Time'] = 10 * tmp['Time']
            tmp['parameter'] = param
            tmp['all'] = tmp[list(set(tmp.columns).difference({"Time",'parameter'}))].sum(axis = 1)
            plot_data = pd.concat([plot_data, tmp[['parameter', 'all', 'Time']]], ignore_index=True)
            column = 'all'
    else:
        if active == 'inactive' and column == 'Sum_Active':
            column = 'Sum_Inactive'
        if active == 'active' and column == 'Sum_Inactive':
            column = 'Sum_Active'
        for i in range(num_scans):
            # if i == 5: continue
            param = param_range[i]
            tmp = pd.read_csv(f"{in_dir}/{sim_prefix}{i}/data/data_{active}_{location}_{species}.csv", header=0,
                              index_col=None)
            tmp['Time'] = 10 * tmp['Time']
            tmp['parameter'] = param
            plot_data = pd.concat([plot_data, tmp[['parameter', column, 'Time']]], ignore_index=True)


    if log:
        ax = sns.lineplot(x = plot_data['Time'].to_numpy(), y= plot_data[column].to_numpy(), hue = plot_data['parameter'].to_numpy(),
                      hue_norm=m.colors.LogNorm(), palette = palette)
    else:
        ax = sns.lineplot(x=plot_data['Time'].to_numpy(), y=plot_data[column].to_numpy(),
                          hue=plot_data['parameter'].to_numpy(),palette = palette)
    plt.xlabel("Time (s)")
    if name is not None:
        plt.ylabel(f"{name} (uM)")
        plt.title(f"{name} at {location.upper()}")

    else:
        if column.startswith('Sum'):
            plt.ylabel(f"Total {active} {species} (uM)")
            plt.title(f"Total {active} {species} at {location.upper()}")
                      # f"Parameter scan over {name_scan}")
        else:
            plt.ylabel(f"{species} (uM)")
            plt.title(f"{species} at {location.upper()}")

    if highlight is not None:
        if active == 'all':
            tmp = pd.read_csv(f"{in_dir}/{highlight}/data/data_{location}_{species}.csv", header=0,
                              index_col=None)
            tmp['all'] = tmp[list(set(tmp.columns).difference({"Time",'parameter'}))].sum(axis = 1)

        else:
            tmp = pd.read_csv(f"{in_dir}/{highlight}/data/data_{active}_{location}_{species}.csv", header=0, index_col=None)
        tmp['Time'] = 10 * tmp['Time']

        sns.lineplot(x = tmp['Time'].to_numpy(), y= tmp[column].to_numpy(), color = 'black',linestyle = "dotted", ax = ax, legend=False)


    if log:
        norm = m.colors.LogNorm(xmin, xmax)
    else:
        if xmax is not None:
            norm = plt.Normalize(xmin, xmax)
        else:
            norm = plt.Normalize(0, 100)
    # old color palette: sns.cubehelix_palette(as_cmap=True)
    sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
    sm.set_array([])
    # Remove the legend and add a colorbar (optional)
    ax.get_legend().remove()
    if xmax is not None:
        ax.figure.colorbar(sm, label = f"{name_scan} (uM)", ticks=param_range, ax=ax)
    else:
        ax.figure.colorbar(sm, label = f"{name_scan} (%)")
        
    plt.tight_layout()
    print("saving fig")
    plt.savefig(f"/Users/catalinaalvarez/Documents/cpc_plots_2023/figures/lineplot_param_scans/{name_folder}/scan-{name_scan}_species-{species}_loc-{location}{suffix}.pdf")
    plt.show()
    plt.close()

name_folder = "Kon scan 12-27-24"
in_dir_ = "/Users/catalinaalvarez/Documents/cpc_plots_2023"
sim_prefix = "12_27_24_relaxed_RefModel_MonseData_Kon_"
name_scan = 'Kon'
num_scans = 5
xmin = 0.1
xmax = 0.5
lineplot('CPC', in_dir_, sim_prefix, name_scan, num_scans, xmax, location='ic')
lineplot('CPC', in_dir_, sim_prefix, name_scan, num_scans, xmax, location='kt')

in_dir_ = "/Users/catalinaalvarez/Documents/cpc_plots_2023/Knl1_plots/Bub1_0.006"
sim_prefix = "03_21_24_relaxed_RefModel_Bub10.006_Knl1_"
name_scan = 'Knl1 IC'
num_scans = 10
xmax = 180
lineplot('CPC', in_dir_, sim_prefix, name_scan, num_scans, xmax, location = 'kt', suffix = '_Bub1_0.006')
lineplot('CPC', in_dir_, sim_prefix, name_scan, num_scans, xmax, location = 'ic', suffix = '_Bub1_0.006')

#Example with log:
sim_prefix = "02_19_24_relaxed_RefModel_Mps1_phos_Plk1a_20Pac_transactiv_CPCi_scan_FIXED_not20Pac "
name_scan = 'CPCi IC'
num_scans = 11
log = False
xmin = 0
xmax = 1.065
lineplot('CPC', in_dir, sim_prefix, name_scan, num_scans, xmax, location='ic')

#Example with one highlight:
sim_prefix = "04_01_24_tensed_RefModel_Bub1_his_scan"
name_scan = 'Bub1a_his_KD'
num_scans = 6
xmin = 0.001
xmax = 100
lineplot('CPC', in_dir, sim_prefix, name_scan, num_scans, xmax = xmax, xmin = xmin,
          location='kt', log = True, active = 'all',
          suffix = '_all',
          highlight = "04_01_24_tensed_RefModel_Bub1_his_scan3",
          name_folder="Bub1-his-scan-tensed_rainbow")








