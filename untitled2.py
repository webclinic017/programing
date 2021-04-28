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

def write_ws(df,pos=(1,1)):
    global wb,ws
    ws.range(pos).value =df
    
    
import datetime 
from dateutil.relativedelta import relativedelta

ss = '1900-12-01'
aa = datetime.datetime.strptime(ss,"%Y-%m-%d").date()
a2 = aa + relativedelta(months=1)

#%%

import yfinance as yf

tickers = yf.Tickers('msft aapl goog')
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
tickers.tickers.MSFT.info
tickers.tickers.AAPL.history(period="1mo")
tickers.tickers.GOOG.actions

#%%
    
init_xw()
#b_list = ['SHY','IEF','TLT','TIP','LQD','HYG','BWX','EMB']  #장기, 단기,중기,회사,하이일드,등등 채권 롤링
#b_list = ['VT','BCI','IAU','EDV','LTPZ','VCLT','VWOB']  #올웨더
#b_list = ['NQ=F','ZB=F','ZN=F','GC=F','SI=F','ES=F','ZT=F','EURUSD=X','JPY=X']  #선물
b_list = ['ES=F','YM=F','NQ=F','ZB=F','ZN=F','GC=F','SI=F','HG=F','CL=F']  #선물
#b_list = ['ZB=F','ZN=F','ZF=F','ZT=F']  #채권
#b_list = ['^GSPC','^IXIC','^DJI','^RUT','^TNX']  #지수



d_list = []
for b in b_list:
#    d0= yf.download(b,start='1900-01-01',end='2021-02-01')
    d0= yf.download(b,period="max")
    
    d0 = d0['Close']
    d0.name = b
    d_list.append(d0)


d1 = pd.concat(d_list,axis=1)
#d2=  d1
d2 = d1.dropna()


write_ws(d2)
#write_ws(d1)

#%%

from fredapi import Fred
#d_list = ['SP500','DGS10','DGS2','DGS3MO','UNRATE','PAYEMS','CPIAUCSL','T10Y2Y','M2','M1','MBM0UKM','WALCL','IOER','BAMLH0A0HYM2','T10YIE','GDPC1','FEDFUNDS','DFII10']
d_list = ['SP500','DGS10','DGS2','DGS3MO','UNRATE','PAYEMS','CPIAUCSL','T10Y2Y','M2','M1','MBM0UKM','WALCL','BAMLH0A0HYM2','T10YIE','GDPC1','FEDFUNDS','DFII10']
fred = Fred(api_key='1db5247a94c30ea7ab051cd5390c879c')
da=[]
for d in d_list:
    df = fred.get_series(d)
    df.name=d
    da.append(df)
    



#%%



a0 = da[0]
for d in da[1:]:
    a0 = pd.merge(a0,d, how='outer', left_index=True, right_index=True)    
write_ws(a0.iloc[-100:])
write_ws(da[1])

