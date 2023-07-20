library(plm)
library(dplyr)
# install.packages("lme4")
library(lme4)
getwd()
# whole data
# data=read.csv("./data/len3_agg.csv")

# data dropped never treated group
data=read.csv("./data/len3_drop_never.csv")
data%>%colnames()

# for log
data<-data%>%filter(otc_dom>0)
data%>%mutate(generic.=generic./100)->data
# data%>%mutate(year=year-2008)->data
data%>%head()

panel_data<-pdata.frame(data,index=c("id","year"))
panel_data%>%head()
panel_data%>%colnames()

# id dummy
# id_dummy=model.matrix(~factor(data$id)-1)
# drop first
id_dummy=model.matrix(~factor(data$id)-1)[,-1]

# time dummy
time_dummy=model.matrix(~factor(data$year)-1)
# drop first
# time_dummy=model.matrix(~factor(data$year)-1)[,-1]

data%>%select(matches("elasped_(m[0-5]|[0-9]|1\\d|20)$"))%>%as.matrix()->event

# log year and id dummy
# -5 to +20

fixed_model3<-lm(log(rx_dom)~ log(generic.)+event+id_dummy+time_dummy-1, data = data)
fixed_model3%>%summary()

fixed_model3<-lm(log(otc_dom) ~ log(generic.)+event+id_dummy+time_dummy-1, data = data)
fixed_model3%>%summary()

# drop time dummy

fixed_model3<-lm(log(rx_dom)~ log(generic.)+event+id_dummy-1, data = data)
fixed_model3%>%summary()

fixed_model3<-lm(log(otc_dom) ~ log(generic.)+event+id_dummy-1, data = data)
fixed_model3%>%summary()



# # level year and id dummy
# # -5 to +10
fixed_model3<-lm(rx_dom ~ year+generic.+event+time_dummy+id_dummy-1, data = data)
fixed_model3%>%summary()

fixed_model3<-lm(otc_dom ~ year+generic.+event+time_dummy+id_dummy-1, data = data)
fixed_model3%>%summary()

# # pooling  rx
# # -3 ~ +5
# fixed_model<-plm(rx_dom ~ generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, model = "pooling", effect = "twoways")
# fixed_model%>%summary()

# # random rx
# # -3 ~ +3
# fixed_model<-plm(rx_dom ~ generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, 
# model = c("random"), effect = "twoways")
# fixed_model%>%summary()


# # random otc
# # -3 ~ +3
# fixed_model2<-plm(otc_dom ~ generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5-1, data = panel_data, model = "random", effect = "twoways")
# fixed_model2%>%summary()

# # random log otc
# # -5 to +10
# fixed_model2<-plm(log(otc_dom+0.001) ~ generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10-1, data = panel_data, model = "random", effect = "twoways")
# fixed_model2%>%summary()


# # random log otc
# # -3 ~ +3
# fixed_model2<-plm(log(otc_dom+0.001) ~ generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3-1, data = panel_data, model = "random", effect = "twoways")
# fixed_model2%>%summary()


# # random log rx
# # -3 ~ +3
# fixed_model2<-plm(log(rx_dom+0.001) ~ generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3-1, data = panel_data, model = "random", effect = "twoways")
# fixed_model2%>%summary()




# # year dropped
# fixed_model3<-lm(rx_dom~ generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+id_dummy-1, data = data)
# fixed_model3%>%summary()

# # mixed
# # level
# # -5 to 10
# model <- lmer(rx_dom ~ generic. +generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
# model%>%summary()

# model <- lmer(otc_dom ~ generic. +generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
# model%>%summary()

# # -3 to 5
# model <- lmer(rx_dom ~ generic. +generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
# model%>%summary()

# model <- lmer(otc_dom ~ generic. +generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
# model%>%summary()
# # log
# model <- lmer(log(rx_dom+0.001) ~ generic. +generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+year+(1|id)-1, data=data)
# model%>%summary()

# model <- lmer(log(otc_dom+0.001) ~ generic. +generic.+elasped_m5+elasped_m4+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+elasped_6+elasped_7+elasped_8+elasped_9+elasped_10+(1|year)+(1|id)-1, data=data)
# model%>%summary()

# # -3 to 5
# model <- lmer(log(rx_dom+0.001) ~ generic. +generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
# model%>%summary()

# model <- lmer(log(otc_dom+0.001) ~ generic. +generic.+elasped_m3+elasped_m2+elasped_0+elasped_1+elasped_2+elasped_3+elasped_4+elasped_5+year+(1|id)-1, data=data)
# model%>%summary()