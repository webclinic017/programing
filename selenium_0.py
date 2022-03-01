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
 
#opening file in firefox browser
driver = webdriver.Chrome()

tick='AAPL'
sheet = ['https://finance.yahoo.com/quote/{}/financials?p={}',
'https://finance.yahoo.com/quote/{}/cash-flow?p={}',
'https://finance.yahoo.com/quote/{}/balance-sheet?p={}']

import time

def scrap(tick,sheet):
#    sheet=sheet[2]
    driver.get(sheet.format(tick,tick))
    driver.implicitly_wait(time_to_wait=5)
    
    #분기 
    qu = driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button')
    qu.click()
    #확장
    bt = driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
    bt.click()
    
#    driver.implicitly_wait(time_to_wait=5)
    time.sleep(0.1)
#    driver.implicitly_wait(time_to_wait=5)    
    
    #parsing into lxml
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
    return df

#df = scrap("AAPL",sheet[0])
#df = scrap_all("AAPL")

def scrap_all(tick):
    ret = []
    for ss in sheet:
        ret.append(scrap(tick,ss))
    return pd.concat(ret)

def save_d1(path='./data2', name="AAPL"):
    ret = scrap_all(name)
    ret.to_csv('{}/{}.csv'.format(path,name),index=False)

save_d1()
