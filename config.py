import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    Testing = False
    CSRF_ENABLED = True
    SECRET_KEY = 'Fnwnownvwowi242e54@@@IS%&^%$£&%7'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = ''
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/lifeat'

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/lifeat'

    SESSION_COOKIE_SECURE = False