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

elecpump=pd.read_excel("Elec heat pump.xlsx")
elecpump2=elecpump.iloc[:12,:]

print (elecpump2)
print (elecpump2.columns)

#这个地方我们生成了第一幅图，energy cost(Elec heat pump)
#fig=px.bar(elecpump2,x="Month",y=["fans","heating","cooling"],title="Energy cost (Elec heat pump)").update_layout(
#    xaxis_title="Month", yaxis_title="Electricity Cost [J]")
#fig.show()

month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
month_ratio=[]
#for term in month_days:
#    month_ratio.append(term/365)
#print (month_ratio)
month_ratio=[0.08493150684931507, 0.07671232876712329, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507, 0.0821917808219178, 0.08493150684931507]

month_hours=[744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

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

month=elecpump2["Month"]
fans=elecpump2["fans"]
cooling=elecpump2["cooling"]
heating=elecpump2["heating"]

fans=fans/kwh_convert
cooling=cooling/kwh_convert
heating=heating/kwh_convert

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

cash_cost_elecpump={"Month":month,"supply_charge":part1_cost,
                "general charge fans":fans_general_charge,
                "general charge cooling":cooling_general_charge,
                "general charge heating":heating_general_charge,
                "Controlled load usage charge fans":part3_fans,
                "Controlled load usage charge heating":part3_heating,
                "Controlled load usage charge cooling":part3_cooling
                }

cash_cost_gree_elecpump=pd.DataFrame(cash_cost_elecpump)
#cash_cost_gree_elecpump.to_csv("Cash cost elecpump.csv")

cash_visualization_elecpump=pd.read_csv("Cash cost elecpump.csv")
"""
month_cash=cash_visualization_elecpump["Month"]
fans=cash_visualization_elecpump["fans"]
cooling=cash_visualization_elecpump["cooling"]
heating=cash_visualization_elecpump["heating"]
"""

fig=px.bar(cash_visualization_elecpump,x="Month",y=["fans","heating","cooling"],title="Cash cost (Elec heat pump)").update_layout(
    xaxis_title="Month", yaxis_title="Cash Cost [AUD]")
fig.show()
