from flask import Blueprint

from app.auth.model import Scope

authRouter = Blueprint("auth", __name__)
from . import api
from .api import requireLogin, requireBinding, requireAdmin


def init_sys_account():
    from .model import db, User, Admin
    from config import userSysName

    userSys = User.fromOpenid(userSysName)
    if not userSys:
        userSys = User(userSysName)
        userSys.name = userSysName
        userSys.schoolId = userSysName
        userSys.clazz = userSysName
        db.session.add(userSys)
    
    adminSys = Admin.fromId(userSysName)
    if not adminSys:
        adminSys = Admin()
        adminSys.openid = userSysName
        db.session.add(adminSys)

    scopes = [
        {'scope': 'profile', 'des': '基本用户信息'},
        {'scope': 'admin', 'des': '管理员权限'},
    ]
    for e in scopes:
        scope = Scope.fromScopeStr(e['scope'])
        if not scope:
            scope = Scope()
            scope.scope = e['scope']
            scope.description = e['des']
            db.session.add(scope)
        
    db.session.commit()
    
