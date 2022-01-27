from app.models import db

from app.models import SNOWFLAKE_ID, WECHAT_OPENID, SCHOOL_ID
from sqlalchemy import INTEGER, TEXT, VARCHAR


class Admin(db.Model):
    __tablename__ = "admin"
    openid = db.Column(WECHAT_OPENID, primary_key=True)

    def fromId(id):
        return db.session.query(Admin).filter(Admin.openid == id).one_or_none()


class AdminRequest(db.Model):
    __tablename__ = "admin_req"
    id = db.Column(SNOWFLAKE_ID, primary_key=True)
    requestor = db.Column(WECHAT_OPENID)
    approver = db.Column(WECHAT_OPENID)
    state = db.Column(INTEGER)  # 0: waiting, 1: accept, 2: reject
    reason = db.Column(TEXT)

    def fromId(id):
        return (
            db.session.query(AdminRequest).filter(AdminRequest.id == id).one_or_none()
        )

    def toDict(self):
        return {
            "id": self.id,
            "requestor": User.fromOpenid(self.requestor).toDict(),
            "approver": User.queryName(self.approver),
            # 'state': self.state,
            "reason": self.reason,
        }


class User(db.Model):
    __tablename__ = "user"
    openid = db.Column(WECHAT_OPENID, primary_key=True)
    schoolId = db.Column("school_id", SCHOOL_ID, unique=True)
    name = db.Column(TEXT)
    clazz = db.Column(TEXT)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __init__(self, openid, *args, **kwargs) -> None:
        self.openid = openid
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"User({self.name}, {self.schoolId}, {self.clazz}, {self.openid})"

    def toDict(self):
        return {
            "school-id": self.schoolId,
            "name": self.name,
            "clazz": self.clazz,
            "admin": bool(Admin.fromId(self.openid)),
            "openid": self.openid,
        }

    def fromOpenid(openid):
        return db.session.query(User).filter(User.openid == openid).one_or_none()

    def queryProfile(openId):
        openId = str(openId)
        usr = db.session.query(User).filter(User.openid == openId).one_or_none()
        if usr == None:
            return None
        else:
            usr = usr.toDict()
            return usr

    def queryName(openid):
        """
        return: name of openid, none if not found.
        """

        rst = db.session.query(User.name).filter(User.openid == openid).one_or_none()
        return rst[0] if rst else None


class UserBinding(db.Model):
    __tablename__ = "user_binding"
    schoolId = db.Column("school_id", SCHOOL_ID, primary_key=True)
    name = db.Column(TEXT)
    clazz = db.Column(TEXT)
    openid = db.Column(TEXT)

    def check(schoolId, name, clazz):
        return (
            db.session.query(UserBinding)
            .filter(UserBinding.schoolId == schoolId)
            .filter(UserBinding.name == name)
            .filter(UserBinding.clazz == clazz)
            .one_or_none()
        )

    def toDict(self):
        return {
            "id": self.schoolId,
            "openid": self.openid,
            "clazz": self.clazz,
            "name": self.name,
        }

    def fromOpenId(openid):
        return (
            db.session.query(UserBinding)
            .filter(UserBinding.openid == openid)
            .one_or_none()
        )
