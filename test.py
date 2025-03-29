from requests import *

print(get('127.0.0.1:8080/api/v2/users'))  # корректный
print(get('127.0.0.1:8080/api/v2/users/1'))  # корректный
print(get('127.0.0.1:8080/api/v2/users/8138'))  # некорректный запрос, пользователя нет в базе
print(get('127.0.0.1:8080/api/v2/users/qwe'))  # некорректный запрос, неверный тип данных

print(delete('127.0.0.1:8080/api/v2/users/1'))  # корректный
print(delete('127.0.0.1:8080/api/v2/users/8138'))  # некорректный запрос, пользователя нет в базе
print(delete('127.0.0.1:8080/api/v2/users/qwe'))  # некорректный запрос, неверный тип данных

print(post('127.0.0.1:8080/api/v2/users', data={'surname': 'Smith',
                                                'name': 'Mr',
                                                'age': 25,
                                                'position': 'recruit',
                                                'speciality': 'surgeon',
                                                'email': 'mrsmith@firstmail.com',
                                                'address': 'Ohio',
                                                'password': '7128jdqwue'
                                                }))  # корректный
print(post('127.0.0.1:8080/api/v2/users',
           data={'surname': 'Smith'}))  # некорректный запрос, не все необходимые данные переданы
print(post('127.0.0.1:8080/api/v2/users'))  # некорректный запрос, пустое тело запроса
print(post('127.0.0.1:8080/api/v2/users',
      data={'surname': 12}))  # некорректный запрос, неверные типы данных в теле запроса
