# этот файл позволяет использовать flask-sqlalchemy не из flask-приложения
# так мы собираем новости и кладем их в базу

from webapp import create_app
from webapp.python_news import get_python_news

app = create_app()
with app.app_context():
    get_python_news()
