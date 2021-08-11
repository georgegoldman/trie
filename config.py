import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # app defaults config
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    OAUTHLIB_INSECURE_TRANSPORT= os.environ.get('OAUTHLIB_INSECURE_TRANSPORT')
    
    # database uri
    DEBUG= os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO')

    # jwt confg

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
    JWT_DECODE_ALGORITHMS = os.environ.get('JWT_DECODE_ALGORITHMS')
    

class ProductionConfig(Config):

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SESSION_COOKIE_SECURE = False