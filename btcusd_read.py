# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 18:42:47 2021

@author: JAE
"""

import pandas as pd
import os
import math
import numpy as np 

path = './BTCUSD/'
d0 = os.listdir(path)
d1 = [path+d for d in d0]

dd = d1[0:3]

def read_dlist(dd):
    r = []
    for d in dd:
        r.append(pd.read_csv(d)[::-1])
    r = pd.concat(r).reset_index(drop=True)
    return r


aa = read_dlist(dd)
aa = aa.iloc[:,:5]

aa['timestamp'] = aa['timestamp'].apply(np.ceil)
aa['side'] = aa['side'].replace('Buy','1')
aa['side'] = aa['side'].replace('Sell','-1')
aa['side'] = aa['side'].astype(float)

aa['size'] = aa['side']*aa['size']


def fagg(row):
    if row.name=='size':
        return row.sum()
    if row.name=='price':
        return row.mean()
    
aa = aa.groupby(['timestamp']).agg(fagg)
aa = aa.drop(columns='symbol')
aa = aa.drop(columns='side')










