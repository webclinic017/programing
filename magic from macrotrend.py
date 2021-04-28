# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:06:20 2021

@author: JAE
"""

import requests
from bs4 import BeautifulSoup
import json
import pprint
import pandas as pd
import yfinance as yf
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

import xlwings as xw
wb = False
ws = False

def init_xw():
    global wb,ws
    fname ="./test.xlsx"
    wb = xw.Book(fname)
    ws = wb.sheets[0]

def add_ws(name ='ws'):
    global wb,ws
    wb.sheets.add()
    ws = wb.sheets[0]
    ws.name=name

def write_ws(df):
    global wb,ws
    ws.range((1,1)).value =df
    
types = ['income-statement?freq='
    ,'balance-sheet?freq='
    ,'cash-flow-statement?freq='
    ,'financial-ratios?freq='
    ]
    


def get_d0(name="O",freq="Q",types='cash-flow-statement?freq='):
    if freq !='A' and freq !='Q':
        print('freq must be A , Q')
        return 0
    
    tt = types

    url = requests.get('https://www.macrotrends.net/stocks/charts/'+name)
    
    res = requests.get(url.url+'/'+tt+freq)
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    rr0 = soup.find_all('script')
    rr1 = str(rr0)
    org = rr1.find('originalData')
    start = rr1.find('[',org)
    end = rr1.find(']',start)
    rr2 = rr1[start:end+1]

    df = pd.read_json(rr2)
    df = df.sort_index(axis=1,ascending=False)
    
    for i,row in df.iterrows():
        string=df.loc[:,'field_name'][i]
        soup=BeautifulSoup(string,'html.parser')
        df.loc[:,'field_name'][i] = soup.string
        
#        string=df.loc[:,'popup_icon'][i]
#        a0=string.find('t:')
#        a1=string.find(',',a0)
#        a2=string.find('freq:',a1)
#        a3=string.find(',',a2)
#        txt=string[a0:a1]+','+string[a2:a3]
#        df.loc[:,'popup_icon'][i] = txt
#    aa=df.apply(lambda x : x['popup_icon'].__len__() < POPUP_ICON_CROP_LENGTH, axis=1)
#    df2=df.drop(aa[aa==True].index)
    df = df.drop('popup_icon',1)
    return df
    

#aa= get_d0('O','Q',types[2])
#aa= get_d0('O','A',types[2])
#init_xw()
#write_ws(aa)

    
def get_d1(name="O",freq="Q"):
    df_list = []
    for tt in types:
        df_list.append(get_d0(name,freq,tt))
    return pd.concat(df_list)




#aa = get_d1('O','Q')
#
#write_ws(aa)



    

#%%



#%%


import pandas as pd
import yfinance as yf
import numpy as np

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


#신 마법 공식   저 PBR, 고 GP/A 
df = pd.read_csv('IWV_holdings.csv')
tickers = df.Ticker
maxsize = len(tickers)
tickers = df.Ticker.iloc[0:maxsize]

target_month = ['2020-11-01','2021-02-01'] #포함 범위.

mem = []
for ii, tick in enumerate(tickers): 
    gp_a=np.nan
    pbr= np.nan
    try: 
        dd0 = get_d1(tick,'Q')
        dd0=dd0.set_index('field_name')
    
        yy = yf.Ticker(tick)
        pri = yy.history(period='1d')
        price = pri['Close'].iloc[0]

                
        aa0 = dd0.columns > target_month[0]
        aa1 = dd0.columns < target_month[1]
        flag = dd0.columns[ aa0&aa1]
        
        gp = dd0[dd0.index =='Gross Profit'][flag].iloc[0,0]
        ass = dd0[dd0.index =='Total Assets'][flag].iloc[0,0]
        
        bps = dd0[dd0.index =='Book Value Per Share'][flag].iloc[0,0]
        
#        book = dd0[dd0.index =='Share Holder Equity'][flag].iloc[0,0]
        
        
        
        pbr = price/float(bps)
        
        
        gp_a = float(gp)/float(ass)
        
    except Exception as e:
        print(e)
    mem.append([tick,gp_a,pbr])
    print(tick,'\t', ii,'/',len(tickers),'\t',gp_a,pbr)

df1 = pd.DataFrame(mem)
df1.columns=['TICK','GP/A','PBR']
df1.to_csv('./aaa_trend.csv')

df1['GP/A rank'] = df1['GP/A'].rank(method='average', ascending=False) #high GP/A
df1['PBR rank'] = df1['PBR'].rank(method='average', ascending=True) #low PBR
df1['magic rank'] = df1['PBR rank']+df1['GP/A rank']

df1 = df1.sort_values('magic rank')

