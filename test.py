
import requests
from bs4 import BeautifulSoup
html = requests.get("http://www.pythonscraping.com/pages/warandpeace.html")
html.encoding='utf-8'
soup = BeautifulSoup(html.text, 'html.parser') #注意是html.text
titles = soup.select('h1')
for title in titles:
    print(title.text)

# select用法
peoples = soup.select('span.green')
for people in peoples:
    print(people.text)
# class=red的find_all用法
words = soup.find_all("", {"class":"red"})
for word in words:
    print(word.text)

