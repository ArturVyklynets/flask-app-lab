SECRET_KEY = "secret-key-sdsfs"

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    WTF_CSRF_ENABLED = True
    TESTING = False
    SECRET_KEY = "secret-key-sdsfs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "instance\\test-db.sqlite")
    WTF_CSRF_ENABLED = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DB_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig
}