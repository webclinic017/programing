import requests
from bs4 import BeautifulSoup
import json
import pprint
import pandas as pd

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
    wb.sheets.add()
    ws = wb.sheets[0]

def add_ws():
    global wb,ws
    wb.sheets.add()
    ws = wb.sheets[0]


def pexcel(df):
    global wb,ws
    ws.range((1,1)).value =df
    
name="O"
freq="Q"

types = ['income-statement?freq='
    ,'balance-sheet?freq='
    ,'cash-flow-statement?freq='
    ,'financial-ratios?freq='
    ]
    
    
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

#%%
    
aa = get_data('O','Q')

#%%

ws.range((1,1)).value = aa[0]
add_ws()
ws.range((1,1)).value = aa[1]
add_ws()
ws.range((1,1)).value = aa[2]
add_ws()
ws.range((1,1)).value = aa[3]





