from os import  path

basedir = path.abspath(path.dirname(__file__))

class Config:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = '/templates'
    FLASK_APP = 'run.py'
    SECRET_KEY = "super secret key"


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

class DB():
    URL='http://db:5000'




