#########################################################
# Install all needed packages
packages <- c("ggplot2","ggrastr","png","gridExtra","purrr","latex2exp","stringr","utils","tictoc","tidyverse","tibble","scales", "pdftools", "rhdf5", "png")
lapply(packages, require, character.only = TRUE)
tic("total")


# CHANGE: Folder paths
funcPath<-"/Users/catalinaalvarez/Documents/GitHub/CPC_Analysis/functions"
importPath<-"/Users/catalinaalvarez/Documents/CPC_data_2026"
exportPath<-"/Users/catalinaalvarez/Documents/CPC_plots_2026/CV0.1"
desktop<-"/Users/catalinaalvarez/Desktop"

# funcPath<-"/home/aca9pw/4_post_VCell_processing/functions_2026"
# importPath<-"/project/g_bme-janeslab/SarahG/pyvcell_results/16863175"
# exportPath<-"/home/aca9pw/4_post_VCell_processing/CPC_plots_2026"

# Functions
functions<-list.files(funcPath,recursive=TRUE)
functions<-file.path(funcPath,functions)
for(i in functions){
  print(i)
  source(i)
}

#CHANGE: Chromosome geometry
# Chr19 - PMP1
dataDim=c(136,52)#edited
chromWidth=1.3 #um
chromHeight=3.4 #um

# ---------------- LISTS OF SPECIES ---------------

# Species Lists, add any that are required to be on one plot
CPC_all <-c("CPC_all")


# ---------------- HEAT MAPS ---------------

# How many heat maps to return
# Change
H <- 1

heatmap_species <- vector("list", H)
heatmap_info_list <- vector("list", H)

# Change, IN ORDER
heatmap_species[[1]] <- CPC_all

# Change, name of plot in plot directory, also name in heatmap, IN ORDER
heatmap_info_list[[1]] <- c("all CPC")

# ---------------- LINE PLOTS ---------------
L <- 1

all_data <- vector("list", L)
species_info_list <- vector("list", L)
# all_species <- c(CPC_species, CPCa_total, pH3_species, pH2A_species, HASPIN_PLK1_species, BUB1a_pKNL1_species, SGO1_species, bound_CPC, bound_active_CPC, pNDC80_species, pNDC80_total, pH3S10rep, pKNL1, HASPINi, HASPINa, pKNL1_all)
all_species <- c(CPC_all)

# Change, IN ORDER
all_data[[1]] <- CPC_all

# Change, IN ORDER
#species_info_list[[1]] <- c("File name for saving plot", "Title on plots with only inactive species", "Title on plots with only active species", "Title on plots with both active and inactive species",
                            # SUM:"sums of inactive and active species should be added" (Active: Black, Solid & Inactive: Black, Dashed),
                            # TOTAL: "sum of all species should be added",
                            # FULL: "all species should be added to line plots",
                            # COLLAPSIBLE: "whether only the top 4 species and their sums/total should be specified")
species_info_list[[1]] <- c("CPC_all", "Inactive CPC", "Active CPC", "CPC Activation", FALSE, FALSE, TRUE, FALSE)


# ---------------- SIMULATION SPECIFICS ---------------

