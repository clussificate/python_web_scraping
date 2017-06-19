from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import requests

#  urllib写
random.seed(datetime.datetime.now())
def getlinks(articleUrl):
    html = urlopen("https://en.wikipedia.org/"+articleUrl)
    bsobj = BeautifulSoup(html, 'html.parser')
    return bsobj.find("div",{'id':"bodyContent"}).findAll('a', href=re.compile("^(/wiki/)((?!:).)*$"))
    # for link in bsobj.find("div",{'id':"bodyContent"}).findAll('a', href=re.compile("^(/wiki/)((?!:).)*$")):
    #     print(link)
    #     # if 'href' in link.attrs:
    #     #     print(link.attrs['href'])
links = getlinks("/wiki/Kevin_Bacon")
while len(links)>0:
    newArticle = links[random.randint(0,len(links)-1)].attrs['href']
    print(newArticle)
    links = getlinks(newArticle)

# 用requests写

# html = requests.get("https://en.wikipedia.org/wiki/Kevin_Bacon")
# html.encoding = 'utf-8'
# bsobj = BeautifulSoup(html.text, 'html.parser')
# contents = bsobj.select('a')
# print(contents)
# for content in contents:
#     if 'href' in content.attrs:    #判断是否有link属性
#         print(content['href'])

# test
# html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
# bsobj = BeautifulSoup(html, 'html.parser')
# for link in bsobj.find("div",{"id":"bodyContent"}).findAll("a", href=re.compile("^/wiki/((?!:).)*$")):
#     print(link.attrs['href'])





