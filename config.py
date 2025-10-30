import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_ADMIN = os.getenv('FLASK_ADMIN')
    FLASK_APP = os.getenv('FLASK_APP')
    API_URL = os.getenv('API_URL')
    API_KEY = os.getenv('API_KEY')
    API_FROM = os.getenv('API_FROM')
    NOME = os.getenv('NOME')
    PRONTUARIO = os.getenv('PRONTUARIO')
    EMAIL_PROF = os.getenv('EMAIL_PROF')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or 'sqlite://' 

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}