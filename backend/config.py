import os
import datetime

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)

    def set(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db?charset=utf8'

    def set(app):
        app.secret_key = 'dev ----'
        

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db?charset=utf8'

    def set(app):
        app.secret_key = 'test -----'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db?charset=utf8'

    def set(app):
        app.secret_key = os.urandom(24)
        
config = DevelopmentConfig
skipLoginAndBind = False
skipAdmin = True
accessKeyTimeout = 2 # 网页登陆口令超时时间

WX_APP_ID = 'wx7bfe035eee90419b'
WX_APP_SECRET = '51ed227eed49319fa6474bc79559dc2f'
MACHINE_ID = 0