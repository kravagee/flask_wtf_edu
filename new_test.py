from requests import put

print(put('http://127.0.0.1:8080', data={'job': '1245',
                                         'teamleader': 2})) # корректный запрос
print(put('http://127.0.0.1:8080')) # некорректный запрос, пустое тело запроса
print(put('http://127.0.0.1:8080', data={'asdaf': 1})) # некорректный запрос, неверное имя параметра
print(put('http://127.0.0.1:8080', data={'job': True})) # некорректный запрос, неверный тип данных в запросе