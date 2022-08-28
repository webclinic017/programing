# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 23:23:51 2022

@author: JAE
"""

# 0TAtF9hPBrTIUxXDyP

# YPbdf9Za5HrwULvo4SQqlXs6NJrMyccMo3rb

from pybit import HTTP
import pprint
import pandas as pd
import datetime
import time

session = HTTP(
    endpoint="https://api.bybit.com", 
    # spot=False
)

# aa = datetime.datetime.now().timestamp()-20000
# aa = int(aa)

dd = []


start=datetime.datetime(2022, 1, 1).timestamp()
end=datetime.datetime(2022, 4, 1).timestamp()

aa=int(start)

for i in range(int((end-start)/60/200)):
    
    resp = session.query_kline(
        symbol="BTCUSDT",
        interval=1,
        # limit=200,
        from_time=aa
    )
    aa=aa+200*60
    
    
    
    result = resp['result']
    df = pd.DataFrame(result)
    ts = pd.to_datetime(df['open_time'], unit='s')
    df.set_index(ts, inplace=True)
    df = df[['open', 'high', 'low', 'close']]
    print(df)
    dd.append(df)
    # time.sleep(1)
    

da = pd.concat(dd[::-1])
da.to_csv('./bb2022_1q.data')
