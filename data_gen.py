# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:03:12 2020

@author: JAE
"""

import torch
from torch.distributions import normal
import xlwings as xw


m = normal.Normal(torch.tensor([0.0]), torch.tensor([1.0]))

ten = torch.tensor([0.])

ll = []
for i in range(10000):
    ten += m.sample()
#    print(ten)
    ll.append([ten.item()])

#%%

wb = xw.Book()
ws = wb.sheets[0]


ws.range((1,1)).value = ll



#%%
