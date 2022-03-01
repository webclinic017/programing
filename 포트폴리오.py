# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import yfinance as yf
ticker = "ES=F NQ=F ZB=F ZN=F ZT=F GC=F SI=F HG=F CL=F"
ticker = "SPY TLT"
df= yf.download(ticker,period='max')
df = df['Adj Close']
df = df.fillna(method='ffill')
df = df.dropna(axis=0,how='any')

# df.to_clipboard()
#%% 분기 분할
df = df.resample(rule='1Q').last()





#%% normalize  first day = 1

df1 = df/df.iloc[0]
df1.to_clipboard()



#%%

target = ['ES=F','ZN=F']
balance = [0.6, 0.4]

df2 = df1[target]


p2 = df2.pct_change()
p2.iloc[1]*[0.6,0.4]
p2.iloc[2]*[0.6,0.4]


p2.iloc[1]*df2.iloc[0]*init_bal




df2.iloc[1]
df2.to_clipboard()

#%%
# target = ['ES=F','ZN=F']
# balance = [0.6, 0.4]
df2 = df

# df2 = df2/df2.iloc[0]

bal = [0.6,0.4]
cash = 10000
nof_eq0 = 0
nof_eq1 = 0

dd = df2.iloc[0]
df2 = df2.assign(quarter=df2.index.quarter,is_q_end=df2.index.is_quarter_end,eq0=0,eq1=0,cash=0,evalpf=0)


# df2['eq0']=0
# df2['eq1']=0
# df2['cash']=0
# df2['evalpf']=0
#%%
# for idx,dd in df2[:10].iterrows():
for idx,dd in df2.iterrows():
    if dd['is_q_end']:
        print(dd)
    #평가 잔고
    # evalpf = nof_eq0*dd[0] + nof_eq1*dd[1] + cash 
    # #리벨런싱
    # nof_eq0 = evalpf*bal[0]/dd[0]
    # nof_eq1 = evalpf*bal[1]/dd[1]
    # cash = evalpf - (dd[0]*nof_eq0 + dd[1]*nof_eq1)
    # df2.loc[idx,'eq0']=nof_eq0
    # df2.loc[idx,'eq1']=nof_eq1
    # df2.loc[idx,'cash']=cash
    # df2.loc[idx,'evalpf']=evalpf
    # print(evalpf , nof_eq0,nof_eq1)    


#%%
df2['max']=df2['evalpf'].rolling(4*3,min_periods=1).max()
df2['dd'] = df2['evalpf']/df2['max']-1

df2['evalpf'].plot()

mdd = df2['dd'].min()

#%%  cagr    
bv = df2.iloc[0]['evalpf']
ev = df2.iloc[-1]['evalpf']
n = df2.__len__()

cagr = (ev/bv)**(1/(n/4))-1
print(cagr)
ev
bv
