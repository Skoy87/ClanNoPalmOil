rm(list=ls())
library(data.table)
library(dplyr)
library(ggplot2)
data <- fread("../clan.csv")
data$time <- unlist(lapply(strsplit(data$date," "), function(x) x[2]))
data$date <- unlist(lapply(strsplit(data$date," "), function(x) x[1]))
data[grep("2018-03-19", date)]$date <- "19/03/2018"
data[grep("2018-03-20", date)]$date <- "20/03/2018"
data$date <- as.Date(data$date,format = "%d/%m/%Y")

data$date_time <- as.POSIXct(with(data, paste0(date," ",time)))

data <- as.data.table(data %>% select(-one_of(c("time","date"))))
data_melted <- melt(data,id.vars = c("tag","name","date_time"))

plot_trophies_by_user <- ggplot(data_melted[variable=='trophies']) + geom_line(aes(x=date_time,y=value)) +
  theme_bw()+ theme(axis.text.x = element_text(angle = 90))+
  scale_x_datetime() + xlab("Day - time") + ylab("Trophies")+facet_wrap(~name)

plot_donations_by_user <- ggplot(data_melted[variable %in% c('donations','donationsReceived')]) + 
  geom_line(aes(x=date_time,y=value, colour=variable)) + theme_bw()+ theme(axis.text.x = element_text(angle = 90, hjust=1))+
  scale_x_datetime() + xlab("Day - time") + ylab("Donations")+facet_wrap(~name)