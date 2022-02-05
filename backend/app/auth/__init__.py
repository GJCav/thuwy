from flask import Blueprint


authRouter = Blueprint("auth", __name__)
from . import api
from .api import requireScope


def init_sys_account():
    from .model import db, User, Privilege, Scope
    from config import userSysName

    scopes = [
        {"scope": "profile", "des": "基本用户信息"},
        {"scope": "admin", "des": "管理员权限"},
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
        userSys.name = userSysName
        userSys.schoolId = userSysName
        userSys.clazz = userSysName
        db.session.add(userSys)

        sysAdminPrivilege = Privilege()
        sysAdminPrivilege.openid = userSys.name
        sysAdminPrivilege.scope = (
            db.session.query(Scope).filter(Scope.scope == "admin").one_or_none()
        )
