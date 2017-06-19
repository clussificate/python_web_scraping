import requests
from bs4 import BeautifulSoup
import re
import csv

# 字符串格式化
def F_data(data):   # *data 传递的是空元组
    F_d = data.replace('\t', '').replace('\n', '').replace(' ', '').replace('\"', '')
    return F_d

def getlink(baseurl):
    links = []
    for i in range(0,5):    #实际爬的过程中发现，10,30,40这些页都没显示。
        url = baseurl+str(i*20)
        req = requests.get(url)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'html.parser')
        results = soup.find_all('a', {'class': 'title-link'})
        for result in results:
            print(result['href'])
            links.append(result['href'])
    print('共获取到'+len(links)+'条链接')
    return links


def getdata(link):
    req = requests.get(link)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    name = soup.find('span', {'property': 'v:reviewer'}).text
    film = soup.find('a', {'href': re.compile(r'https://movie.douban.com/subject/[0-9]+/')}).text
    rate = soup.find('span', {'class': re.compile('allstar.0 main-title-rating')})['title']
    viewdt = soup.find('span', {'property': 'v:dtreviewed'}).text.strip()
    favor = F_data(soup.find('button', {'class': re.compile('btn useful_count .+ j a_show_login')}).text)
    disfavor = F_data(soup.find('button', {'class':re.compile('btn useless_count .+ j a_show_login')}).text)
    content = F_data(soup.find('', {'property': 'v:description'}).text)
    setdata(name, film, rate, viewdt, favor, disfavor, content)
    return None


def setdata(name, film, rate, viewdt, favor, disfavor, content):
    csvfile = open('mydata.csv', 'a', encoding='utf-8')
    try:
        writer = csv.writer(csvfile)
        writer.writerow((name, film, rate, viewdt, favor, disfavor, content))
    finally:
        csvfile.close()

baseurl = 'https://movie.douban.com/review/best/?start='
links = getlink(baseurl)
for link in links:
    getdata(link)

