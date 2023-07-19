library(plm)
library(dplyr)
# install.packages("lme4")
library(lme4)
getwd()
data=read.csv("./data/len3_agg.csv")
data%>%colnames()
panel_data<-pdata.frame(data,index=c("id","year"))
panel_data%>%head()

# pooling  rx
# -3 ~ +5
fixed_model<-plm(rx_dom ~ Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, model = "pooling", effect = "twoways")
fixed_model%>%summary()

# random rx
# -3 ~ +3
fixed_model<-plm(rx_dom ~ Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, 
model = c("random"), effect = "twoways")
fixed_model%>%summary()


# random otc
# -3 ~ +3
fixed_model2<-plm(otc_dom ~ Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, model = "random", effect = "twoways")
fixed_model%>%summary()

# random log otc
# -5 to +10
fixed_model2<-plm(log(otc_dom+0.001) ~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10-1, data = panel_data, model = "random", effect = "twoways")
fixed_model2%>%summary()


# random log otc
# -3 ~ +3
fixed_model2<-plm(log(otc_dom+0.001) ~ Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3-1, data = panel_data, model = "random", effect = "twoways")
fixed_model2%>%summary()


# random log rx
# -3 ~ +3
fixed_model2<-plm(log(rx_dom+0.001) ~ Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3-1, data = panel_data, model = "random", effect = "twoways")
fixed_model2%>%summary()

# make factors
time_dummy <- model.matrix(~ factor(data$year) - 1)
id_dummy <- model.matrix(~ factor(data$id) - 1)

# log year and id dummy
# -5 to +10
fixed_model3<-lm(log(rx_dom+0.001) ~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+id_dummy-1, data = data)
fixed_model3%>%summary()

fixed_model3<-lm(log(otc_dom+0.001) ~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+id_dummy-1, data = data)
fixed_model3%>%summary()


# level year and id dummy
# -5 to +10
fixed_model3<-lm(rx_dom~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+id_dummy-1, data = data)
fixed_model3%>%summary()

fixed_model3<-lm(otc_dom ~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+id_dummy-1, data = data)
fixed_model3%>%summary()

# year dropped
fixed_model3<-lm(rx_dom~ Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+id_dummy-1, data = data)
fixed_model3%>%summary()

# mixed
# level
# -5 to 10
model <- lmer(rx_dom ~ Percentage +Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
model%>%summary()

model <- lmer(otc_dom ~ Percentage +Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
model%>%summary()

# -3 to 5
model <- lmer(rx_dom ~ Percentage +Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
model%>%summary()

model <- lmer(otc_dom ~ Percentage +Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
model%>%summary()
# log
model <- lmer(log(rx_dom+0.001) ~ Percentage +Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+(1|id)-1, data=data)
model%>%summary()

model <- lmer(log(otc_dom+0.001) ~ Percentage +Percentage+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
model%>%summary()

# -3 to 5
model <- lmer(log(rx_dom+0.001) ~ Percentage +Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
model%>%summary()

model <- lmer(log(otc_dom+0.001) ~ Percentage +Percentage+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
model%>%summary()