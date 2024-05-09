# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 12:45:26 2023

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

global kwh_convert

kwh_convert=3600000

gree=pd.read_excel("Gree, Electricity.xlsx")
gree2=gree.iloc[:12,:]

print (gree2)
print (gree2.columns)

###首先我们计算非空调，电炉子的家用电器的耗电量
month=gree2["Month"]
month2=month
light=gree2["light"]
appliance=gree2["appliance (Besides air conditioner and furnace)"]

fans=gree2["fans"]
cooling=gree2["cooling"]
heating=gree2["heating"]

###这个地方我们生成了第一幅图，energy cost(light and appliance)
#fig=px.bar(gree2,x="Month",y=["light","appliance (Besides air conditioner and furnace)"],title="Energy cost (Only light and appliance)").update_layout(
#    xaxis_title="Month", yaxis_title="Electricity Cost [J]")
#fig.show()

###这个地方我们生成了第二幅图，energy cost(Gree air conditioner)
#fig=px.bar(gree2,x="Month",y=["fans","heating","cooling"],title="Energy cost (Gree Air Conditioner)").update_layout(
#    xaxis_title="Month", yaxis_title="Electricity Cost [J]")
#fig.show()

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

month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
month_ratio=[]
#for term in month_days:
#    month_ratio.append(term/365)
#print (month_ratio)
month_ratio=[0.08493150684931507, 0.07671232876712329, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507]

month_hours=[744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
cheap_electricity_limit_part2=[]
#for term in month_days:
#    cheap_electricity_limit_part2.append(term*24*20)
#print (cheap_electricity_limit_part2)
cheap_electricity_limit_part2=[14880, 13440, 14880, 14400, 14880, 14400, 14880, 14880, 14400, 14880, 14400, 14880]

"""
第一部分：计算supply charge
"""
month=[i for i in range(1,13)]

supply_charge=365*238.7/100
#print ("supply_charge",supply_charge)
supply_charge_month=[]
for term in month_ratio:
    supply_charge_month.append(term*supply_charge)
#print ("supply_charge_month",supply_charge_month)

"""
第二部分：计算General Usage charge
"""

#Turning J into kwh, and computing 
#print (light)
light=light/kwh_convert
#print (light)

light_cost=(light*40.04)/100
#print ("light_cost",light_cost)

#print (appliance)
appliance=appliance/kwh_convert
#print (appliance)

appliance_cost=(appliance*40.04)/100
#print ("appliance_cost",appliance_cost)

#显然，灯和电器（空调，炉子以外）的耗电量远低于高价警戒线

"""
第三部分：计算Load Usage charge
"""
light_sum=sum(light)
#print (light_sum)
money_light=(17.49*light_sum)/100+(365*5.5)/100
#print ("money_light:",money_light)

money_light_month=[]
for term in month_ratio:
    money_light_month.append(term*money_light)
#print ("money_light_month:",money_light_month)

appliance_sum=sum(appliance)
#print (appliance_sum)
money_appliance=(17.49*appliance_sum)/100+(365*5.5)/100
#print ("money_appliance:",money_appliance)

appliance_light_month=[]
for term in month_ratio:
    appliance_light_month.append(term*money_appliance)
#print ("money_light_appliance:",appliance_light_month)

#print (month)

cash_cost={"Month":month2,"supply charge":supply_charge_month,
           "light, general usage cost":light_cost, "appliance, general usage cost":light_cost,
           "light, load_usage_charge":money_light_month,"appliance, load_usage_charge":appliance_light_month}

cash_cost_df=pd.DataFrame(cash_cost)
print (cash_cost_df.columns)

"""
fig = px.bar(cash_cost_df,
            x=month,
            y=['supply charge', 
                   'light, general usage cost', 'appliance, general usage cost',
                   'light, load_usage_charge', 'appliance, load_usage_charge'],
            title="Energy Cash-cost on non-air conditioner household equipments").update_layout(yaxis_title="Electricity Cost [AUD]")
fig.update_xaxes(
    type='linear',
    side='bottom',
    showgrid=False,
    zeroline=True,
    automargin=True,
)
                              
fig.show()
"""

"""
第四部分， 可视化 fans,heating和cooling的能耗
"""
fans=fans/kwh_convert
cooling=cooling/kwh_convert
heating=heating/kwh_convert

#在这个地方我们画出第五幅图
#fig=px.bar(gree2,x="Month",y=["fans","heating","cooling"],title="Energy cost (Air conditioner and furnace)").update_layout(
#    xaxis_title="Month", yaxis_title="Electricity Cost [J]")
#fig.show()

"""
第五部分：计算每个月每种情况需要耗费多少电能
"""
print (fans)
print (heating)
print (cooling)

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

#General charge, heating:
heating_general_charge=[]
for term in list(heating):
    heating_general_charge.append((term*40.04)/100)
print (heating_general_charge)

#General charge, cooling:
cooling_general_charge=[]
for term in list(cooling):
    cooling_general_charge.append((term*40.04)/100)
print (cooling_general_charge)

#最后计算日费
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

#heating charge
count_by_kwh_heating_general_charge=[]
for term in list(heating):
    count_by_kwh_heating_general_charge.append((term*17.49)/100)
#print (count_by_kwh_heating_general_charge)
part3_heating=[x + y for x, y in zip(count_by_day_cost, count_by_kwh_heating_general_charge)]
print (part3_heating)

#cooling charge
count_by_kwh_cooling_general_charge=[]
for term in list(cooling):
    count_by_kwh_cooling_general_charge.append((term*17.49)/100)
#print (count_by_kwh_cooling_general_charge)
part3_cooling=[x + y for x, y in zip(count_by_day_cost, count_by_kwh_cooling_general_charge)]
print (part3_cooling)

cash_cost_gree={"Month":month2,"supply_charge":part1_cost,
                "general charge fans":fans_general_charge,
                "general charge cooling":cooling_general_charge,
                "general charge heating":heating_general_charge,
                "Controlled load usage charge fans":part3_fans,
                "Controlled load usage charge heating":part3_heating,
                "Controlled load usage charge cooling":part3_cooling
                }

cash_cost_gree_df=pd.DataFrame(cash_cost_gree)
#cash_cost_gree_df.to_csv("Cash cost gree.csv")

cash_visualization_gree=pd.read_csv("Cash cost gree.csv")
month_cash=cash_visualization_gree["Month"]
fans=cash_visualization_gree["fans"]
cooling=cash_visualization_gree["cooling"]
heating=cash_visualization_gree["heating"]

fig=px.bar(cash_visualization_gree,x="Month",y=["fans","heating","cooling"],title="Cash cost (Gree)").update_layout(
    xaxis_title="Month", yaxis_title="Cash Cost [AUD]")
fig.show()