# Model type, goes on the left of the heatmap
# Change
kt_width = c(
    "Metacentric_Relaxed"
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed",
#     "Metacentric_Relaxed"
# 
)
# 
# # All simulation IDs
# # Change
  sims <- c(
  "SimID_316230588_0__exported"
#   "ensemble_run13/SimID_1659916430_0__exported",
#   "ensemble_run37/SimID_1852478929_0__exported",
#   "ensemble_run32/SimID_1174143904_0__exported",
#   "ensemble_run48/SimID_371420409_0__exported",
#   "ensemble_run76/SimID_1730253940_0__exported",
#   "ensemble_run27/SimID_1323640365_0__exported",
#   "ensemble_run81/SimID_2007203903_0__exported",
#   "ensemble_run57/SimID_2132986709_0__exported",
#   "ensemble_run20/SimID_515133776_0__exported",
#   "ensemble_run59/SimID_1548746213_0__exported",
#   "ensemble_run87/SimID_667083104_0__exported",
#   "ensemble_run23/SimID_157300581_0__exported",
#   "ensemble_run53/SimID_971155492_0__exported",
#   "ensemble_run98/SimID_1897367753_0__exported",
#   "ensemble_run73/SimID_49495671_0__exported",
#   "ensemble_run21/SimID_82293471_0__exported",
#   "ensemble_run29/SimID_464916703_0__exported",
#   "ensemble_run95/SimID_1658467233_0__exported",
#   "ensemble_run4/SimID_558275775_0__exported",
#   "ensemble_run24/SimID_2019067803_0__exported",
#   "ensemble_run93/SimID_1747371907_0__exported",
#   "ensemble_run85/SimID_584896334_0__exported",
#   "ensemble_run40/SimID_1063751170_0__exported",
#   "ensemble_run30/SimID_1633238538_0__exported",
#   "ensemble_run60/SimID_667051310_0__exported",
#   "ensemble_run3/SimID_976605771_0__exported",
#   "ensemble_run77/SimID_624424470_0__exported",
#   "ensemble_run100/SimID_1767894091_0__exported",
#   "ensemble_run74/SimID_1714366672_0__exported",
#   "ensemble_run34/SimID_2012260857_0__exported",
#   "ensemble_run92/SimID_1228797912_0__exported",
#   "ensemble_run19/SimID_983310548_0__exported",
#   "ensemble_run96/SimID_633814112_0__exported",
#   "ensemble_run82/SimID_1962320143_0__exported",
#   "ensemble_run12/SimID_669535503_0__exported",
#   "ensemble_run41/SimID_1577765662_0__exported",
#   "ensemble_run83/SimID_1499556403_0__exported",
#   "ensemble_run84/SimID_1771464932_0__exported",
#   "ensemble_run63/SimID_273878190_0__exported",
#   "ensemble_run55/SimID_1377777267_0__exported",
#   "ensemble_run45/SimID_1013511251_0__exported",
#   "ensemble_run46/SimID_367349224_0__exported",
#   "ensemble_run61/SimID_2103443806_0__exported",
#   "ensemble_run43/SimID_102516_0__exported",
#   "ensemble_run36/SimID_625109031_0__exported",
#   "ensemble_run89/SimID_1179757200_0__exported",
#   "ensemble_run8/SimID_1998822596_0__exported",
#   "ensemble_run65/SimID_1901464818_0__exported",
#   "ensemble_run64/SimID_291803680_0__exported",
#   "ensemble_run79/SimID_1825165209_0__exported",
#   "ensemble_run2/SimID_1294574654_0__exported",
#   "ensemble_run1/SimID_1786071476_0__exported",
#   "ensemble_run50/SimID_1341540332_0__exported",
#   "ensemble_run70/SimID_1748141074_0__exported",
#   "ensemble_run18/SimID_1864999998_0__exported",
#   "ensemble_run5/SimID_2105582645_0__exported",
#   "ensemble_run44/SimID_1737891094_0__exported",
#   "ensemble_run90/SimID_1922497650_0__exported",
#   "ensemble_run66/SimID_269068068_0__exported",
#   "ensemble_run97/SimID_1428849649_0__exported",
#   "ensemble_run99/SimID_1334221591_0__exported",
#   "ensemble_run16/SimID_184833552_0__exported",
#   "ensemble_run10/SimID_393615482_0__exported",
#   "ensemble_run38/SimID_1385927133_0__exported",
#   "ensemble_run15/SimID_1796435746_0__exported",
#   "ensemble_run62/SimID_720638095_0__exported",
#   "ensemble_run51/SimID_324372520_0__exported",
#   "ensemble_run78/SimID_675086644_0__exported",
#   "ensemble_run52/SimID_628479837_0__exported",
#   "ensemble_run56/SimID_1482607664_0__exported",
#   "ensemble_run35/SimID_1538038555_0__exported",
#   "ensemble_run54/SimID_365697982_0__exported",
#   "ensemble_run17/SimID_1613430057_0__exported",
#   "ensemble_run9/SimID_1347651621_0__exported",
#   "ensemble_run31/SimID_1613394600_0__exported",
#   "ensemble_run88/SimID_808717142_0__exported",
#   "ensemble_run86/SimID_926719637_0__exported",
#   "ensemble_run49/SimID_121702330_0__exported",
#   "ensemble_run47/SimID_1736281535_0__exported",
#   "ensemble_run14/SimID_2110558630_0__exported",
#   "ensemble_run72/SimID_630945050_0__exported",
#   "ensemble_run22/SimID_707905839_0__exported",
#   "ensemble_run28/SimID_1874630207_0__exported",
#   "ensemble_run42/SimID_827035766_0__exported",
#   "ensemble_run25/SimID_309425260_0__exported",
#   "ensemble_run69/SimID_106791967_0__exported",
#   "ensemble_run58/SimID_640723070_0__exported",
#   "ensemble_run75/SimID_1897651770_0__exported"
  

  )

