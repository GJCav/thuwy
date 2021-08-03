import os

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def set(app):
        app.secret_key = os.urandom(24)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'

    def set(app):
        app.secret_key = os.urandom(24)
        

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

    def set(app):
        app.secret_key = os.urandom(24)
        

config = DevelopmentConfig

WX_APP_ID = 'wx7bfe035eee90419b'
WX_APP_SECRET = '51ed227eed49319fa6474bc79559dc2f'
MACHINE_ID = 0