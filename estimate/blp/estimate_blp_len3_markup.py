import pandas as pd
import numpy as np
import statsmodels.api as sm
# from linearmodels.panel.data import PanelData
# from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects, compare
import matplotlib.pyplot as plt
import pyblp
import sys
import datetime
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def mute():
    sys.stdout = open('nul', 'w')
    # a=0
def unmute():
    sys.stdout = sys.__stdout__

drop_self,drop_nonself=0,0
opt=0
if len(sys.argv) > 2:
    drop_self = int(sys.argv[1])
    drop_nonself = int(sys.argv[2])
    print(f"Received parameters: param1={drop_self}, param2={drop_nonself}")
else:
    print("Insufficient parameters. Please provide two parameters.")
# Call the function with suppressed output
mute()
save=0

product_data=pd.read_csv("../../data/merged/len3_ndb_blp_DN_firm_FC.csv",encoding="utf-8",index_col=0)
print(product_data.columns[:30])
# rename
product_data=product_data.rename(columns={"薬価":"prices",
                    "同一剤形・規格の後発医薬品がある先発医薬品":"long_term",
                    "医薬品名":"product_ids",
                    "薬効分類":"TClass",
                    "メーカー名":"firm_ids"})

product_data["long_term"] = product_data["long_term"].replace("○", 1).fillna(0)
product_data.loc[product_data["firm_ids"]=="self","prices"]=product_data.loc[product_data["firm_ids"]=="self","mean_price"]*0.5
product_data.loc[product_data["firm_ids"]=="nonself","prices"]=product_data.loc[product_data["firm_ids"]=="nonself","mean_price"]*0.5*0.7
product_data = product_data[product_data["year"] > 2014]
product_data.loc[:,"market_ids"]=product_data.loc[:,"TClass"].astype(int).astype(str)+"-"+product_data.loc[:,"year"].astype(int).astype(str)
product_data.loc[:,"shares"]=product_data["総計"]/(120000000*100)
if drop_nonself:
    product_data = product_data[product_data["firm_ids"]!="nonself"]
if drop_self:
    product_data = product_data[product_data["firm_ids"]!="self"]



# drop which doesn't have generic
# product_data=product_data[~((product_data["long_term"]==0)&(product_data["generic"]==0))]
product_data=product_data.loc[product_data["shares"]>0]
# unmute()
# print(product_data.loc[product_data["markup"].isna(),["product_ids","firm_ids","prices","markup","year"]])
# print(set(product_data.loc[product_data["markup"].isna(),"year"]))
# mute()
product_data=product_data[["wholesale_price","markup","product_ids","market_ids","firm_ids","prices","brand","oral","generic","in_hospital","TClass","year","shares","id_l4","long_term","otc","Pharmacopoeia"]]
product_data=product_data.astype({"prices":float,"shares":float,"oral":float,"generic":int,"otc":int,"in_hospital":int,"long_term":int})
product_data.reset_index(drop=True,inplace=True)
unmute()
# print(product_data.corr())
# print(product_data.corr()>0.1)
mute()
# specify instruments
demand_instruments=pyblp.build_blp_instruments(pyblp.Formulation("1+generic+in_hospital+oral+long_term+Pharmacopoeia"),product_data=product_data)
# demand_instruments=pyblp.build_blp_instruments(formulation=pyblp.Formulation("1+prices+generic+oral+in_hospital"),product_data=product_data)
product_data_ids=product_data.loc[:,["shares","product_ids","market_ids","firm_ids","id_l4","year","TClass"]]
product_data_dm=product_data[["prices","markup","in_hospital","oral","generic","otc","long_term","Pharmacopoeia","TClass","year","firm_ids"]]
product_cols=product_data_dm.columns[:8]
absorb_formulation = pyblp.Formulation('prices+markup+in_hospital+oral+generic+otc+long_term+Pharmacopoeia', absorb='C(TClass)+C(year)+C(firm_ids)')
demeaned_product=pyblp.build_matrix(absorb_formulation,product_data_dm)
demeaned_product=pd.DataFrame(demeaned_product, columns=product_cols)
MD=demand_instruments.shape[1]
demand_instruments=pd.DataFrame(demand_instruments, columns=[f'demand_instruments{i}' for i in range(MD)])
# add exogenous = False

demand_instruments=pd.concat([demand_instruments,product_data.loc[:,["TClass","year","firm_ids"]]],axis=1)
instrument_names = ''.join([f'+demand_instruments{i}' for i in range(MD)])
absorb_formulation = pyblp.Formulation(instrument_names, absorb='C(TClass)+C(year)+C(firm_ids)')
demeaned_instruments=pyblp.build_matrix(absorb_formulation,demand_instruments)
demand_instruments=pd.DataFrame(demeaned_instruments, columns=[f'demand_instruments{i}' for i in range(MD)])
demand_instruments=pd.concat([demeaned_product.loc[:,["in_hospital","oral","generic","otc","long_term","Pharmacopoeia"]],demand_instruments],axis=1)
MD=demand_instruments.shape[1]
demand_instruments.columns = [f'demand_instruments{i}' for i in range(demand_instruments.shape[1])]
## if exogenous are also demeaned before
# product_data=pd.concat([demeaned_product,demand_instruments],axis=1)
# product_data=pd.concat([product_data,product_data_ids],axis=1)
## other wise
product_data=pd.concat([product_data,demand_instruments],axis=1)

