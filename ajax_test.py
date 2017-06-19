import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 下列代码只能抓取加载前页面的数据
req = requests.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
html = BeautifulSoup(req.text, 'html.parser')
txt = html.select('#content')
print(txt[0].text)

# #抓取加载后页面的数据
# driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe') #需要配置Chromedriver
# driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
# try:
#     element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'loadedButton')))
# finally:
#     r = driver.find_element_by_css_selector('#content')
#     print(r.text)
#     driver.close()

