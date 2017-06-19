import requests
from bs4 import BeautifulSoup
import re
import pandas as pa
import csv

def setData(name, film, rate, viewdt, favor, disfavor, content):
    csvFile = open('mydata.csv', 'a', encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        writer.writerow((name, film, rate, viewdt, favor, disfavor, content))
    finally:
        csvFile.close()

def F_data(data):  #*data 传递的是空元祖
    F_d = data.replace('\t', '').replace('\n', '').replace(' ', '').replace('\"', '')
    return F_d

req = requests.get('https://movie.douban.com/review/8389080/')
req.encoding = 'utf-8'
soup = BeautifulSoup(req.text, 'html.parser')
name = soup.find('span', {'property': 'v:reviewer'}).text
film = soup.find('a', {'href': re.compile(r'https://movie.douban.com/subject/[0-9]+/')}).text
rate = soup.find('span', {'class': 'allstar40 main-title-rating'}).text
viewdt = soup.find('span', {'property': 'v:dtreviewed'}).text.strip()
favor = F_data(soup.find('button', {'class': 'btn useful_count 8389080 j a_show_login'}).text)
disfavor = F_data(soup.find('button', {'class': 'btn useless_count 8389080 j a_show_login'}).text)
content = F_data(soup.find('', {'property': 'v:description'}).text)
setData(name, film, rate, viewdt, favor, disfavor, content)

