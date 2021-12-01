""" Application configuration settings. """
from json import load as jload
from sys import platform

if platform == "win32":
    file = "c:\\config.json"
else:
    file = "/etc/config.json"

with open(file) as config_file:
    config = jload(config_file)


class Config:
    """ Application Variables. """
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_Port = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config.get("MAIL_USER")
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")
    MAIL_RECIPIENT = config.get("MAIL_RECIPIENT")
