library(dplyr)
library(imputeTS)
library(stats)

# パラメータを設定
x <- seq(2010, 2010+n, by = 1)
y=0.6+0.09*x-0.04*x^2

data=c(NA,NA,NA,y)
imp=na_ma(data)
imp=na_kalman(data,smooth = TRUE)
imp=na_kalman(data,smooth = FALSE)
imp=na_kalman(data,smooth = TRUE)
# imp=na_kalman(data,model="auto.arima",smooth = TRUE)
# imp=na_interpolation(data,option="spline")
# imp=na_interpolation(data,option="stine")
imp