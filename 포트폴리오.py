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
#%% data download
"""
AGG US Tbond aggregate 
BND total bond
BNDX total international bond
BSV 단기 세계

LQD 투자등급 회사채

MBB  MBS 채권
IGSB 1-5Y 투자등급 회사채


VCIT 중기 회사채
VCSH 단기 회사채


HYG  high yield 회사채
JNK  high yield 회사채
SRLN  시니어 론 ETF 



SHV  1M~1Y Tbond
SHY  1~3Y Tbond  
IEF  7~10Y Tbond
TLT  19Y Tbond
VGLT 18Y Tbond
EDV  25Y Tbond

SCHP 7.5Y TIPS
VTIP 1~3Y 단기 TIPS
TIP  7~10 중기 TIPS
LTPZ   20+ 장기 TIPS

UST  중기 2x
TYD  중기 3x
UBT  장기 2x
TMF  장기 3x

TBX  중기 -1x
PST  중기 -2x

TMV  장기 -3x

TBF  장기 -1x
TBT  장기 -2x
TTT  장기 -3x

SH   sp500 -1x
SDS  sp500 -2x
SPXU sp500  -3x
SPXS  sp500 -3x #거래량 적음
SSO    2x
SPXL    3x
UPRO  3x

UVXY  x1.5 vix 단기 
TVIX   x2  ETN
VIXY  vix 단기
SIXY   -1x
VIXM  중기 vix
SVXY  vix 단기 -1x
VXX   vix 단기  ETN 최초 상품
VXZ  중기 vix ETN



QQQ   1x
PSQ  -1x
QID  -2x

SQQQ  -3x
TQQQ  3x
QLD x2

QYLD  qqq커버드 콜


GLD
SLV


"""

"SHY IEF TLT EDV VTIP TIP LTPZ "



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
