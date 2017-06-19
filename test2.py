from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsobj = BeautifulSoup(html, 'html.parser')

namelist = bsobj.find_all("span", {"class":"green"})
for name in namelist:
    print(name.get_text())