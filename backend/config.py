import os
import datetime

UNIX_USERNAME = "jcav"
DB_UNIX_SOCK = r"/run/mysqld/mysqld.sock"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SCHEDULER_TIMEZONE = "Asia/Shanghai"

    def set(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://%s@/thuwy_dev?unix_socket=%s&charset=utf8mb4"
        % (UNIX_USERNAME, DB_UNIX_SOCK)
    )

    def set(app):
        app.secret_key = "dev ----"


class TestingConfig(Config):
    TESTING = True
    ENABLE_TEST_ACCOUNT = False
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://%s@/thuwy?unix_socket=%s&charset=utf8mb4"
        % (UNIX_USERNAME, DB_UNIX_SOCK)
    )

    def set(app):
        app.secret_key = os.urandom(24)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://%s@/thuwy?unix_socket=%s&charset=utf8mb4"
        % (UNIX_USERNAME, DB_UNIX_SOCK)
    )

    def set(app):
        app.secret_key = os.urandom(24)


config = DevelopmentConfig
userSysName = "system"  # 默认添加一个 system 管理员，处理定时任务

# 这两个数据是测试号
WX_APP_ID = "wxe7ad44246de39b1c"
WX_APP_SECRET = "130e4ff26bfe7bd283bf6e0294b4665e"
MACHINE_ID = 0
