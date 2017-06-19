from urllib.request import urlopen
import urllib.error
from bs4 import  BeautifulSoup
import datetime
import random
import re
import json

random.seed(datetime.datetime.now())
def getlinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsobj = BeautifulSoup(html, 'html.parser')
    return bsobj.find("div", {'id': 'bodyContent'}).find_all('a', href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    #编辑历史页面URL的连接格式是：http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url:"+historyUrl)
    html = urlopen(historyUrl)
    bsobj = BeautifulSoup(html, 'html.parser')
    ipAddresses = bsobj.find_all("a", {"class": "mw-userlink mw-anonuserlink"})
    addressList = set()
    for ipAddresse in ipAddresses:
        addressList.add(ipAddresse.get_text())
        # print(ipAddresse.get_text())
    return addressList


def getcountry(ipaddress):
    try:
        url="http://freegeoip.net/json/"+ipaddress
        # print("url:"+url)
        response = urlopen(url).read().decode("utf-8")
    except urllib.error.HTTPError:
        return None
    responseJson = json.loads(response)
    # print(responseJson.get("country_code"))
    return responseJson.get("country_code")

links = getlinks("/wiki/Python_(programming_language)")
while(len(links)>0):
    for link in links:
        print("----------------------------------")
        historyIPs = getHistoryIPs(link.attrs['href'])
        for historyIP in historyIPs:
            # print("history ip" + historyIP)
            country = getcountry(historyIP)
            if country is not None:
                print(historyIP+" is from "+country)

    newLink = links[random.randint(0, len(links))].attrs['href']
    links = getlinks(newLink)