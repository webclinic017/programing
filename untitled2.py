# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:28:54 2020

@author: JAE
"""
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
#    fname ="./test.xlsx"
    try: 
        wb = xw.books.active
    except:
        wb = xw.Book()
    
#    wb = xw.Book()
#    wb = xw.Book(fname)
    ws = wb.sheets[0]

def add_ws(name ='ws'):
    global wb,ws
    wb.sheets.add()
    ws = wb.sheets[0]
    ws.name=name

def write_ws(df):
    global wb,ws
    ws.range((1,1)).value =df
    
    
#%%
    
init_xw()
#b_list = ['SHY','IEF','TLT','TIP','LQD','HYG','BWX','EMB']  #장기, 단기,중기,회사,하이일드,등등 채권 롤링
#b_list = ['VT','BCI','IAU','EDV','LTPZ','VCLT','VWOB']  #올웨더
#b_list = ['NQ=F','ZB=F','ZN=F','GC=F','SI=F','=F','ES=F','ZT=F','EURUSD=X','JPY=X']  #선물
b_list = ['ZB=F','ZN=F','ZF=F','ZT=F']  #채권
#b_list = ['^GSPC','^IXIC']  #지수



d_list = []
for b in b_list:
    t = yf.Ticker(b)
    d0 = t.history(period='max')
    d0 = d0['Close']
    d0.name = b
    d_list.append(d0)


d1 = pd.concat(d_list,axis=1)
d2=  d1
#d2 = d1.dropna()


write_ws(d2)
