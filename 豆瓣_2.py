import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def getlist(datas):
    a=[]
    for data in datas:
        a.append(data.text)
    return a

url = 'http://movie.douban.com/review/best/?start=0'
req = requests.get(url)
req.encoding = 'utf-8'
soup = BeautifulSoup(req.text, 'html.parser')
names = soup.find_all('span', {'property': 'v:reviewer'})
titles = soup.select('.title-link')
films = soup.find_all('a', {'class': 'subject-title'})
times = soup.find_all('span', {'property': 'v:dtreviewed'})
favors = soup.find_all('span', {'class': 'left'})

namelists = getlist(names)
filmlists = getlist(films)
favorlists = getlist(favors)
print(favorlists)
FdataFrame = pd.DataFrame({'name': namelists, 'film': filmlists})
print(FdataFrame)
# FdataFrame.to_csv('Dataout.csv', sep=",", encoding='utf-8')
# baseUrl = 'http://movie.douban.com/review/best/?start='

