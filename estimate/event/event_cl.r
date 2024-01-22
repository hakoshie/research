# install.packages("did2s")

# Automatically loads fixest
library(did2s)
library(dplyr)

# Load Data from R package
# data("df_het", package = "did2s")
# df_het = as.data.frame(df_het)
# df_het%>%head(5)
df=read.csv("./data/merged/len3_ship_cl_DN.csv")
# data%>%
df <- df[df$otc_dom > 0 & df$rx_dom > 0, ]
df$log_rx_dom <- log(df$rx_dom)
df$log_otc_dom <- log(df$otc_dom)
df$log_stock_rx_lag <- log(df$stock_rx_lag + 0.001)
df$log_stock_otc_lag <- log(df$stock_otc_lag + 0.001)
df%>%filter(otc_dom>0)->df
colnames(df)
# df$log_otc_dom=log(df$otc_dom)
# pwd
# Event Study
df%>%dim()
df$treat=ifelse(df$elapsed>=0,1,0)
df$unit = paste(as.character(df$id), as.character(df$year), sep="-")
df$unit
# data$g=ifelse(data$elapsed>=0,data$release_year,0)
es <- did2s(df,
  yname = "log_rx_dom", first_stage = ~ 0 | id + year,
  second_stage = ~ i(elapsed, ref=c(-1,-2,Inf)), treatment = "treat",
  cluster_var = "year"
)
fixest::iplot(es, main = "Event study: Staggered treatment", xlab = "Relative time to treatment", col = "steelblue", ref.line = -0.5)

df$elapsed%>%summary()
for (i in 1:20){
  df%>%filter(elapsed==i-1)%>%dim()->n
#   cat(i-1,n,"\n")
}
es
#> Running Two-stage Difference-in-Differences
#>  - first stage formula `~ 0 | state + year`
#>  - second stage formula `~ i(rel_year, ref = c(-1, Inf))`
#>  - The indicator variable that denotes when treatment is on is `treat`
#>  - Standard errors will be clustered by `state`

df%>%select(id,year,elapsed,treat,log_otc_dom)%>%tail(15)


twfe = feols(log_rx_dom ~ i(elapsed, ref=c(-1, Inf,-2))| id + year, data = df) 

fixest::iplot(list(es, twfe), sep = 0.2, ref.line = -0.5,
      col = c("steelblue", "#82b446"), pt.pch = c(20, 18), 
      xlab = "Relative time to treatment", 
      main = "Event study: Staggered treatment (comparison)")


# Legend
legend(x=-15, y=7, col = c("steelblue", "#82b446"), pch = c(20, 18), 
       legend = c("Two-stage estimate", "TWFE"))

# out = event_study(
#   data = data, yname = "log_otc_dom", idname = "unit",
#   tname = "year", gname = "release_year", estimator = "all"
# )
plot_event_study(out, horizon = c(-5,10))



df%>%select(year)%>%unique()
df%>%select(release_year)%>%unique()
