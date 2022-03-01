# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:41:40 2021

@author: JAE
"""



import pandas as pd
import yfinance as yf
import numpy as np
import numpy as np
from datetime import datetime
from dateutil.relativedelta import *
import time
import os
import sys
import shutil
from multiprocessing import Process, Queue, freeze_support

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


def save_momentum(tick , months=[1,3,6,12],margin_day=15):
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
        
        
    df = pd.DataFrame([mm_list])
    df.columns= ['1M','3M','6M','12M']
    df = latest_price/df
    df['cur_price']=latest_price
    df.to_csv('./data2/{}_mom.csv'.format(tick))

def save_balsheet(tick):
    yy = yf.Ticker(tick)
    cash = yy.quarterly_cashflow
    bal = yy.quarterly_balancesheet
    fin = yy.quarterly_financials
    bal=pd.concat([bal,fin,cash])


    bal.to_csv('./data2/{}.csv'.format(tick))
    info = yy.info
    dd = []
    for k,v in info.items():
        dd.append([k,v])
        
    dd = pd.DataFrame(dd)
    dd.to_csv('./data2/{}_info.csv'.format(tick))
    return bal,dd



def ps_work(idd, tickers):
    print(idd,"start")
    for ii, tick in enumerate(tickers): 
        try:
            bal,info=save_balsheet(tick)
            save_momentum(tick)
            print(idd,tick,'\t', ii,'/',len(tickers),'\t')
        except Exception as e:
            print(e)
            pass
    pass


def mp_update_bal(tickers,NOP=10):
#    os.rmdir('./data2')
    try:
        out = np.array_split(tickers,NOP)
        ps=[]
        idd=0
        print(len(out))
        for ticks in out:
            p = Process(target=ps_work,args=(idd, ticks,))
            ps.append(p)
            p.start()
            idd+=1
        print('join')
        for p in ps:
            p.join()
        print('save done')
    except :
        print('err')
        input()



def load_balsheet(tick):
    bal = pd.read_csv('./data2/{}.csv'.format(tick))
    info = pd.read_csv('./data2/{}_info.csv'.format(tick))
    mom = pd.read_csv('./data2/{}_mom.csv'.format(tick))
    bal = bal.set_index('Unnamed: 0')
    mom = mom.set_index('Unnamed: 0')
    info = info.drop('Unnamed: 0',axis=1)
    info = info.set_index('0')
            
            
            
    return bal,info,mom
   

def get_item(ba,ss='',summ=False):
    if summ==False:
        aa = ba[ba.index ==ss].dropna(axis=1)
        if aa.size!=0:
            return aa.iloc[0,0]
        else:
            return 0.0
    else:
        return ba[ba.index ==ss].sum(axis=1).iloc[0]
        

def magic_run():
    mem=[]
    base = './data2'
    bb0 = os.listdir(base)    
    mm_path = os.path.join(base,'00_moment.csv')
    

    
    
    #data2 folder pre processing
    bb1 = [b for b in bb0 if not 'info' in b]
    bb1 = [b for b in bb1 if not 'mom' in b]
    bb2 = [b for b in bb1 if not '00' in b]
    tickers = [b.replace('.csv','') for b in bb2 ]
#    tickers
    err_tick = []
#    print("{} \t {}/{}\t{:8},{:8},{:8},{:8}".format('ticker',"i","max",'gp_a','pbr','psr','per'))
    print("{} \t {}/{}\t{:8},{:8}".format('ticker',"i","max",'ROC','EY'))
    for ii, tick in enumerate(tickers): 
        try:
#            tick='OSUR'
#            tick='AAPL'
#            tick='AROW'
            gp_a=np.NaN
            pbr=np.NaN
            per=np.NaN
            psr=np.NaN
            ROC=np.NaN
            EY=np.NaN
            
            ba,info,mom = load_balsheet(tick)
            
            
            gp = get_item(ba,'Gross Profit')
            ass = get_item(ba,'Total Assets')
            
            
            
#            rev = ba[ba.index =='Total Revenue'].sum(axis=1).iloc[0]
#            income = ba[ba.index =='Net Income'].sum(axis=1).iloc[0]
            ebit = get_item(ba,'Ebit',True)
#            book = ba[ba.index =='Total Stockholder Equity'].dropna(axis=1).iloc[0,0]
            
            liab = get_item(ba,'Total Liab')
            current_asset = get_item(ba,'Total Current Assets')
            cash_eq = get_item(ba,'Cash')
            l_debt = get_item(ba,'Long Term Debt')
            borrow = get_item(ba,'Short Long Term Debt')
#            other_liab = ba[ba.index =='Other Liab'].dropna(axis=1).iloc[0,0]
            
            current_liab = get_item(ba,'Total Current Liabilities')
            depreciation = get_item(ba,'Depreciation')
            
#            total_non_cur_liab = l_debt + other_liab
#            total_non_cur_liab = liab - current_liab
            
            total_non_current_asset = ass - current_asset
            
            markcap = float(info[info.index=='marketCap'].iloc[0,0])
#            ev = float(info[info.index=='enterpriseValue'].iloc[0,0])
            
            ev = markcap + l_debt +borrow -cash_eq  #without cp 
            cap=((current_asset-current_liab)+( total_non_current_asset - depreciation ))
            ROC = ebit / cap
            EY = ebit/ev
            
#자본수익률 = 법인세전이익(EBIT)/((유동자산-유동부채)+(비유동자산-감가상각비))  #높은거
#이익수익률 = 법인세전이익/(시가총액+순차입금) = ebit/EV    #높은거 
           #per 낮은거  저평가.        이익수익률
            #ev/ebit  낮을 수록 저평가  이익수익률
            #roe 높은거 돈 잘버는거.  자본수익률
            #gp/a  자본 수익률. 높은거. 자본수익률
#            
#            pbr = markcap/book
#            psr = markcap/rev
#            per = markcap/income
#            
#            float(info[info.index=='priceToBook'].iloc[0,0])
#            float(info[info.index=='priceToSalesTrailing12Months'].iloc[0,0])
#            float(info[info.index=='trailingPE'].iloc[0,0])
            
#            mem.append([tick,gp_a,pbr,psr,per])
            mem.append([tick,ebit,ev,cap,ROC,EY])
            print("{} \t {}/{}\t{:8.2f},{:8.2f}".format(tick,ii,len(tickers),ROC,EY))
#            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),gp_a,pbr,psr,per))
        except Exception as e:
            print(e)
            print("{} \t {}/{}\t{:8.2f},{:8.2f}".format(tick,ii,len(tickers),ROC,EY))
#            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),gp_a,pbr,psr,per))
            err_tick.append(tick)
            pass
        
    
    df1 = pd.DataFrame(mem)
#    df1.columns=['TICK','GP/A','PBR','PSR','PER']
    df1.columns=['TICK','ebit','ev','cap','ROC','EY']
    
#    df1['GP/A rank'] = df1['GP/A'].rank(method='average', ascending=False) #high GP/A
#    df1['PBR rank'] = df1['PBR'].rank(method='average', ascending=True) #low PBR
#    df1['PSR rank'] = df1['PSR'].rank(method='average', ascending=False) #
#    df1['PER rank'] = df1['PER'].rank(method='average', ascending=True) #
    df1['ROC rank'] = df1['ROC'].rank(method='average', ascending=False) #
    df1['EY rank'] = df1['EY'].rank(method='average', ascending=False) #
    
    
    df1['magic rank'] = df1['ROC rank']+df1['EY rank']
    
    df1 = df1.sort_values('magic rank')
    df1.to_csv('./magic.csv')
    

        
    print('err ticker',err_tick, len(err_tick))
    print('restore err')
    restore(err_tick)
    
    

def magic_momentum_run():
    mem=[]
    base = './data2'
    bb0 = os.listdir(base)    
    

    #data2 folder pre processing
    bb1 = [b for b in bb0 if not 'info' in b]
    bb2 = [b for b in bb1 if not 'mom' in b]
    tickers = [b.replace('.csv','') for b in bb2 ]
#    tickers = tickers[0:10]
    err_tick = []
    print("{} \t {}/{}\t{:8},{:8},{:8}".format('ticker',"i","max",'ROC','EY','MOM'))
    for ii, tick in enumerate(tickers): 
        try:
#            tick='OSUR'
#            tick='AAPL'
#            tick='GNMK'
            gp_a=np.NaN
            pbr=np.NaN
            per=np.NaN
            psr=np.NaN
            ROC=np.NaN
            EY=np.NaN
            mavg=-1
            
            
            ba,info,mom = load_balsheet(tick)
            
            mavg = mom.iloc[:,0:4].mean(axis=1).iloc[0]
            mm = mom.iloc[0].tolist()
            
            gp = get_item(ba,'Gross Profit')
            ass = get_item(ba,'Total Assets')
            
            
            ebit = get_item(ba,'Ebit',True)
            
            liab = get_item(ba,'Total Liab')
            current_asset = get_item(ba,'Total Current Assets')
            cash_eq = get_item(ba,'Cash')
            l_debt = get_item(ba,'Long Term Debt')
            borrow = get_item(ba,'Short Long Term Debt')
            
            current_liab = get_item(ba,'Total Current Liabilities')
            depreciation = get_item(ba,'Depreciation')
            
            
            total_non_current_asset = ass - current_asset
            
            markcap = float(info[info.index=='marketCap'].iloc[0,0])
            
            ev = markcap + l_debt +borrow -cash_eq  #without cp 
            cap =((current_asset-current_liab)+( total_non_current_asset - depreciation ))
            ROC = ebit / cap
            EY = ebit/ev
            
#자본수익률 = 법인세전이익(EBIT)/((유동자산-유동부채)+(비유동자산-감가상각비))  #높은거
#이익수익률 = 법인세전이익/(시가총액+순차입금) = ebit/EV    #높은거 
#            mom[mom.index==tick]
            mem.append([tick,ebit,ev,markcap,cap,mm[0],mm[1],mm[2],mm[3],mm[4],ROC,EY,mavg])
            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),ROC,EY,mavg))
#            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),gp_a,pbr,psr,per))
        except Exception as e:
            print(e)
            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),ROC,EY,mavg))
#            print("{} \t {}/{}\t{:8.2f},{:8.2f},{:8.2f},{:8.2f}".format(tick,ii,len(tickers),gp_a,pbr,psr,per))
            err_tick.append(tick)
            pass
        
    
    df1 = pd.DataFrame(mem)
#    df1.columns=['TICK','GP/A','PBR','PSR','PER']
    df1.columns=['TICK','ebit','ev','markcap','cap','1M','3M','6M','12M','Price','ROC','EY','MOM']
    
    
#    df1['GP/A rank'] = df1['GP/A'].rank(method='average', ascending=False) #high GP/A
#    df1['PBR rank'] = df1['PBR'].rank(method='average', ascending=True) #low PBR
#    df1['PSR rank'] = df1['PSR'].rank(method='average', ascending=False) #
#    df1['PER rank'] = df1['PER'].rank(method='average', ascending=True) #
    df1['ROC rank'] = df1['ROC'].rank(method='average', ascending=False) #
    df1['EY rank'] = df1['EY'].rank(method='average', ascending=False) #
#    df1['MOM rank'] = df1['MOM'].rank(method='average', ascending=False) #
    
    
    df1['magic rank'] = df1['ROC rank']+df1['EY rank']
    
    df1 = df1.sort_values('magic rank')
#    df1.to_csv('./MAIN_MAGIC_OUT.csv')
    
    df1.to_excel('./MAIN_MAGIC_OUT.xlsx')
        
    print('err ticker',err_tick, len(err_tick))
    print('restore err')
    restore(err_tick)
    
def restore(err_tick):
    
    for ii, tick in enumerate(err_tick):
        try:
            print(ii,'/',len(err_tick),tick)
            save_balsheet(tick)
            save_momentum(tick)
        except Exception as e:
            print(e)
        
def valid_check(tickers):
    res = []
    check_ba = ['Gross Profit',
        'Total Assets',
        'Ebit',
        'Total Liab',
        'Total Current Assets''Cash',
        'Long Term Debt',
        'Short Long Term Debt',
        'Total Current Liabilities',
        'Depreciation']
#    tick = df.Ticker[0]
    for ii, tick in enumerate(tickers):
        try:
            print(ii,'/',len(tickers))
            ba,info,mom = load_balsheet(tick)
            
            ii = 0
            
            for ck in check_ba:
                if isinstance(get_item(ba,ck),float) :
#                    print('pass',tick,ck)
                    pass
                else:
                    print('fail',tick,ck)
                    ii=1
                    
            if isinstance(float(info[info.index=='marketCap'].iloc[0,0]),float):
#                print('pass marketcap')
                pass
            else:
                print('fail marketcap')
                ii=1
            if ii == 1:
                res.append(tick)
        except:
            res.append(tick)
#    restore(res)
    return res
#%%

if __name__ == '__main__':
    print("1.update bal sheet,2.valid check  3.magic run, 4. magic_mom_run ")    
    opt= input()
    
    freeze_support()
    if opt=='1':
        shutil.rmtree('data2',ignore_errors=True)
        print('rmdir')
        os.mkdir('./data2')
        print('mkdir')
        df = pd.read_csv('iwv.csv')
        df = df.dropna(subset=['Ticker'])
        print('update bal sheet')
        mp_update_bal(df.Ticker)
    elif opt=='2':
        df = pd.read_csv('iwv.csv')
        df = df.dropna(subset=['Ticker'])
        print('valid check')
        rr = valid_check(df.Ticker)
        
        mp_update_bal(rr,5)
        pass
    elif opt=='3':
        print('magic_run')
        magic_run()
    elif opt=='4':
        print('magic_mom_run')
        magic_momentum_run()
    print("press doen")
    aa=  input()