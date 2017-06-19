import requests
from bs4 import BeautifulSoup
url = 'https://movie.douban.com/subject/26769480/comments?sort=new_score&status=P'
req = requests.get(url)
req.encoding = 'utf-8'
soup = BeautifulSoup(req.text, 'html.parser')
contents = soup.select('.comment')
rs=[]
for content in contents:
    contentX=content.text.replace('\t', '').replace('\n', '').replace(' ', '')# 去除空格、制表符和换行符
    rs.append(contentX)
    with open('daa.txt', 'a', encoding='utf-8') as f:
        f.write(contentX+'\n')
    print(contentX)
