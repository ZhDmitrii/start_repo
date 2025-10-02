""" Задача 1.
Измерьте с помощью декоратора measure_execution_time продолжительность HTTP запроса к произвольному
url (можно взять код из первых уроков по ботам)"""

from datetime import datetime
from typing import SupportsIndex

import requests
from requests import Response


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        t_start = datetime.now()
        result = func(*args, **kwargs)
        t_finish = datetime.now()
        execution_time = t_finish - t_start
        milliseconds = round(execution_time.microseconds / 1000)
        print(f"Function completed in: "
              f"{execution_time}s {milliseconds}ms", "\n")
        return result

    return wrapper


@measure_execution_time
def send_http_request(url: str) -> Response:
    """
    Функция делает HHTP-запрос к произвольному url
    :param url: str: Адрес сайта или любого веб-ресурса
    :return: Response: Ответ на запрос
    """
    return requests.get(url)


print("Ответ на задание № 1: ")
response = send_http_request("https://google.com")
print(response.text)

""" Задача 2. 

    Описание задачи:

Необходимо разработать декоратор requires_admin, который будет использоваться для проверки роли 
пользователя перед выполнением защищенной функции. Если роль пользователя не соответствует требуемой, 
декоратор должен выбрасывать исключение PermissionError. В противном случае функция должна 
выполняться корректно.

    Пример использования:

Функция delete_user отвечает за удаление пользователей. Она должна быть доступна только для 
пользователей с ролью "admin".  Если пользователь, вызывающий эту функцию, не является администратором,
необходимо остановить выполнение функции и выбросить PermissionError.

@requires_admin
def delete_user(user, username_to_delete):
    return f"User {username_to_delete} has been deleted by {user['username']}."

# Пример юзеров
admin_user = {'username': 'Alice', 'role': 'admin'}
regular_user = {'username': 'Bob', 'role': 'user'}

# Вызовы функции
print(delete_user(admin_user, 'Charlie')) # Должно отработать
print(delete_user(regular_user, 'Charlie')) # Должно рейзить PermissionError"""


def requires_admin(func):
    def wrapper(user, *args, **kwargs):
        if user.get("role") != "admin":
            raise PermissionError("Вы не являетесь администратором, выполнение функции остановлено.")
        return func(user, *args, **kwargs)

    return wrapper


@requires_admin
def delete_user(user, username_to_delete):
    return f"Пользователь {username_to_delete} был удалён администратором {user['username']}."


# Пример юзеров
admin_user = {'username': 'Алиса', 'role': 'admin'}
regular_user = {'username': 'Боб', 'role': 'user'}

# Вызовы функции
print("-" * 30)
print("Ответ на задание № 2: ")
print(delete_user(admin_user, 'Чарли'))  # Должно отработать
# print(delete_user(regular_user, 'Чарли')) # Должно рейзить PermissionError
