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