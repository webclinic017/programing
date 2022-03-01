# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:04:30 2021

@author: JAE
"""

import requests
from bs4 import BeautifulSoup
import json
import pprint
import pandas as pd
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from lxml import html
import lxml
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#file path access local html
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
    


    tree = html.fromstring(driver.page_source)
    
    #searching table financial data
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.
    assert len(table_rows) > 0
    
    parsed_rows = []
    
    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")
        
        none_count = 0
        
        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1
    
        if (none_count < 4):
            parsed_rows.append(parsed_row)
    
    df = pd.DataFrame(parsed_rows)
    
    

#aa= get_d0('O','Q',types[2])
#aa= get_d0('O','A',types[2])
#init_xw()
#write_ws(aa)

    
def get_d1(name="O",freq="Q"):
    df_list = []
    for tt in types:
        df_list.append(get_d0(name,freq,tt))
    return pd.concat(df_list)

