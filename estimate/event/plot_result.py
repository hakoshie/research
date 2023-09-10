import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel.data import PanelData
from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects, compare
import matplotlib.pyplot as plt
import seaborn as sns

def plot_result(result, start_from=1, period=17, insert_index=6, time_start=-7,ylim=(-1,1),plot_type="o-",file_name="result", title="Event Study Coefficients with Confidence Intervals",markersize=5):
    colors=sns.color_palette("husl", 4)
    summary_table = pd.DataFrame(result.summary.tables[1].data[start_from:start_from + period], columns=result.summary.tables[1].data[0])
    new_row = [0] * len(summary_table.columns)
    summary_table = pd.concat([summary_table.iloc[:insert_index], pd.DataFrame([new_row], columns=summary_table.columns), summary_table.iloc[insert_index:]]).reset_index(drop=True)

    summary_table["Time"] = np.array(list(range(time_start, period + time_start + 1)))
    summary_table = summary_table.apply(pd.to_numeric, errors='ignore')
    plt.figure(figsize=(10, 6))

    # Plot coefficients as points
    plt.plot(summary_table['Time'], summary_table["Parameter"], plot_type, label='Coefficients', color=colors[0],markersize=markersize)

    # Plot confidence intervals as error bars
    plt.fill_between(summary_table['Time'], summary_table['Lower CI'], summary_table['Upper CI'], color=colors[1], alpha=0.3, label='Confidence Intervals')

    # Separate the data for regression before and after insert_index
    pre_insert_data = summary_table[summary_table['Time'] <= insert_index+time_start]
    post_insert_data = summary_table[summary_table['Time'] > insert_index+time_start]

    # # Perform regression before and after insert_index
    # X_pre = sm.add_constant(pre_insert_data['Time'])
    # X_post = sm.add_constant(post_insert_data['Time'])
   
    # squared version
    # Perform regression before and after insert_index
    X_pre = sm.add_constant(np.array([pre_insert_data['Time'],np.array(pre_insert_data['Time'])**2]).transpose())
    X_post = sm.add_constant(np.array([post_insert_data['Time'],np.array(post_insert_data['Time'])**2]).transpose())

    # print(X_pre)                            
    model_pre = sm.OLS(pre_insert_data['Parameter'], X_pre).fit()
    model_post = sm.OLS(post_insert_data['Parameter'], X_post).fit()

    # Plot regression lines
    plt.plot(pre_insert_data['Time'], model_pre.predict(X_pre), '--', label='Regression Line (Before Event)', color=colors[2])
    plt.plot(post_insert_data['Time'], model_post.predict(X_post), '--', label='Regression Line (After Event)', color=colors[3])

    plt.xlabel('Time')
    plt.ylim(ylim)
    plt.ylabel("Parameter")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig("./plots/{}.png".format(file_name), dpi=300, bbox_inches="tight", transparent=False, facecolor="white")
    plt.show()