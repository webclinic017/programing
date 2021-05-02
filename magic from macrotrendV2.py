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

import numpy as np
from datetime import datetime
from dateutil.relativedelta import *
import time




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
    if freq !='A' and freq !='Q':
        print('freq must be A , Q')
        return 0
    
    url = requests.get('https://www.macrotrends.net/stocks/charts/'+name)
    
    df_list = []
    for tt in types:
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
        df_list.append(df)
    return pd.concat(df_list)




def save_d1(path='./data', name="O",freq='Q'):
    ret = get_d1(name,freq)
    ret.to_csv('{}/{}.csv'.format(path,name),index=False)
    

def get_russell_balsheet():
    df = pd.read_csv('IWV_holdings.csv')
    tickers = df.Ticker
    maxsize = len(tickers)
    tickers = df.Ticker.iloc[0:maxsize]
    for ii, tick in enumerate(tickers): 
        try:
            print(ii,tick,' save.... ')
            save_d1(name=tick)
        except Exception as e:
            print(e)
            

get_russell_balsheet()

import os



def read_ticker(path='./data'):
    ff= os.listdir(path)
    nff = [aa.replace('.csv','') for aa in ff]
    return nff

vtick = read_ticker()

def read_db(path='./data',tick='aapl'):
    df1 = pd.read_csv('{}/{}.csv'.format(path,tick))
    
    return df1.set_index('field_name')


def find_df(df,name='Gross Profit'):
    return df[df.index ==name]
    

def read_db2(path='./data',tick='aapl',date):
    df = read_db(tick=tick)
    flag = df.columns[ df.columns < now]
    return df[flag]
    
    
tt = vtick[0]
df = read_db(tick=tt)
now = datetime.now().date().strftime('%Y-%m-%d')

df = read_db2(tick=tt,date=now)



        
        
        gp = dd0[dd0.index =='Gross Profit'][flag].iloc[0,0]
        ass = dd0[dd0.index =='Total Assets'][flag].iloc[0,0]
        
        
df[]
aa = find_df(df)
aa.iloc[0,0]

#%%



#%%


import pandas as pd



def get_momentum(tick , months=[1,3,6,12],margin_day=7):
#    tick ='AAPL'
#    months=[1,3,6,12]
#    margin_day=7
    
    now = datetime.now().date()
    now2 = (now-relativedelta(days=margin_day))
    
    
    vv = yf.download(tick , start=now2, end=now,progress=False)
    latest_price = vv['Close'][-1] #최근 가격
    
    mm_list = []
    
    for mo in months:
        m1 = (now2-relativedelta(months=mo))
        m2 = (now-relativedelta(months=mo))
    
        vv2 = yf.download(tick , start=m1, end=m2,progress=False)
        mm_list.append(vv2['Close'].mean())  #종가 평균.
    return latest_price/mm_list


pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


#신 마법 공식   저 PBR, 고 GP/A 
df = pd.read_csv('IWV_holdings.csv')
tickers = df.Ticker
maxsize = len(tickers)
maxsize = 1000
tickers = df.Ticker.iloc[0:maxsize]

target_month = ['2020-11-01','2021-02-01'] #포함 범위.


start_time = time.time()


mem = []
for ii, tick in enumerate(tickers): 
    gp_a=np.nan
    pbr= np.nan
    per= np.nan
    psr= np.nan
    ret= pd.DataFrame([0])
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
        
        ret = get_momentum(tick)
        
        eps = float(dd0[dd0.index =='EPS - Earnings Per Share'][flag].iloc[0,0])
        reve = float(dd0[dd0.index =='Revenue'][flag].iloc[0,0])
        shar = float(dd0[dd0.index =='Shares Outstanding'][flag].iloc[0,0])
        neti = float(dd0[dd0.index =='Net Income'][flag].iloc[0,0])
        
        per = price/eps
        psr = price/(reve/shar)
        
        
        
    except Exception as e:
        print(e)
    aa= [tick,gp_a,pbr,per,psr,ret.mean()]
    aa.extend(ret)
    mem.append(aa)
    print(aa[0],'\t', ii,'/',len(tickers),'\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f '%(aa[1],aa[2],aa[3],aa[4],aa[5]))

df1 = pd.DataFrame(mem)
df1.columns=['TICK','GP/A','PBR','PER','PSR','MOM_avg','1M','3M','6M','12M']
df1.to_csv('./aaa_trend.csv')

print('end time:',time.time()-start_time)

df1 = pd.read_csv('./aaa_trend.csv')

df1['GP/A rank'] = df1['GP/A'].rank(method='average', ascending=False) #high GP/A
df1['PBR rank'] = df1['PBR'].rank(method='average', ascending=True) #low PBR
#df1['PER rank'] = df1['PER'].rank(method='average', ascending=False) #low PBR
df1['PSR rank'] = df1['PSR'].rank(method='average', ascending=False) #low PBR

df1['magic rank'] = (df1['PBR rank']+df1['GP/A rank']+df1['PSR rank'])

df1 = df1.sort_values('magic rank')
df1.to_csv('./magic_out.csv')
