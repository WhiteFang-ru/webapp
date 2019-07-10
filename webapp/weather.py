# добавим обработку исключений. ЭТО БАЗОВАЯ ГИГИЕНА ПРОГРАММИСТА, БЕЗ НЕЕ НЕ БЕРУТ НА РАБОТУ
# исключение надо добавлять перед той частью кода, которая выдает ошибку:
# 1) отсоединяемся от интернета ->
# Traceback (most recent call last):
#   File "API_and_weather.py", line 31, in <module>
#     print(weather_by_city('Moscow, Russia'))
#   File "API_and_weather.py", line 18, in weather_by_city
#     result = requests.get(weather_url, params= params)
# 2) отдаем неверный адрес сайта для обработки запроса (-> 404)  ->
#   json.decoder.JSONDecodeError: Expecting value...
#   File "weatherweather.py", line 25, in weather_by_city
#     weather = result.json()

from flask import current_app  # так мы обращаемся к текущему flask-приолжению
import requests

def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'key': current_app.config['WEATHER_API_KEY'],  # '89c2900d5e6843f49da170013191706' - ранний вариант, до config
        'q': city_name,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'ru'
    }
    try:                # если все пойдет хорошо
        result = requests.get(weather_url, params= params)
        result.raise_for_status()    # обработка ошибок на сервере погоды. Вызов raise_for_status сгенерирует exception
                                     # если сервер ответил кодом, начинающимся с 4xx или 5xx
        weather = result.json()     # Сервер может прислать некорректно сформированный результат (JSON).
                                    # тогда на строчке return result.json() мы получим exception ValueError
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):  # если все пойдет не очень
        print('Сетевая ошибка')  # для себя
        return False             # для сетевого клиента
    return False

if __name__ == '__main__':
    print(weather_by_city('Moscow, Russia'))


# варианты ответов сервера на запросы клиента:
# 200 - все отлично  (любые двухсотые коды)
# 301 - страница перемещена на другой адрес (коды 301, 302 и др)
# 401 - нужно авторизоваться
# 404 - страница не найдена
# 500 - на сервере произошла ошибка (можно его увидеть, если из application.py убрать debug=True,
#                                    из weatherweather.py убрать ValueError и задать неверный адрес страницы для запроса)
# Ошибка 500 выглядит так: Internal Server Error
#                          The server encountered an internal error and was unable to complete your request.
#                          Either the server is overloaded or there is an error in the application (в браузере)