unmute()
# print(product_data["firm_ids"].shape)
print(product_data["shares"].min(),product_data["shares"].max())
product_data[product_data["shares"]<=0]=1e-9
print(product_data["shares"].min(),product_data["shares"].max())
print(product_data.columns,MD)
# print(demand_instruments.columns)
# print(demand_instruments.isna().sum(),demand_instruments.shape) 
mute()
# print(product_data.corr().to_csv('correlation_matrix.csv', sep='\t'))
# print(product_data.corr()>0.1)
# lagged demand instruments
# demand_instrument_columns = [col for col in product_data.columns if col.startswith('demand_instrument')]
# def lag_demand_instruments(group):
#     for col in demand_instrument_columns:
#         for i in range(N_DI):  # 0から1までのラグを取得
#             lagged_column_name = f'demand_instruments{i+N_DI}'
#             group[lagged_column_name] = group[col].shift(1)
#     return group
# product_data=product_data.sort_values(['TClass', 'year'])
# product_data = product_data.groupby('id_l4').apply(lag_demand_instruments)
# product_data.shape

# product_data.loc[product_data["product_ids"]=="self"]["shares"]
# nesting
product_data["firm_ids"]=product_data["firm_ids"].astype(str)
product_data["market_ids"]=product_data["market_ids"].astype(str)
product_data["product_ids"]=product_data["product_ids"].astype(str)
product_data["nesting_ids"]=product_data["generic"].astype(str)+product_data["otc"].astype(str)
# logit_formulation= pyblp.Formulation('0+prices+markup+in_hospital+oral+generic+otc+long_term+Pharmacopoeia')
logit_formulation= pyblp.Formulation('prices+markup+in_hospital+oral+generic+otc+long_term+Pharmacopoeia',absorb="C(TClass)+C(year)+C(firm_ids)")
if drop_self and drop_nonself:
    logit_formulation= pyblp.Formulation('prices+markup+in_hospital+oral+generic+long_term+Pharmacopoeia', absorb='C(TClass)+C(year)+C(firm_ids)')
# logit_formulation= pyblp.Formulation('prices+oral+in_hospital+long_term', absorb='C(market_ids)+C(firm_ids)')

# typeで怒られがち
problem = pyblp.Problem(product_formulations=logit_formulation, product_data=product_data,add_exogenous=False)
# problem
optimization=pyblp.Optimization('l-bfgs-b')
logit_results = problem.solve(rho=0.7, optimization=optimization,rho_bounds=(0,1))

unmute()
print(logit_results)
mute()

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
cs=logit_results.compute_consumer_surpluses()
cs2=logit_results.compute_consumer_surpluses(eliminate_product_ids=["nonself"])
cs3=logit_results.compute_consumer_surpluses(eliminate_product_ids=["self"])
cs4=logit_results.compute_consumer_surpluses(eliminate_product_ids=["nonself","self"])
unmute()
print("logit")
print([np.mean(cs),np.mean(cs2),np.mean(cs3),np.mean(cs4)]/np.mean(cs))
print(sum(cs),sum(cs2),sum(cs3),sum(cs4))
print("delta",np.mean(logit_results.delta),np.sum(logit_results.delta))
mute()
if opt:
    instruments_results=logit_results.compute_optimal_instruments()
    instruments_results
    updated_problem=instruments_results.to_problem()
    updated_results=updated_problem.solve(rho=0.7,optimization=optimization,rho_bounds=(0,1))
    unmute()
    print(updated_results)
    mute()
    print(np.round(updated_results.beta.T/(1-updated_results.rho),4))
    costs = updated_results.compute_costs()
    # plt.hist(costs, bins=50)
    # plt.legend(["Marginal Costs"])
    # plt.show()
    markups = updated_results.compute_markups(costs=costs)
    # plt.hist(markups, bins=50)
    # plt.legend(["Markups"])

    cs=updated_results.compute_consumer_surpluses()
    cs2=updated_results.compute_consumer_surpluses(eliminate_product_ids=["nonself"])
    cs3=updated_results.compute_consumer_surpluses(eliminate_product_ids=["self"])
    cs4=updated_results.compute_consumer_surpluses(eliminate_product_ids=["nonself","self"])
    unmute()
    print("updated") 
    print([np.mean(cs),np.mean(cs2),np.mean(cs3),np.mean(cs4)]/np.mean(cs))
    print(sum(cs),sum(cs2),sum(cs3),sum(cs4))

    print("optimal delta",np.mean(updated_results.delta),"drop_self",drop_self,"drop_nonself",drop_nonself)
    mute()

    # # Get the current date and time
    # current_time = datetime.datetime.now()

    # # Format the time as a string
    # time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # if save:
    #     logit_results.to_pickle(f"./results/NL_len3_{time_string}_{drop_self}{drop_nonself}.pkl")
    # elasticities = logit_results.compute_elasticities()
    # # %matplotlib inline
    # import matplotlib.pyplot as plt
    # single_market = product_data['market_ids'] == '131-2015'
    # K=sum(single_market)
    # # plt.colorbar(plt.matshow(elasticities[single_market][:,:K]))
    # product_data[single_market].shape,K
    # elasticities[single_market][:,:K]
    # diversions = logit_results.compute_diversion_ratios()
    # plt.colorbar(plt.matshow(diversions[single_market][:,:K]))
