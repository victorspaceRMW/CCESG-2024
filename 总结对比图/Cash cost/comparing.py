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
#print (data)

#month=data["Month"]
fig = px.bar(data,
             x="Month",
             y=["Elec pump","GEHP","Gree","Gas furnace"],
             barmode="group"  # ['stack', 'group', 'overlay', 'relative']
            )
fig.update_layout(
    xaxis_title="Month", yaxis_title="Cash cost [AUD]")

fig.show()