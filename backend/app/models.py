from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode="utf8mb4")


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


# 太TM神奇了，python的dict没有__dict__属性，不能动态添加属性，如：
#   a = {}
#   a.foo = 10 # 报错：AttributeError
# 此时setattr也没用，因为dict重写了__setattr__
# 但自己写的类默认是有__dict__的，也就是可以setattr
# 如果自己写的类有__slot__，那么也不能动态添加，sqlachemy.engine.row.Row 就这么干的


class _Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def __getattribute__(self, name: str):
        if name in self:
            return self[name]
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name: str, value) -> None:
        self[name] = value


# 一些常用类型
from sqlalchemy import BIGINT, VARCHAR

SNOWFLAKE_ID = BIGINT
WECHAT_OPENID = VARCHAR(64)
SCHOOL_ID = VARCHAR(16)
