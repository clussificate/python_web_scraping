import requests
files = {'uploadFile': open('1.jpg', 'rb')}
r = requests.post("http://www.pythonscraping.com/files/processing2.php", files=files)
print(r.text)