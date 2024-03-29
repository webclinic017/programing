# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 20:27:45 2021

@author: JAE
"""

import pandas as pd
import yfinance as yf

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


#%%

import yfinance as yf

tickers = yf.Tickers('msft aapl goog')
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
tickers.tickers.MSFT.info
tickers.tickers.AAPL.info



 'financials',
 'quarterly_financials',
 'balancesheet',
 'quarterly_balancesheet',
 'cashflow',
 'quarterly_cashflow',
 


#%%
 
tickers = yf.Tickers('msft aapl goog')
for tt in tickers.tickers :
    print(tt.cashflow)

#%%

df = pd.read_csv('IWV_holdings.csv')
df.Ticker

tick = df.Ticker[0]
#%%
yy = yf.Ticker(tick)
cash = yy.quarterly_cashflow
bal = yy.quarterly_balancesheet
fin = yy.quarterly_financials
info = yy.info


dd = []
for k,v in info.items():
    dd.append([k,v])
    
dd = pd.DataFrame(dd)
dd.to_csv('./test1.csv',index=False)
#%%
#GP/A
gp = fin[fin.index =='Gross Profit'].iloc[0,0]
ass = bal[bal.index =='Total Assets'].iloc[0,0]

gp_a = gp/ass

ass = bal[bal.index =='Total Assets'].iloc[0,0]
liab = bal[bal.index =='Total Liab'].iloc[0,0]
book = bal[bal.index =='Total Stockholder Equity'].iloc[0,0]
#stock = bal[bal.index =='Common Stock'].iloc[0,0]

pbr = info['marketCap']/book


vv=bal
#EV= Market cap + total debt - C
market_cap = vv[vv.index =='Total Stockholder Equity'].iloc[0,0]
total_debt = vv[vv.index =='Short Long Term Debt'].iloc[0,0]
cas = vv[vv.index =='Cash'].iloc[0,0]


floatShares

ev = market_cap+total_debt-cas

#PBR = Price / BPS =  price /( (Asset - lib)/shares )
info['marketCap']
info['bookValue']
info['enterpriseValue']
info['enterpriseToRevenue']
info['priceToBook'] #pbr
info['enterpriseToEbitda'] #ev/ebitda 멀티플
info['floatShares'] #유동 주식수.
info['profitMargins']
info['sharesOutstanding']
info['earningsQuarterlyGrowth']
info['pegRatio']
info['regularMarketPrice']




#%%
import pandas as pd
import yfinance as yf
import numpy as np
import numpy as np
from datetime import datetime
from dateutil.relativedelta import *
import time

from multiprocessing import Process, Queue

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)






#신 마법 공식   저 PBR, 고 GP/A 
df = pd.read_csv('IWV_holdings.csv')
tickers = df.Ticker
#maxsize = len(tickers)
maxsize = 3
tickers = df.Ticker.iloc[0:maxsize]

import time

start = time.time()

mem = []
for ii, tick in enumerate(tickers): 
    gp_a=np.nan
    pbr= np.nan
    try: 
        bal, info = load_balsheet(tick)
    
        gp = bal[bal.index =='Gross Profit'].iloc[0,0]
        ass = bal[bal.index =='Total Assets'].iloc[0,0]
        
        gp_a = gp/ass
        
        book = bal[bal.index =='Total Stockholder Equity'].iloc[0,0]
        pbr = info['priceToBook']
        
        psr = 
        
    except Exception as e:
        print(e)
    mem.append([tick,gp_a,pbr])
    print(tick,'\t', ii,'/',len(tickers),'\t',gp_a,pbr)

df1 = pd.DataFrame(mem)
df1.columns=['TICK','GP/A','PBR']
df1.to_csv('./aaa.csv')

print("end time : ",time.time()-start)


df1 = pd.read_csv('./aaa.csv')

df1['GP/A rank'] = df1['GP/A'].rank(method='average', ascending=False) #high GP/A
df1['PBR rank'] = df1['PBR'].rank(method='average', ascending=True) #low PBR
df1['magic rank'] = df1['PBR rank']+df1['GP/A rank']

df1 = df1.sort_values('magic rank')
df1.to_csv('./magic.csv')
#%%
    

