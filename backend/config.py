from exam.wechatlogin import WX_APP_ID, WX_APP_SECRET


class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'pro': ProductionConfig,
    'default': DevelopmentConfig
}

WX_APP_ID = 'wx7bfe035eee90419b'
WX_APP_SECRET = '51ed227eed49319fa6474bc79559dc2f'