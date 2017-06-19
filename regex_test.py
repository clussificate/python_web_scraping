from urllib.request import urlopen
from bs4 import BeautifulSoup
import  re
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsobj = BeautifulSoup(html, 'html.parser')
images = bsobj.find_all("img", {"src":re.compile("\.\.\/img\/gifts\/img[0-9]\.jpg")})
for image in images:
    print(image["src"])