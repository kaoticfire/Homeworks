from os import getenv


class Config:
    DB_NAME = 'database.db'
    DB_NAME = getenv('WEB_FLASK_DB')
    SECRET_KEY = getenv('FLASK_SECRET')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_Port = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAIL_USER')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
