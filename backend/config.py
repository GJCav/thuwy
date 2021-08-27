import os
import datetime

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)

    def set(app):
        pass
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
        
config = ProductionConfig
skipLoginAndBind = False
skipAdmin = False
userSysName = 'system'  # 默认添加一个 system 管理员，处理定时任务

WX_APP_ID = 'wx7bfe035eee90419b'
WX_APP_SECRET = '51ed227eed49319fa6474bc79559dc2f'
MACHINE_ID = 0