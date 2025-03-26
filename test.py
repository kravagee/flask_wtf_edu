from requests import *

data = {'1': 1223, '2': 765}

print(data['2'] if '2' in data.keys() else '')
print(put('http://127.0.0.1:8080/api/users/1', json={'surname': '123', 'name': '246'}))