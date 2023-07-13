x=1:100
library(dplyr)
y=log(x)
x2=x^2
x3=x^3
# fit=lm(y~x+x2+x3)
fit=lm(y~poly(x,10))
fit%>%summary()
fit2%>%summary()
x^2
pred=predict(fit)
plot(x, y, main = "Predicted vs Actual", xlab = "X", ylab = "Actual", col = "blue",type="l")
points(x, pred, col = "red",type="l")