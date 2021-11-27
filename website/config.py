from json import load as jload

with open('/etc/config.json') as config_file:
    config = jload(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_Port = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config.get('MAIL_USER')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')
    MAIL_RECIPIENT = config.get('MAIL_RECIPIENT')
