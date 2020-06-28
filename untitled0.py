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
    

#msft = yf.Ticker("MSFT")
#msft.info
#hist = msft.history(period="max")
#msft.actions
#msft.dividends
#msft.splits
#msft.financials
#msft.quarterly_financials
#stock.major_holders
#stock.institutional_holders
#msft.balance_sheet
#msft.quarterly_balance_sheet
#msft.cashflow
#msft.quarterly_cashflow
#msft.earnings
#msft.quarterly_earnings
#msft.sustainability
#msft.recommendations
#msft.calendar
#msft.isin
#msft.options
#opt = msft.option_chain('YYYY-MM-DD')


def get_data(name="O",freq="Q"):
    if freq !='A' and freq !='Q':
        return 0
    POPUP_ICON_CROP_LENGTH=5

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
            
            string=df.loc[:,'popup_icon'][i]
            a0=string.find('t:')
            a1=string.find(',',a0)
            a2=string.find('freq:',a1)
            a3=string.find(',',a2)
            txt=string[a0:a1]+','+string[a2:a3]
            df.loc[:,'popup_icon'][i] = txt
        aa=df.apply(lambda x : x['popup_icon'].__len__() < POPUP_ICON_CROP_LENGTH, axis=1)
        df2=df.drop(aa[aa==True].index)
        df_list.append(df2)
        
    return df_list


def save_data(name):
    "분기별, 연도별, 파이넨스 데이터 전부."
    "일별 주가 데이터전부."
    global wb,ws
    
    fname ="./data/data_{}.xlsx".format(name)
    wb = xw.Book()
    ws = wb.sheets[0]
    
    aa = get_data(name,'Q')
    add_ws('Qincome')
    write_ws(aa[0])
    add_ws('Qbalance')
    write_ws(aa[1])
    add_ws('Qfinratio')
    write_ws(aa[3])
    
    aa = get_data(name,'A')
    add_ws('Aincome')
    write_ws(aa[0])
    add_ws('Abalance')
    write_ws(aa[1])
    add_ws('Acashflow')
    write_ws(aa[2])
    add_ws('Afinratio')
    write_ws(aa[3])
    
    
    tick = yf.Ticker(name)
#    add_ws('info')
#    
#    i = 1
#    for k,v in tick.info.items():
##        print(k,v,type(k),type(v)) 
#        ws.range((i,1)).value = k
#        ws.range((i,2)).value = v
#        i+=1
#        
#    add_ws('actions')
#    write_ws(tick.actions)
    add_ws('history')
    write_ws(tick.history(period="max"))
    
    wb.save(fname)
    
    wb.close()
    

#%%

save_data('WFC')

#%%

tic=['SPG','CCL','LULU','DOCU','ABBV','XOM','VZ','MSFT']
for t in tic:
    save_data(t)

#%%

"extract yield curve "
rawurl = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldAll'
res = requests.get(rawurl)
    
html = res.text
soup = BeautifulSoup(html,'html.parser')

table = soup.find_all('table',class_='t-chart')
df = pd.read_html(table[0].prettify())
df = df[0].fillna(0)
df.to_csv('./data/yield_curve.csv')



#%%


