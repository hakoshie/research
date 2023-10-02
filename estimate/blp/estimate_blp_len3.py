import pandas as pd
import numpy as np
import statsmodels.api as sm
# from linearmodels.panel.data import PanelData
# from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects, compare
import matplotlib.pyplot as plt
import pyblp
drop_self,drop_nonself=1,1
product_data=pd.read_csv("../../data/merged/len3_ndb_blp_DN_firm_FC.csv",encoding="utf-8",index_col=0)
print(product_data.columns[:30])
product_data=product_data.rename(columns={"薬価":"prices",
                    # "lag_mean_price":"demand_instruments0",
                    # "lag_sum_quantity":"demand_instruments1",
                    # "lag_generic_share_q":"demand_instruments2",
                    "同一剤形・規格の後発医薬品がある先発医薬品":"long_run"})
# "long_run"列の欠損値を0で埋める
product_data["long_run"].fillna(0, inplace=True)
# "long_run"列の"○"を1に置き換える
product_data["long_run"] = product_data["long_run"].replace("○", 1)
# product_data.loc[product_data["メーカー名"]=="sotc","prices"]=product_data.loc[product_data["メーカー名"]=="sotc","mean_price_g"]
# "year"列でフィルタリング
product_data = product_data[product_data["year"] > 2014]
if drop_nonself:
    product_data = product_data[product_data["メーカー名"]!="nonself"]
if drop_self:
    product_data = product_data[product_data["メーカー名"]!="self"]
product_data["product_ids"]=product_data["医薬品名"]
save=1
product_data.loc[:,"market_ids"]=product_data.loc[:,"薬効分類"].astype(int).astype(str)+"-"+product_data.loc[:,"year"].astype(int).astype(str)
product_data.loc[:,"firm_ids"]=product_data.loc[:,"メーカー名"].astype(str)
product_data.loc[:,"shares"]=product_data["総計"]/(120000000*100)


# drop which doesn't have generic
# product_data=product_data[~((product_data["long_run"]==0)&(product_data["generic"]==0))]
product_data=product_data.loc[product_data["shares"]>0]

product_data=product_data[["product_ids","market_ids","firm_ids","prices","brand","oral","generic","in_hospital","薬効分類","year","shares","id_l4","long_run","otc","Pharmacopoeia"]]
product_data=product_data.astype({"prices":float,"shares":float,"oral":float,"generic":int,"otc":int,"in_hospital":int,"long_run":int})
# product_data.loc[product_data["product_ids"]=='otc',"generic"]=0
product_data.reset_index(drop=True,inplace=True)
print(product_data.columns[:20])
print(product_data.shape)
# product_data["long_run"].value_counts()
# product_data["lag_sum_quantity"].isna().sum()
# product_data.shape

demand_instruments=pyblp.build_blp_instruments(pyblp.Formulation("1+generic+in_hospital+oral+long_run+Pharmacopoeia"),product_data=product_data)
# demand_instruments=pyblp.build_blp_instruments(formulation=pyblp.Formulation("1+prices+generic+oral+in_hospital"),product_data=product_data)
demand_instruments
demand_instruments.shape,product_data.shape
MD=demand_instruments.shape[1]
demand_instruments=pd.DataFrame(demand_instruments, columns=[f'demand_instruments{i}' for i in range(MD)])
product_data=pd.concat([product_data,demand_instruments],axis=1)
product_data.columns,product_data.shape
# lagged demand instruments
# demand_instrument_columns = [col for col in product_data.columns if col.startswith('demand_instrument')]
# def lag_demand_instruments(group):
#     for col in demand_instrument_columns:
#         for i in range(N_DI):  # 0から1までのラグを取得
#             lagged_column_name = f'demand_instruments{i+N_DI}'
#             group[lagged_column_name] = group[col].shift(1)
#     return group
# product_data=product_data.sort_values(['薬効分類', 'year'])
# product_data = product_data.groupby('id_l4').apply(lag_demand_instruments)
# product_data.shape

product_data.shape
product_data.columns[:30]
product_data.loc[product_data["product_ids"]=="self"]["shares"]
product_data["nesting_ids"]=product_data["in_hospital"].astype(int).astype(str)+product_data["otc"].astype(int).astype(str)
logit_formulation= pyblp.Formulation('prices+oral+in_hospital+generic+otc+long_run+Pharmacopoeia', absorb='C(market_ids)+C(firm_ids)')
if drop_self and drop_nonself:
    logit_formulation= pyblp.Formulation('prices+oral+in_hospital+generic+long_run+Pharmacopoeia', absorb='C(market_ids)+C(firm_ids)')
# logit_formulation= pyblp.Formulation('prices+oral+in_hospital+long_run', absorb='C(market_ids)+C(firm_ids)')
logit_formulation
# product_data["shares"]-=1e-10
# typeで怒られがち
problem = pyblp.Problem(product_formulations=logit_formulation, product_data=product_data)
# problem
optimization=pyblp.Optimization('bfgs')
logit_results = problem.solve(rho=0.7, optimization=optimization)
logit_results
# print(np.round(logit_results.beta.T/(1-logit_results.rho),4))
# print(np.round(logit_results.beta_se.T,6))
data = np.vstack((logit_results.beta.T/(1-logit_results.rho),
logit_results.beta_se.T))

# Find the maximum width for each column
max_widths = [max(len(f"{num:.4f}") for num in col) for col in zip(*data)]

# Format and print the aligned data
for row in data:
    formatted_row = [f"{num:.4f}".rjust(max_width) for num, max_width in zip(row, max_widths)]
    print(" ".join(formatted_row))
instruments_results=logit_results.compute_optimal_instruments()
instruments_results
updated_problem=instruments_results.to_problem()
updated_results=updated_problem.solve(rho=0.7,optimization=optimization)
updated_results
print(np.round(updated_results.beta.T/(1-updated_results.rho),4))
costs = updated_results.compute_costs()
plt.hist(costs, bins=50)
plt.legend(["Marginal Costs"])
# plt.show()
markups = updated_results.compute_markups(costs=costs)
plt.hist(markups, bins=50)
plt.legend(["Markups"])
cs=updated_results.compute_consumer_surpluses()
sum(cs),np.mean(cs)
cs2=updated_results.compute_consumer_surpluses(eliminate_product_ids=["nonself"])
cs3=updated_results.compute_consumer_surpluses(eliminate_product_ids=["self"])
cs4=updated_results.compute_consumer_surpluses(eliminate_product_ids=["nonself","self"])
print([np.mean(cs),np.mean(cs2),np.mean(cs3),np.mean(cs4)]/np.mean(cs))
print(sum(cs),sum(cs2),sum(cs3),sum(cs4))
np.mean(updated_results.delta)
import datetime

# Get the current date and time
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
if save:
    logit_results.to_pickle(f"./results/NL_len3_{time_string}_{drop_self}{drop_nonself}.pkl")
elasticities = logit_results.compute_elasticities()
# %matplotlib inline
import matplotlib.pyplot as plt
single_market = product_data['market_ids'] == '131-2015'
K=sum(single_market)
# plt.colorbar(plt.matshow(elasticities[single_market][:,:K]))
product_data[single_market].shape,K
elasticities[single_market][:,:K]
diversions = logit_results.compute_diversion_ratios()
# plt.colorbar(plt.matshow(diversions[single_market][:,:K]))
