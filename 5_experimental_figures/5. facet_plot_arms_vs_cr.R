
library(ggplot2)
library(tidyr)
library(readxl)

setwd("/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/08-26 All acetylation quantifications/07-25-26 H2A acetylation/Replicate 3")

df <- read_excel("all_data_master_summary.xlsx") #cells_micronuclei spreadsheet


# Assume your current data frame is 'df' and you have your 'i' defined (e.g., i = 1)
# metrics <- c("Mean", "Median", "uq75", "uq80", "uq90")
# 
# for (i in metrics) {
#   x_var <- paste0("Inside_", i, "_acH2A")
#   y_var <- paste0("Outside_", i, "_acH2A")
#   
  # Create a subset with the specific columns needed and reshape into a long format
  # df_subset <- df[, c("cell", x_var, y_var, "Chromosome")]
  # colnames(df_subset) <- c("cell", "Inside", "Outside", "Chromosome")
  # 
  # Create the faceted plot
ggplot(df, aes(x = Inside_Mean_acH2A, y = Outside_Mean_acH2A, color = Chromosome)) +
    geom_point(size = 2, alpha = 0.9) +
   geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "black", alpha = 0.5) + 
    facet_wrap(~ cell) +
    theme_minimal() +
    labs(
      x = "Centromeric intensity",
      y = "Arms intensity",
      title = "Summary: mean")
 
ggsave(filename = "Arm2centromereInt_R.pdf", path ="/Users/catalinaalvarez/Google Drive/My Drive/UVA/Research/JanesLab/CPC_project/CPC experimental/08-26 All acetylation quantifications/07-25-26 H2A acetylation/Replicate 3") 

# }