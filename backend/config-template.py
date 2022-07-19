import os
import datetime

UNIX_USERNAME = "jcav"
DB_UNIX_SOCK = r"/run/mysqld/mysqld.sock"

SESSION_HEADER = "Session"

CORS_ORIGINS = ["https://our_static_file_server_domain"]
CORS_EXPOSE_HEADERS = [SESSION_HEADER]

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
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
WX_APP_ID = "wxc32f29e7a1c08dba"
WX_APP_SECRET = "26e3ede2ebace7c238fdd43a6c0394a3"
MACHINE_ID = 0

THUWY_EMAIL_LICENSE = "xxxxxx"
WX_SUBSC_TPL_ID = "xxxxx"