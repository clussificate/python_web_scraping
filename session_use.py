import requests
session = requests.session()

paras = {'username': 'username', 'password': 'password'}
s = session.post('http://pythonscraping.com/pages/cookies/welcome.php', paras)
print('Cookie is set to :')
print(s.cookies.get_dict())
print('--------------------')
print('Going to profile page')
s = session.get('http://pythonscraping.com/pages/cookies/profile.php') #使用Session进入下一个界面
print(s.text)