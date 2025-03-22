from datetime import datetime

from requests import post

# В теле запроса пусто (некорректный запрос)
print(post('http://127.0.0.1:8080/api/jobs', json={}))

# Неполный запрос, не хватает данных (некорректный запрос)
print(post('http://127.0.0.1:8080/api/jobs', json={'teamleader': 1}))

# В запросе указан неверный тип данных (некорректный запрос)
print(post('http://127.0.0.1:8080/api/jobs', json={'teamleader': 'Joe'}))

# Корректный запрос
print(post('http://127.0.0.1:8080/api/jobs', json={'teamleader': 1,
                                                        'job': 'some job',
                                                        'work_size': 23,
                                                        'collaborators': '2, 3',
                                                        'start_date': datetime.now(),
                                                        'end_date': datetime.now()}))

'''print(post('http://127.0.0.1:8080/api/jobs').json())
print(get('http://127.0.0.1:8080/api/jobs/1').json())
print(get('http://127.0.0.1:8080/api/jobs/999').json())
print(get('http://127.0.0.1:8080/api/jobs/qwe').json())'''