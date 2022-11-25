from os import  path

basedir = path.abspath(path.dirname(__file__))

class Config:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = '/main/templates'
    FLASK_APP = 'run.py'
    SECRET_KEY = "super secret key"


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DB:
    MySQL_API_URL='http://20.48.237.189:5000'
    MySQL_URL = '20.48.237.189'
    IoT_ip = "20.104.197.37"
    IoT_port = "6667"
    IoT_username = "root"
    IoT_password = "root"
    IoT_zone ="UTC-5"
    need_init = True
    IoT_API_URL='http://20.104.197.37:5000'
    URL = '20.48.237.189'