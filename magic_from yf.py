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


"""
profitMargins
sharesOutstanding
earningsQuarterlyGrowth
pegRatio
regularMarketPrice
"""



#%%
import pandas as pd
import yfinance as yf
import numpy as np

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


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


#신 마법 공식   저 PBR, 고 GP/A 
df = pd.read_csv('IWV_holdings.csv')
tickers = df.Ticker
#maxsize = len(tickers)
maxsize = 20
tickers = df.Ticker.iloc[0:maxsize]

#target_month = ['2020-11-01','2021-02-01'] #포함 범위.
import time

start = time.time()

mem = []
for ii, tick in enumerate(tickers): 
    gp_a=np.nan
    pbr= np.nan
    try: 
        yy = yf.Ticker(tick)
    #    cash = yy.quarterly_cashflow
        bal = yy.quarterly_balancesheet
        fin = yy.quarterly_financials
        
        aa0 = bal.columns > target_month[0]
        aa1 = bal.columns < target_month[1]
        flag = bal.columns[ aa0&aa1]
        
        info = yy.info
    
        gp = fin[fin.index =='Gross Profit'][flag].iloc[0,0]
        ass = bal[bal.index =='Total Assets'][flag].iloc[0,0]
        
        gp_a = gp/ass
        
        book = bal[bal.index =='Total Stockholder Equity'][flag].iloc[0,0]
        
        pbr = info['marketCap']/book
        
        
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
    

