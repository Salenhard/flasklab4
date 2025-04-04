from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app

# создаем расширение
db = SQLAlchemy()
ma = Marshmallow(app)
# конфигурируем базу данных SQLite в папке instance приложения
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///structure.db"

# инициализируем приложение с расширением
db.init_app(app)