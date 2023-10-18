# 必要なライブラリを読み込む
library(plm)
library(lmtest)
library(sandwich)
library(pretrends)

# データの読み込み
df <- read.csv("./data/merged/len3_ship_DN.csv", header = TRUE, encoding = "shift-jis")

# 必要な列を抽出・変換
df <- df[df$otc_dom > 0 & df$rx_dom > 0, ]
df$log_rx_dom <- log(df$rx_dom)
df$log_otc_dom <- log(df$otc_dom)
df$log_stock_rx_lag <- log(df$stock_rx_lag + 0.001)
df$log_stock_otc_lag <- log(df$stock_otc_lag + 0.001)
df$year_trend <- df$year - 2008

# パネルデータに変換
df_panel <- pdata.frame(df, index = c("id", "year"))

# モデル1の推定
formula1 <- log_rx_dom ~ year_trend + elapsed_m10 + elapsed_m9 + elapsed_m8 + elapsed_m7 + elapsed_m6 +
elapsed_m5 + elapsed_m4 + elapsed_m3 + elapsed_m2 + elapsed_0 + elapsed_1 + elapsed_2 + elapsed_3 +
elapsed_4 + elapsed_5 + elapsed_6 + elapsed_7 + elapsed_8 + elapsed_9 + elapsed_10 + elapsed_11 +
elapsed_12 + elapsed_13 + elapsed_14 + elapsed_15 + generic_per+log_stock_rx_lag + generic_share_r + generic_share_q

model1 <- plm(formula1, data = df_panel, model = "within", effect = "twoways")
summary_model1 <- coeftest(model1, vcov. = vcovHC(model1, type = "HC3"))
print(summary_model1)

# モデル2の推定
formula2 <- log_otc_dom ~ elapsed_m10 + elapsed_m9 + elapsed_m8 + elapsed_m7 + elapsed_m6 + elapsed_m5 +
elapsed_m4 + elapsed_m3 + elapsed_m2 + elapsed_0 + elapsed_1 + elapsed_2 + elapsed_3 + elapsed_4 +
elapsed_5 + elapsed_6 + elapsed_7 + elapsed_8 + elapsed_9 + elapsed_10 + elapsed_11 + elapsed_12 +
elapsed_13 + elapsed_14 + elapsed_15 + generic_per + log_stock_otc_lag +
generic_share_r + generic_share_q

model2 <- plm(formula2, data = df_panel, model = "within", effect = "twoways")
summary_model2 <- coeftest(model2, vcov. = vcovHC(model2, type = "HC3"))
print(summary_model2)
beta=summary_model2[1:25, 1]
sigma=vcovHC(model2, type = "HC3")[1:25, 1:25]
# -10 to 15 and drop the reference period
tVec=seq(-10,15,1)[-10]
referencePeriod <- -1 #This is the omitted period in the regression
data.frame(t = tVec, beta = beta)
slope50 <-
slope_for_power(sigma = sigma,
                targetPower = 0.8,
                tVec = tVec,
                referencePeriod = referencePeriod)
slope50

pretrendsResults <- 
  pretrends(betahat = beta, 
            sigma = sigma, 
            tVec = tVec, 
            referencePeriod = referencePeriod,
            deltatrue = slope50 * (tVec - referencePeriod))
pretrendsResults$event_plot
pretrendsResults$df_power
