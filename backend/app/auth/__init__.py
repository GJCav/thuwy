from app import app
from . import header_session
header_session.patch_session(app)

from flask import Blueprint
from config import DevelopmentConfig

authRouter = Blueprint("auth", __name__)

from . import api
from .api import requireScope, challengeScope # 其他模块可直接从次导出


def init():
    with app.app_context():
        from .model import db, User
        from config import userSysName
        from .scope_def import ScopeAdmin, UserAdmin

        userSys = User.fromOpenid(userSysName)
        if not userSys:
            userSys = User(
                openid=userSysName,
                name = userSysName,
                schoolId = userSysName,
                clazz = userSysName
            )
            db.session.add(userSys)

            userSys.entity.scopes.append(ScopeAdmin)
            userSys.entity.scopes.append(UserAdmin)
            
            db.session.commit()

        from config import config
        if config == DevelopmentConfig:
            # 创建测试账号
            normalUser = User.fromOpenid("normal_user")
            if not normalUser:
                normalUser = User(
                    name = "normal_user",
                    openid = "normal_user",
                    schoolId = "2020018888",
                    clazz = "未央-测试01",
                )
                db.session.add(normalUser)
                db.session.commit()

init()