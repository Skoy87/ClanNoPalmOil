#INSTRUCTIONS:
# 1. source this file
# 2. run the following lines:
#    OUTPUT_DIR = 'plots/'
#    PATH_TO_CLAN_CSV = '../clan.csv'
# 3. run plots_stats <- pipeline_plots(PATH_TO_CLAN_CSV=PATH_TO_CLAN_CSV,OUTPUT_DIR=OUTPUT_DIR)


#OUTPUT_DIR = 'plots/'
#PATH_TO_CLAN_CSV = '../clan.csv'

pipeline_plots <- function(PATH_TO_CLAN_CSV, OUTPUT_DIR){
  load_pkgs()
  if(!dir.exists(OUTPUT_DIR)){dir.create(path = OUTPUT_DIR)}
  plots_stats <- plot_stats_clan(path_to_clan_csv=PATH_TO_CLAN_CSV,
                                 output_dir = OUTPUT_DIR)
  return(plots_stats)
}

load_pkgs <- function(){
  library(data.table)
  library(dplyr)
  library(ggplot2)
}

plot_stats_clan <- function(path_to_clan_csv, output_dir){
  
  data <- fread(path_to_clan_csv)
  data$date <- as.POSIXct(data$date)
  data_melted <- melt(data,id.vars = c("tag","name","date"))
  
  plot_trophies_by_user <- ggplot(data_melted[variable=='trophies']) + geom_line(aes(x=date,y=value)) +
    theme_bw()+ theme(axis.text.x = element_text(angle = 90))+
    scale_x_datetime() + xlab("Day - time") + ylab("Trophies")+facet_wrap(~name)
  
  plot_donations_by_user <- ggplot(data_melted[variable %in% c('donations','donationsReceived')]) + 
    geom_line(aes(x=date,y=value, colour=variable)) + theme_bw()+ theme(axis.text.x = element_text(angle = 90, hjust=1))+
    scale_x_datetime() + xlab("Day - time") + ylab("Donations")+facet_wrap(~name)
  
  list_plots <- list()
  list_plots$plot_trophies_by_user <- plot_trophies_by_user
  list_plots$plot_donations_by_user <- plot_donations_by_user
  
  trophies_plot_name = paste0(output_dir,"/trophies_plot_",Sys.Date(),".pdf")
  donations_plot_name = paste0(output_dir,"/donations_plot_",Sys.Date(),".pdf")
  
  ggsave(plot = plot_trophies_by_user,filename = trophies_plot_name, width = 30, units = "cm")
  ggsave(plot = plot_donations_by_user,filename = donations_plot_name, width = 30, units = "cm")
  
  return(list_plots)
}
