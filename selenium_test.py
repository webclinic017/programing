# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:39:23 2019

@author: JAE
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:\\chromedriver.exe')

#%%

#driver.get("https://www.google.co.kr")
driver.get("https://kr.investing.com")
#try:
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "PromoteSignUpPopUp"))
)

#finally:
#    driver.quit()
#    

#%%
search = driver.find_element_by_xpath("/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input")
search.send_keys("AAPL")
#%%
#search.submit()

search_click = driver.find_element_by_xpath("/html/body/div[5]/header/div[1]/div/div[3]/div[1]/label")
search_click.click()

#%%
driver.get("https://kr.investing.com/equities/apple-computer-inc")

https://kr.investing.com/equities/apple-computer-inc-income-statement
https://kr.investing.com/equities/apple-computer-inc-balance-sheet
https://kr.investing.com/equities/apple-computer-inc-cash-flow
https://kr.investing.com/equities/apple-computer-inc-ratios
https://kr.investing.com/equities/apple-computer-inc-dividends
https://kr.investing.com/equities/apple-computer-inc-earnings