# Folder naming corresponding to specific simulation ID
# Change
var <- c(
  "06_13_26_metacentric_relaxed_MCF10A_chr19_PMP1"
  # "ensemble_run13",
  # "ensemble_run37",
  # "ensemble_run32",
  # "ensemble_run48",
  # "ensemble_run76",
  # "ensemble_run27",
  # "ensemble_run81",
  # "ensemble_run57",
  # "ensemble_run20",
  # "ensemble_run59",
  # "ensemble_run87",
  # "ensemble_run23",
  # "ensemble_run53",
  # "ensemble_run98",
  # "ensemble_run73",
  # "ensemble_run21",
  # "ensemble_run29",
  # "ensemble_run95",
  # "ensemble_run4",
  # "ensemble_run24",
  # "ensemble_run93",
  # "ensemble_run85",
  # "ensemble_run40",
  # "ensemble_run30",
  # "ensemble_run60",
  # "ensemble_run3",
  # "ensemble_run77",
  # "ensemble_run100",
  # "ensemble_run74",
  # "ensemble_run34",
  # "ensemble_run92",
  # "ensemble_run19",
  # "ensemble_run96",
  # "ensemble_run82",
  # "ensemble_run12",
  # "ensemble_run41",
  # "ensemble_run83",
  # "ensemble_run84",
  # "ensemble_run63",
  # "ensemble_run55",
  # "ensemble_run45",
  # "ensemble_run46",
  # "ensemble_run61",
  # "ensemble_run43",
  # "ensemble_run36",
  # "ensemble_run89",
  # "ensemble_run8",
  # "ensemble_run65",
  # "ensemble_run64",
  # "ensemble_run79",
  # "ensemble_run2",
  # "ensemble_run1",
  # "ensemble_run50",
  # "ensemble_run70",
  # "ensemble_run18",
  # "ensemble_run5",
  # "ensemble_run44",
  # "ensemble_run90",
  # "ensemble_run66",
  # "ensemble_run97",
  # "ensemble_run99",
  # "ensemble_run16",
  # "ensemble_run10",
  # "ensemble_run38",
  # "ensemble_run15",
  # "ensemble_run62",
  # "ensemble_run51",
  # "ensemble_run78",
  # "ensemble_run52",
  # "ensemble_run56",
  # "ensemble_run35",
  # "ensemble_run54",
  # "ensemble_run17",
  # "ensemble_run9",
  # "ensemble_run31",
  # "ensemble_run88",
  # "ensemble_run86",
  # "ensemble_run49",
  # "ensemble_run47",
  # "ensemble_run14",
  # "ensemble_run72",
  # "ensemble_run22",
  # "ensemble_run28",
  # "ensemble_run42",
  # "ensemble_run25",
  # "ensemble_run69",
  # "ensemble_run58",
  # "ensemble_run75"
  
)
#########################################################

for(i in 1:length(sims)){
  if(file.exists(importPath) == TRUE){


    sweep_name<-var[i]

    print(sweep_name)


    dir.create(file.path(exportPath, sweep_name))
    exportPath_new <- paste(exportPath, sweep_name, sep="/")


    save_plots(sims[i],
               paste(kt_width[i], "Model"),
               heatmap_species,
               heatmap_info_list,
               all_data,
               all_species,
               species_info_list,
               tInit=0,
               tSpan=100,
               desiredInterval=1,
               nHeatmaps = 7,
               # alternative_range <- NULL, #when equal spacing is enough on heatmaps
               alternative_range <- c(0, 10, 20, 25, 30, 40, 50), #alternative desired time points to be plotted on heatmaps
               # alternative_range <- c(0, 20, 30, 50, 70, 90, 100), #alternative desired time points to be plotted on heatmaps
               cutoff=list("CPC"=11), #for heatmap color bar
               funcPath,
               importPath,
               exportPath_new,
               kt_width[i],
               movie = FALSE,
               lineplots=TRUE,
               KK_dist_relaxed = 0.575,
               KK_dist_tensed = 1.15,
               KT_width= 0.075,
               KT_height = 0.3, #0.3 um in model
               cohesin_width = 0.1) #0.1 um in model

  }

}

