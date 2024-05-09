# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:03:43 2023

@author: z5252229
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly_express as px
import plotly.graph_objects as go

data=pd.read_excel("cash cost.xlsx")
print (data)
elec=sum(data["Elec pump"])
GEHP=sum(data["GEHP"])
Gree=sum(data["Gree"])
gas=sum(data["Gas furnace"])

sizes=[elec,GEHP,Gree,gas]
labels=["Electrical Heat Pump","GEHP","Gree Air conditioner","Gas Furnace"]
explode = (0, 0.1, 0, 0)
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.show()

#month=data["Month"]
"""
fig = px.bar(data,
             x="Month",
             y=["Elec pump","GEHP","Gree","Gas furnace"],
             barmode="group"  # ['stack', 'group', 'overlay', 'relative']
            )
fig.update_layout(
    xaxis_title="Month", yaxis_title="Energy Cost [Joule]")

fig.show()
"""