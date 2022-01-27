from flask import Blueprint

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
    db.session.commit()
