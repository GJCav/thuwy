from flask import Blueprint
from app.auth.model import Scope

from config import DevelopmentConfig


authRouter = Blueprint("auth", __name__)
from . import api
from .api import requireScope, challengeScope


def init():
    from .model import db, User
    from config import userSysName

    Scope.define("User", "Basic user permission", True)
    PermissionAdmin = Scope.define("PermissionAdmin", "Admin for permission", True)
    UserAdmin = Scope.define("UserAdmin", "Admin for all users", True)


    userSys = User.fromOpenid(userSysName)
    if not userSys:
        userSys = User(
            openid=userSysName,
            name = userSysName,
            schoolId = userSysName,
            clazz = userSysName
        )
        db.session.add(userSys)

        userSys.entity.scopes.append(PermissionAdmin)
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
