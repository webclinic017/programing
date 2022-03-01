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


import yfinance as yf
import os
PATH= "./future_data"

#%%
    
#b_list = ['SHY','IEF','TLT','TIP','LQD','HYG','BWX','EMB']  #장기, 단기,중기,회사,하이일드,등등 채권 롤링
#b_list = ['VT','BCI','IAU','EDV','LTPZ','VCLT','VWOB']  #올웨더
#b_list = ['NQ=F','ZB=F','ZN=F','GC=F','SI=F','ES=F','ZT=F','EURUSD=X','JPY=X']  #선물
b_list = ['ES=F','YM=F','NQ=F','ZB=F','ZN=F','GC=F','SI=F','HG=F','CL=F']  #선물
#b_list = ['ZB=F','ZN=F','ZF=F','ZT=F']  #채권
#b_list = ['^GSPC','^IXIC','^DJI','^RUT','^TNX']  #지수



def get_data(b_list):
    for b in b_list:
    #    d0= yf.download(b,start='1900-01-01',end='2021-02-01')
        d0= yf.download(b,period="max")
        d0.to_excel('{}/{}.xlsx'.format(PATH,b))
    



d0 = os.listdir(PATH)

d1 = pd.read_excel('{}/{}'.format(PATH,d0[0])).set_index('Date')

d1.iloc[1]



d1['Close'].plot()

a0= d1.iloc[10:50,0:4]

a1 = a0.to_numpy()
a2 = torch.FloatTensor(a1)
a2.size(0)
x0 = torch.linspace(10,50)

#%%


import torch
import torch.nn as nn
model = nn.Linear(4, 1)

import torch.nn.functional as F
cost = F.mse_loss(prediction, y_train)


optimizer = torch.optim.SGD(model.parameters(), lr=0.01) 
nb_epochs = 500
for epoch in range(nb_epochs+1):

    # H(x) 계산
    prediction = model(x_train)

    # cost 계산
    cost = F.mse_loss(prediction, y_train) # <== 파이토치에서 제공하는 평균 제곱 오차 함수

    # cost로 H(x) 개선하는 부분
    # gradient를 0으로 초기화
    optimizer.zero_grad()
    # 비용 함수를 미분하여 gradient 계산
    cost.backward() # backward 연산
    # W와 b를 업데이트
    optimizer.step()

    if epoch % 100 == 0:
    # 100번마다 로그 출력
      print('Epoch {:4d}/{} Cost: {:.6f}'.format(
          epoch, nb_epochs, cost.item()
      ))