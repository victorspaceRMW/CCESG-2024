# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:38:01 2023

@author: z5252229
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly
import plotly_express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'

import sys

#from gree.py import month_days

month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
month_ratio=[]
#for term in month_days:
#    month_ratio.append(term/365)
#print (month_ratio)
month_ratio=[0.08493150684931507, 0.07671232876712329, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507]

month_hours=[744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

global kwh_convert
kwh_convert=3600000

furnace=pd.read_excel("Mixed chart.xlsx")
print (furnace.columns)

month=furnace["Month"]

months = list(furnace["Month"])

print (furnace)
gas_cost=furnace["heating (gas)"]
gas_cost=gas_cost/1000000

fans=furnace["fans (Electricity)"]
fans=fans/kwh_convert

print (gas_cost)

"""
#在这里我们画第一幅图
fig = go.Figure()
fig.add_trace(go.Bar(
    x=months,
    y=list(furnace["fans (Electricity)"]),
    # base另一种写法：np.array([2000, 3000, 5000]) * (-1)
    base=0,  # 基准设置
    marker_color='crimson',
    name='Electricity Energy Consumption'))
fig.add_trace(go.Bar(
    x=months,
    y=list(furnace["inverse_heating (gas)"]),
    base=0,  # 默认基准设置
    marker_color='lightslategrey',
    name='Gas Energy Consumption'
))
fig.update_layout(
    xaxis_title="Month", yaxis_title="Energy Cost [J]",title="We count both the energy consumption by Joule")
fig.show()
"""

#我们首先计算电价
###采用1st Energy的电价模型，假设Ausgrid为distributor，去计算电价
###
###在这个round里，我们先不考虑光伏的问题
###电价模型可以分为三个部分：
# 1. Supply Charge, 238.7/c per day
# 2. General Usage Charge:
    
#40.04c per kWh
#for the first 20kWh used per day
#44.11c per kWh
#for usage over 20kWh per day

# 3. Controlled load usage charge

# 17.49c per kwh
# 5.5c per day

#首先计算入户费
part1_cost=[]
for term in month_days:
    part1_cost.append((term*238.7)/100)
print (part1_cost)

#然后计算general charge
#General charge, fans:
fans_general_charge=[]
for term in list(fans):
    fans_general_charge.append((term*40.04)/100)
print (fans_general_charge)

count_by_day_cost=[]
for term in month_days:
    count_by_day_cost.append((term*5.5)/100)
#print (count_by_day_cost)

#fan charge
count_by_kwh_fans_general_charge=[]
for term in list(fans):
    count_by_kwh_fans_general_charge.append((term*17.49)/100)
#print (count_by_kwh_fans_general_charge)
part3_fans=[x + y for x, y in zip(count_by_day_cost, count_by_kwh_fans_general_charge)]
print (part3_fans)

overall_cost_electricity=[x+y+z for x,y,z in zip(part1_cost,fans_general_charge,part3_fans)]
print (overall_cost_electricity)


#之后我们计算燃气的费用
#在这里我们采用AGL公司的燃气费用标准

#5.01c per MJ
#for the first 20.71MJ used per day
#4.08c per MJ
#for usage between 20.71-41.1MJ per day
#4.01c per MJ
#for usage between 41.1-90.41MJ per day
#3.89c per MJ
#for usage between 90.41-2745.2MJ per day
#3.72c per MJ
#for usage between 2745.2-13709.59MJ per day
#3.44c per MJ
#for usage over 13709.59MJ per day

print (gas_cost)
l1=20.71
l2=41.1
l3=90.41
l4=2745.2

price0=5.01/100
price1=4.08/100
price2=4.01/100
price3=3.89/100
price4=3.72/100
price5=3.44/100

list_l1=[term*l1 for term in month_days]
#print (list_l1)
list_l2=[term*l2 for term in month_days]
list_l3=[term*l3 for term in month_days]
list_l4=[term*l4 for term in month_days]
#print (list_l4)

bar_gas_cost={"gas_cost":gas_cost,
              "level1":list_l1,
              "level2":list_l2,
              "level3":list_l3,
              "level4":list_l4
    }
bar_gas_cost_df=pd.DataFrame(bar_gas_cost)
print (bar_gas_cost_df)

gas_cash_list=[]

for index,row in bar_gas_cost_df.iterrows():
    print (list(row))
    sub_list=list(row)
    if (sub_list[0]<sub_list[1]):
        gas_cash=sub_list[0]*price0 
    elif (sub_list[1]<sub_list[0] and sub_list[0]<sub_list[2]):
        gas_cash=sub_list[1]*price0+(sub_list[0]-sub_list[1])*price1 
    elif (sub_list[2]<sub_list[0]<sub_list[3]):
        gas_cash=sub_list[1]*price0+(sub_list[2]-sub_list[1])*price1+(sub_list[0]-sub_list[2])*price2
    elif (sub_list[3]<sub_list[0]<sub_list[4]):
        gas_cash=sub_list[1]*price0+(sub_list[2]-sub_list[1])*price1+(sub_list[3]-sub_list[2])*price2+(sub_list[0]-sub_list[3])*price3
    gas_cash_list.append(gas_cash)
print (gas_cash_list)

df_furnace_cost=pd.DataFrame({"Month":month,"elec_cash":overall_cost_electricity,
                 "gas_cash":gas_cash_list})
df_furnace_cost.to_csv("furnace_cost")

fig = px.bar(df_furnace_cost,
            x="Month",
            y=["elec_cash","gas_cash"],title="The Cash cost of furnace(Only for heating)")
fig.show()
