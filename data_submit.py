import requests
datas = {'firstname':'Ryan', 'lastname':'Mitchell'}
r = requests.post('http://pythonscraping.com/pages/files/processing.php', data=datas)
print(r.text)