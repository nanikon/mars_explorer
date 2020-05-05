from requests import get, post, delete

# примеры использования API для таблицы User
# получение записи/записей
"""print(get('http://127.0.0.1:8080/api/v2/users').json())  # Получение всех пользователей
print(get('http://127.0.0.1:8080/api/v2/users/1').json())  # Корректное получение одного пользователя по id
print(get('http://127.0.0.1:8080/api/v2/users/50').json())  # Ошибочный запрос получения одного пользователя — неверный id
print(get('http://127.0.0.1:8080/api/v2/users/andry').json())  # Ошибочный запрос получения одного пользователя — строка
print()
# добавление записи
print(post('http://127.0.0.1:8080/api/v2/users').json())  # Ошибочный запрос - пустой
print(post('http://127.0.0.1:8080/api/v2/users',
           json={'id': 3,
                 'surname': 'Nikonova',
                 'name': 'Natalia',
                 'age': 17,
                 'address': 'module_2',
                 'password': 'true'}).json())  # Ошибочный запрос - недостаточное количество параметров
print(post('http://127.0.0.1:8080/api/v2/users',
           json={'id': 3,
                 'surname': 'Nikonova',
                 'name': 'Natalia',
                 'age': 17,
                 'position': 'junior scientist',
                 'speciality': 'programist',
                 'address': 'module_2',
                 'city_from': 'Sochi',
                 'password': 'true',
                 'email': 'nik@mars.org'}).json())  # Ошибочный запрос - уже существующий id
print(post('http://127.0.0.1:8080/api/v2/users',
           json={'id': 6,
                 'surname': 'Nikonova',
                 'name': 'Natalia',
                 'age': 17,
                 'position': 'junior scientist',
                 'speciality': 'programist',
                 'address': 'module_2',
                 'city_from': 'Sochi',
                 'password': 'true',
                 'email': 'nik@mars.org'}).json())  # Корректный запрос на добавление
print(get('http://127.0.0.1:8080/api/v2/users').json())  # Получение всех работ (проверка)
print()
# удаление записи по id
print(delete('http://localhost:8080/api/v2/users/').json())  # Ошибочный запрос - пустой
print(delete('http://localhost:8080/api/v2/users/50').json())  # Ошибочный запрос - пользователя с таким id нет
print(delete('http://localhost:8080/api/v2/users/nikonova').json())  # Ошибочный запрос - строка
print(delete('http://localhost:8080/api/v2/users/6').json())  # Корректный запрос
print(get('http://127.0.0.1:8080/api/v2/users').json())  # Получение всех работ  """

# примеры использования API для таблицы Jobs
# получение записи/записей
print(get('http://127.0.0.1:8080/api/v2/jobs').json())  # Получение всех работ
print(get('http://127.0.0.1:8080/api/v2/jobs/1').json())  # Корректное получение одной работы
print(get('http://127.0.0.1:8080/api/v2/jobs/50').json())  # Ошибочный запрос на получение одной работы — неверный id
print(get('http://127.0.0.1:8080/api/v2/jobs/development').json())  # Ошибочный запрос на получение одной работы — строка
print()
# добавление записи
print(post('http://127.0.0.1:8080/api/v2/jobs').json())  # Ошибочный запрос - пустой
print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'job': 'aaaaa',
                 'team_leader_id': 1,
                 'work_size': 12,
                 'collaborators': '2, 3, 4, 5, 100'}).json())  # Ошибочный запрос - недостаточное количество параметров
print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'id': 3,
                 'job': 'aaaaa',
                 'team_leader_id': 1,
                 'work_size': 12,
                 'collaborators': '2, 3, 4, 5, 100',
                 'is_finished': True,
                 'categories_id': '1, 2, 3'}).json())  # Ошибочный запрос - уже существующий id
print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'id': 6,
                 'job': 'aaaaa',
                 'team_leader_id': 1,
                 'work_size': 12,
                 'collaborators': '2, 3, 4, 5, 100',
                 'is_finished': True,
                 'categories_id': '1, 2, 3'}).json())  # Корректный запрос на добавление
print(get('http://127.0.0.1:8080/api/v2/jobs').json())  # Получение всех работ (проверка)
print()
# удаление записи по id
print(delete('http://localhost:8080/api/v2/jobs/').json())  # Ошибочный запрос - пустой
print(delete('http://localhost:8080/api/v2/jobs/50').json())  # Ошибочный запрос - работы с таким id нет
print(delete('http://localhost:8080//api/v2/jobs/analysis').json())  # Ошибочный запрос - строка
print(delete('http://localhost:8080/api/v2/jobs/6').json())  # Корректный запрос
print(get('http://127.0.0.1:8080/api/v2/jobs').json())  # Получение всех работ (проверка)
print()
