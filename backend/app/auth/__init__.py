from flask import Blueprint

from config import DevelopmentConfig


authRouter = Blueprint("auth", __name__)
from . import api
from .api import requireScope, challengeScope


def init():
    from .model import db, User, Privilege, Scope
    from config import userSysName

    scopes = [
        {"scope": "profile", "des": "基本用户信息"},
        {"scope": "admin", "des": "管理员权限"},
        {"scope": "teacher", "des": "教师权限"},
        {"scope": "monitor", "des": "班长权限"},
        {"scope": "*", "des": "获取用户具有的所有权限"}
    ]
    for e in scopes:
        scope = Scope.fromScopeStr(e["scope"])
        if not scope:
            scope = Scope()
            scope.scope = e["scope"]
            scope.description = e["des"]
            db.session.add(scope)
    db.session.commit()

    userSys = User.fromOpenid(userSysName)
    if not userSys:
        userSys = User(userSysName)
        userSys.openid = userSysName
        userSys.name = userSysName
        userSys.schoolId = userSysName
        userSys.clazz = userSysName
        db.session.add(userSys)

        sysAdminPrivilege = Privilege()
        sysAdminPrivilege.openid = userSys.openid
        sysAdminPrivilege.scope = (
            db.session.query(Scope).filter(Scope.scope == "admin").one_or_none()
        )
        db.session.add(sysAdminPrivilege)
        db.session.commit()

    from config import config
    if config == DevelopmentConfig:
        # 创建测试账号
        normalUser = User.fromOpenid("normal_user")
        if not normalUser:
            normalUser = User("normal_user")
            normalUser.name = "normal_user"
            normalUser.schoolId = "2020018888"
            normalUser.clazz = "未央-测试01"
            db.session.add(normalUser)
            db.session.commit()

        superAdmin = User.fromOpenid("super_admin")
        if not superAdmin:
            superAdmin = User("super_admin")
            superAdmin.name = "super_admin"
            superAdmin.schoolId = "2020019999"
            superAdmin.clazz = "未央-测试02"
            db.session.add(superAdmin)

            for e in scopes:
                pri = Privilege()
                pri.openid = superAdmin.openid
                pri.scopeId = Scope.fromScopeStr(e["scope"]).id
                db.session.add(pri)
            db.session.commit()
