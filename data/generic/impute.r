library(dplyr)
library(imputeTS)
data=read.csv("./data/generic/generic_usage_nan.csv")
data%>%select(Year,Percentage)->data

imp=na_interpolation(data)
ggplot_na_imputations(data$Percentage, imp$Percentage)
imp
