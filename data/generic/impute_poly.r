library(dplyr)
data=read.csv("./data/generic/generic_usage_nan.csv")
# getwd()
x=data$Year
y=data$Percentage
fit=lm(y~poly(x,5),na.action = na.omit)
fit%>%summary()
pred=predict(fit)
plot(x, y, main = "Predicted vs Actual", xlab = "X", ylab = "Actual", col = "blue")
points(x, pred, col = "red",type="l")
pred
res=predict(fit,newdata=list(data$Year))
# res
