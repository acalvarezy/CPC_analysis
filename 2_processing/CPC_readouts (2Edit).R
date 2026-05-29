packages <- c("ggplot2","plotrix","forcats","dplyr","tidyr", "pdftools", "png", "gridExtra", "cowplot")
lapply(packages, require, character.only = TRUE)

#Access the folders and read the data
importPath<-"/Users/catalinaalvarez/Documents/CPC_plots_2026"

var <- c(
  "03_31_26_metacentric_relaxed_MCF10A_chr19_PMP1_kpps=0.1s",
  "03_31_26_metacentric_tensed_MCF10A_chr19_PMP1_kpps=0.1s"
)

timepoint = 40
timepoint = timepoint+1

df <- data.frame(
  state = character(),  # Character type column
  cumboundCPC = numeric(),    # Numeric type column
  averageboundCPC = numeric(),    # Numeric type column
  activeboundCPC_ic = numeric(),  # Numeric type column
  activeboundCPC_kt = numeric(),  # Numeric type column
  pNDC80rep = numeric(),   # Numeric type column
  pH3S10rep = numeric()   # Numeric type column
)

for(i in 1:length(var)){
  if(file.exists(importPath) == TRUE){
    
    sweep_name<-var[i]
    print(sweep_name)
    exportPath <- paste0(importPath, '/' ,var[i])
    datadir <- file.path(importPath, var[i], "data")
    
    
    if (grepl("tensed", var[i], ignore.case = FALSE)) {
      state <- "Tensed"
    } else {
      state <- "Relaxed"
    }
    
    # Find the matching file for the desired variables
    file_pattern1 <- "cumulative_bound_CPC_IC.csv"
    data <- read.csv(file.path(datadir, file_pattern1),
                 header = TRUE)
      cumboundCPC       = data[timepoint, 3]
      averageboundCPC    = data[timepoint, 4]
      
     file_pattern2 <- "data_active_ic_bound_active_CPC.csv"
     data <- read.csv(file.path(datadir, file_pattern2),
                       header = TRUE)
     
     activeboundCPC_ic <- data[timepoint, 2]
     
     file_pattern3 <- "data_active_kt_bound_active_CPC.csv"
     data <- read.csv(file.path(datadir, file_pattern3),
                       header = TRUE)
     activeboundCPC_kt <- data[timepoint, 2]
      
     file_pattern4 <- "data_kt_pNDC80rep.csv"
     data <- read.csv(file.path(datadir, file_pattern4),
                      header = TRUE)
     pNDC80rep <- data[timepoint, 2]/469.9543485

    file_pattern5 <- "data_active_ic_pH3S10rep.csv"
     data <- read.csv(file.path(datadir, file_pattern5),
                      header = TRUE)
     pH3S10rep <- data[timepoint, 2]/120

     
   new_row <- data.frame(state, cumboundCPC, averageboundCPC, activeboundCPC_ic, activeboundCPC_kt,  pNDC80rep, pH3S10rep)                      
   df <- rbind(df, new_row)
     
  }
}
dir.create(file.path(exportPath), showWarnings = FALSE, recursive = TRUE)
csv_path <- file.path(exportPath, "CPC_readouts.csv")
write.csv(df, csv_path, row.names = FALSE)
cat(sprintf("Table saved to: %s\n", csv_path))

#Barplots
#CPC intensities
df$state <- factor(df$state, levels = c('Relaxed', 'Tensed'))
p1 <- ggplot(df, aes(x=state, y=cumboundCPC, fill=state))+ geom_bar(stat="identity", width=0.5) +
   theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('CPC cumulative K2K (uM)') + xlab('') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none")

p2 <- ggplot(df, aes(x=state, y=averageboundCPC, fill=state))+ geom_bar(stat="identity", width=0.5) +
  theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('CPC average K2K (uM)') + xlab('') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none")

p3 <- ggplot(df, aes(x=state, y=activeboundCPC_ic, fill=state))+ geom_bar(stat="identity", width=0.5) +
  theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('Active CPC IC (uM)') + xlab('') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none") +
  geom_hline(yintercept = 3.679, linetype = "dashed", color = "black", size = 1)

p4 <- ggplot(df, aes(x=state, y=activeboundCPC_kt, fill=state))+ geom_bar(stat="identity", width=0.5) +
  theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('Active CPC KT (uM)') + xlab('') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none") +
  geom_hline(yintercept = 3.679, linetype = "dashed", color = "black", size = 1)

p5 <- ggplot(df, aes(x=state, y=pNDC80rep, fill=state))+ geom_bar(stat="identity", width=0.5) +
  theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('pNDC80rep (%)') + xlab('Chromosome state') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none")

p6 <- ggplot(df, aes(x=state, y=pH3S10rep, fill=state))+ geom_bar(stat="identity", width=0.5) +
  theme(panel.background = element_blank(),panel.border = element_rect(fill = NA)) +
  ylab('pH3S10rep (%)') + xlab('') + geom_col(width = 0.5, position = position_dodge(0.9)) +
  scale_fill_brewer(palette = "Set1", direction = -1) + theme(legend.position = "none")

plot_grid(p1, p2, p3, p4, p5, p6, ncol=3)
ggsave('CPC_readouts.pdf', path = exportPath, dpi=300, height=11, width = 13, units='cm')



