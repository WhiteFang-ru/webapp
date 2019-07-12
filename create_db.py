from webapp import db, create_app

db.create_all(app=create_app())  # прошу db создать ВСЕ модели для этого приложения