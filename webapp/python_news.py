# ПАРСИМ НОВОСТНУЮ СТРАНИЦУ
# 1) смотрю исходный код страницы, которую нужно спарсить (правая кнопка мыши)
# 2) в исходном коде они выглядят так: поиск по 'Latest News', в body есть <div class="most-recent-posts"> , далее
# <h3 class="event-title"><a href="http://feedproxy.google.com/~r/PythonInsider/~...
# (ссылка, через которую привязана новость)
# ul - маркированный список (в нем пункты обозначаются точками) + к нему применен CSS для визуально более приятного
# отображения. li - это один эл-т списка. h3 - заголовок новости. внутри ссылка и название новости
# (Python 3.7.4 is now available</a></h3>). p - параграф (в нашем случае это текст с новой строки),
# в него заложена дата публикации новости
# 3) копирую исходный текст с помощью requests

from bs4 import BeautifulSoup
from datetime import datetime
import requests
from webapp.model import db, News


def get_html(url):
    try:
        result = requests.get(url) # при помощи requests берем данные из этого url
        result.raise_for_status()  # обрабатываем исключения
        return result.text          # 'текст' здесь - это контент страницы, которую парсим
    except(requests.RequestException, ValueError):   # 1 - если сетевая проблема, 2 - если сработал raise_for_status()
                                                    # из-за проблемы на сервере
        print('Сетевая ошибка')  # по-хорошему надо выходить не через принт, а через логирование
        return False

def get_python_news():
    html = get_html("https://www.python.org/blogs/")  # функцию 'get_html' вызываем сразу внутри этой, чтобы не надо было вызывать 2 фукнции в 'application'
    if html:
        soup = BeautifulSoup(html, 'html.parser')  # создаем дерево soup, преобразованный из html. В нем можно делать поиск
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')   # ищем нужный нам эл-т, а именно: <ul class="list-recent-posts menu">
            # findAll возвращает ВСЕ эл-ты искомого вида. class_ с подчеркиванием, потому что это очень частый атрибут
            # из вытащенного полного 'ul' блока выгрызаем все 'li' (т е собственно текст новостей). Получаем список из 'li'
            # print(all_news)
        # result_news = []  # список для коллекционирования новостей (ранняя редакция)
        for news in all_news:  # кроме самой новости нам нужны: заголовок, дата публикации
            title = news.find('a').text  # заголовок новости в исходном коде лежит внутри 'h3 -> a + link'
                # text - это то, что между открывающим и закрывающим тегом
                # print(title)
            url = news.find('a')['href']  #  ссылка на текст новости, вытаскиваем из атрибута href как из эл-та словаря
            published = news.find('time').text  # 'text' это property, поэтому запрашивается через точку. Время в формате 'string'
            try:
                published = datetime.strptime(published, '%B %d, %Y')  #  переводим время в формат 'datetime'
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)  # вызываем функцию сохранения новости в БД
            # result_news.append({   # в список добавляем все 3 хар-ки новости через append({СЛОВАРЬ})
            #     'title': title,
            #     'url': url,
            #     'published': published
            # })
        # return result_news   #  получаем список из словарей, проверяем результат через 'print'

    # return False

# после if html задается это действие, так генерится файл .html с исходным кодом страницы, которую мы парсим
            # with open("python_org_news.html", "w", encoding="utf-8") as f:
            #     f.write(html)
def save_news(title, url, published):  # задаю функцию для записи новости в БД
    news_exists = News.query.filter(News.url == url).count()   # проверяем, есть ли новость уже в БД (по уникальному url):
        # query - делает выборку News, filter ограничивает эту выборку, count считает кол-во новостей с таким url
    print(news_exists)
    if not news_exists:
        new_News = News(title=title, url=url, published=published) # кладем новый объект класса 'News' в переменную, id и text
                                                # прописывать не нужно, потому что id БД формирует сама, а text - nullable
        db.session.add(new_News)  # сохраняем объект класса 'News' в БД: кладем его в сессию SQLAlchemy
        db.session.commit()  # после commit новость по факту сохранилась в мою БД


# BeautifulSoup форрмирует из строки (которую мы скачали) "дом-дерево", т е дерево эл-тов (мы по ним можем делать поиск,
# добавлять новые эл-ты, удалять старые). Нам сейчас нужен поиск и получение контента
# BS исправляет часть огрехов html-документов (html - очень нестрогий формат. BS нивелирует такие вещи как незакрытые теги и пр
# все, что наворочено в функции get_python_news(html), взято из структуры исходного кода веб-страницы

# strptime (т е string parse time) парсит строку datetime по формату, который мы задали
