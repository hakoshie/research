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
# warnings.filterwarnings("ignore")


def mute():
    sys.stdout = open('nul', 'w')
    # a=0
def unmute():
    sys.stdout = sys.__stdout__

drop_self,drop_nonself=0,0
if len(sys.argv) > 2:
    drop_self = int(sys.argv[1])
    drop_nonself = int(sys.argv[2])
    print(f"Received parameters: param1={drop_self}, param2={drop_nonself}")
else:
    print("Insufficient parameters. Please provide two parameters.")
# Call the function with suppressed output
# mute()
save=1

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

product_data["prices"]=product_data["prices"]*3.4
product_data=product_data.loc[product_data["shares"]>0]
product_data=product_data[["wholesale_price","markup","product_ids","market_ids","firm_ids","prices","brand","oral","generic","in_hospital","TClass","year","shares","id_l4","long_term","otc","Pharmacopoeia"]]
product_data=product_data.astype({"prices":float,"shares":float,"oral":float,"generic":int,"otc":int,"in_hospital":int,"long_term":int})
product_data.reset_index(drop=True,inplace=True)
# specify instruments
demand_instruments=pyblp.build_blp_instruments(pyblp.Formulation("1+generic+in_hospital+oral+long_term+Pharmacopoeia"),product_data=product_data)
# demand_instruments=pyblp.build_blp_instruments(formulation=pyblp.Formulation("1+prices+generic+oral+in_hospital"),product_data=product_data)

MD=demand_instruments.shape[1]
demand_instruments=pd.DataFrame(demand_instruments, columns=[f'demand_instruments{i}' for i in range(MD)])
product_data=pd.concat([product_data,demand_instruments],axis=1)
# unmute()
# print(product_data.corr().to_csv('correlation_matrix.csv', sep='\t'))
# print(product_data.corr()>0.1)
# mute()
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

product_data.loc[product_data["product_ids"]=="self"]["shares"]
# nesting
product_data["nesting_ids"]=product_data["generic"].astype(str)+product_data["otc"].astype(str)
X1_formulation= pyblp.Formulation('prices+in_hospital+oral+generic+otc+long_term+Pharmacopoeia', absorb='C(TClass)+C(year)+C(firm_ids)')
if drop_self and drop_nonself:
    X1_formulation= pyblp.Formulation('prices+in_hospital+oral+generic+long_term+Pharmacopoeia', absorb='C(TClass)+C(year)+C(firm_ids)')
# logit_formulation= pyblp.Formulation('prices+oral+in_hospital+long_term', absorb='C(market_ids)+C(firm_ids)')
X2_formulation=pyblp.Formulation("-1+I(-prices)")
agent_num=200
N=product_data.shape[0]
values=[.3,.1]
probs=[.6,.4]
agent_data=pd.DataFrame(np.random.choice(values, size=(N*agent_num, 1), p=probs))

agent_data["market_ids"]=product_data["market_ids"].repeat(agent_num).reset_index(drop=True)

product_formulations=(X1_formulation,X2_formulation)

# product_data=product_data.loc[product_data["year"]==2015]
N=product_data.shape[0]
product_formulations = (X1_formulation, X2_formulation)
agent_formulation = pyblp.Formulation('-1+I(-burden)')
agent_formulation=pyblp.Formulation('-1')



# optim = pyblp.Optimization('nelder-mead',compute_gradient=False)
# optim = pyblp.Optimization('slsqp')

product_data["shares"].min()
agent_num=200
N=product_data.shape[0]
values=[.3,.1]
probs=[.6,.4]
agent_data=pd.DataFrame({"burden":np.random.choice(values, size=(N*agent_num, 1), p=probs).flatten()})

agent_data["market_ids"]=product_data["market_ids"].repeat(agent_num).reset_index(drop=True)
agent_data
mc_integration = pyblp.Integration('halton', size=agent_num, specification_options={'seed': 0})
mc_integration
# mc_problem = pyblp.Problem(product_formulations, product_data ,agent_formulation,agent_data,integration=mc_integration,rc_types=["log","linear"])
mc_problem = pyblp.Problem(product_formulations, product_data ,agent_formulation,agent_data,integration=mc_integration,rc_types=["linear"])
mc_problem
optim = pyblp.Optimization('l-bfgs-b',{'gtol': 1e-4})
# optim = pyblp.Optimization('nelder-mead',compute_gradient=False)
# optim = pyblp.Optimization('slsqp')
lb=-10
ub=10
# results1 = mc_problem.solve(sigma=np.eye(2),pi=[[1],[0]],sigma_bounds = [((lb, lb), (lb, lb)),
#                ((ub, ub), (ub, ub))],pi_bounds=((0,0),(10,10)),optimization=optim)
# in case of agent data exists
# results1 = mc_problem.solve(sigma=np.eye(2),pi=[[1],[0]],sigma_bounds = (((0,0),(0,None)),((None,None),(None,None))) ,pi_bounds=((0,None),(None,None)),optimization=optim)
# without agent data
# unmute()
n_beta=7
results1 = mc_problem.solve(rho=0.7,sigma=[1],beta_bounds=([lb]*7,[ub]*7),pi=1,pi_bounds=(0,None),sigma_bounds = (0,None) ,optimization=optim)
# results1
# mute()
cs=results1.compute_consumer_surpluses()
cs2=results1.compute_consumer_surpluses(eliminate_product_ids=["self"])
cs3=results1.compute_consumer_surpluses(eliminate_product_ids=["nonself"])
cs4=results1.compute_consumer_surpluses(eliminate_product_ids=["nonself","self"])
# unmute()
print("consumer surplus")
print([np.mean(cs),np.mean(cs2),np.mean(cs3),np.mean(cs4)]/np.mean(cs))
sum(cs),sum(cs2),sum(cs3),sum(cs4)
import datetime

# Get the current date and time
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
# save=1
if save:
    results1.to_pickle(f"./results/RCNL_len3_{time_string}.pkl")
# pr_integration = pyblp.Integration('product', size=5)
# # pr_problem = pyblp.Problem(product_formulations, product_data,agent_formulation,agent_data,integration=pr_integration,rc_types=["log","linear"])
# pr_problem = pyblp.Problem(product_formulations, product_data,agent_formulation,agent_data,integration=pr_integration,rc_types=["log","linear"])
# optim = pyblp.Optimization('bfgs',{'gtol': 1e-4})
# # with pyblp.parallel(3):
# results2 = pr_problem.solve(sigma=np.eye(2),pi=[[1],[1]], optimization=optim)
# results2

