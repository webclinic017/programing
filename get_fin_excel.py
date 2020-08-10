# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 00:53:15 2020

@author: JAE
"""


items = ['T','O','APLE','WFC','BA']
dim = ['Q','A']
section= ['Balance%20Sheet', 'Income%20Statement','Cash%20Flow','Metrics','Growth']


base_url = 'https://stockrow.com/api/companies/{}/financials.xlsx?dimension={}&section={}&sort=desc'

import wget
import pandas as pd
import os


def get_excel_data(items):
    for item_ in items:
        xl_list=[]
        dim_ = dim[0]
        for section_ in section:
            url = base_url.format(item_,dim_,section_) 
            fname = './{}_{}_{}.xlsx'.format(item_,dim_,section_)
            wget.download(url, fname)
            print('wget ',fname)
            xl_list.append(fname)    
        
        xls = [pd.ExcelFile(xl) for xl in xl_list]
        frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in xls]
        alldf = pd.concat(frames)
        alldf.to_excel("./all_{}.xlsx".format(item_),header=False,index=False)
        for xl in xls:
            os.remove(xl)
    

def _get_valid_index(df, key):
    valid_list=[]
    for i in df.index :
        line = df.iloc[i,0]
        if type(line)!=str:
            continue
#            print(i,line)
        if key in line:
            valid_list.append(i)
    return valid_list


def get_data_from_key(keys,items):
    ll=[]
    for item in items:
        fname = './all_{}.xlsx'.format(item)
        try:
            df = pd.read_excel(fname)
        except:
            print('file read err')
            get_excel_data([item])
            return -1
        
        valid=[]
        for key in keys:
#            print(key)
            vl = _get_valid_index(df,key)
            valid.extend(vl)
#        print(valid)
        vdf = df.iloc[valid]
        vdf.insert(0,'Name',item)
        ll.append(vdf)
    adf = pd.concat(ll)
    adf.columns.values[1] = "comment"
    aa = adf.sort_values('comment')
    return aa

        
        
#%%


import xlwings as xw
#items = ['T','O','APLE','WFC','BA','TMUS','VZ']
items = ['T','O','TMUS','VZ']
#keys=['EPS','Income','Debt','Revenue','Margin']
keys=['Revenue','Debt']
#wb = xw.Book()
ws = wb.sheets[0]
aa = get_data_from_key(keys,items)

ws.range((1,1)).value= aa.columns.tolist()
ws.range((2,1)).value= aa.values.tolist()


#%%
    
    
 
