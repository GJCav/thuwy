import enum
from typing import Dict, Set

from flask import current_app

from app import app
from app.models import db
from app import timetools as T
from app.models import WECHAT_OPENID, SCHOOL_ID
from sqlalchemy import BIGINT, TEXT, BigInteger, Column, Enum, ForeignKey, Integer, String, Table, and_, func, or_
from sqlalchemy.orm import relationship

SCOPE_STR = String(64, collation="utf8_bin")

EntityAssociation = Table(
    "entity_association", db.Model.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("group_id", ForeignKey("entity.id")),
    Column("member_id", ForeignKey("entity.id")),
    Column("expire_at", BIGINT, default=0)
)

Permission = Table(
    "permission", db.Model.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("entity_id", ForeignKey("entity.id")),
    Column("scope_name", ForeignKey("scope.name")),
    Column("expire_at", BIGINT, default=0)
)


class EntityType(enum.Enum):
    Role = 0
    Group = 1


class Entity(db.Model):
    __tablename__ = "entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    type = Column(Enum(EntityType), default=EntityType.Role)
    expire_at = Column(BigInteger, default=0)       # 超时自动失效

    members = relationship(
        lambda: Entity, 
        secondary = EntityAssociation, 
        primaryjoin = and_(
            id == EntityAssociation.c.group_id,
            or_(
                EntityAssociation.c.expire_at == 0,
                EntityAssociation.c.expire_at > func.unix_timestamp() * 1000
            )
        ),
        secondaryjoin = and_(
            id == EntityAssociation.c.member_id,
            or_(
                EntityAssociation.c.expire_at == 0, 
                EntityAssociation.c.expire_at > func.unix_timestamp() * 1000
            )
        ),
        backref="groups"
    )

    # groups, see members
    
    scopes = relationship(
        lambda: Scope,
        secondary = Permission,
        primaryjoin = and_(
            id == Permission.c.entity_id,
            or_(
                Permission.c.expire_at == 0,
                Permission.c.expire_at > func.unix_timestamp() * 1000
            )
        ),
        secondaryjoin = lambda: and_(
            Permission.c.scope_name == Scope.name,
            or_(
                Permission.c.expire_at == 0,
                Permission.c.expire_at > func.unix_timestamp() * 1000
            )
        ),
        backref="entities"
    )

    @property
    def privileges(self) -> Set[str]:
        """
        返回该实体具备的所有权限
        """
        return set([s.name for s in self.scopes])

    @property
    def group_privileges(self) -> Dict[str, set]:
        """
        返回该实体所在组的权限，以字典的形式
        """
        rtn = {}
        for g in self.groups:
            rtn[g.name] = set([s.name for s in g.scopes])
        return rtn

    @property
    def all_privileges(self) -> Set[str]:
        """
        返回该实体、及该实体所在组的所有权限
        """
        rtn = self.privileges
        for k in self.group_privileges:
            rtn |= self.group_privileges[k]
        return rtn

    def __str__(self):
        return f"{self.name}"


class Scope(db.Model):
    __tablename__ = "scope"
    
    name = Column(SCOPE_STR, primary_key=True)
    description = Column(String(256), default="")
    create_time = Column(BigInteger, default=lambda: T.now())

    # entities, see Entity.scopes

    @staticmethod
    def fromName(name):
        return db.session.query(Scope).filter(Scope.name == name).one_or_none()

    
    @staticmethod
    def define(name, des="", suppress_warning=False):
        exist = Scope.fromName(name)
        if exist:
            if not suppress_warning:
                from app.ColorConsole import Yellow
                print(f"{Yellow('Warning: ')} duplicate scope name: {name}")
            return exist
        
        r = Scope(name=name, description=des)
        db.session.add(r)
        db.session.commit()
        return r


class User(db.Model):
    __tablename__ = "user"
    openid = db.Column(WECHAT_OPENID, primary_key=True)
    schoolId = db.Column("school_id", SCHOOL_ID, unique=True)
    name = db.Column(TEXT)
    clazz = db.Column(TEXT)
    email = db.Column(String(64))

    entity_id = db.Column(ForeignKey(Entity.id))

    entity = relationship(Entity)


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.entity == None:
            self.entity = Entity(name=self.openid+"_entity")
            self.entity.scopes.append(Scope.fromName("User"))


    def __repr__(self) -> str:
        return f"User({self.name}, {self.schoolId}, {self.clazz}, {self.openid})"


    def toDict(self):
        return {
            "school-id": self.schoolId,
            "name": self.name,
            "clazz": self.clazz,
            "openid": self.openid,
            "privilege_info": self.privilege_info
        }


    def fromOpenid(openid) -> "User":
        return db.session.query(User).filter(User.openid == openid).one_or_none()


    def queryName(openid):
        """
        return: name of openid, none if not found.
        """

        rst = db.session.query(User.name).filter(User.openid == openid).one_or_none()
        return rst[0] if rst else None

    @property
    def privileges(self):
        return self.entity.privileges if self.entity else set()

    @property
    def group_privileges(self):
        return self.entity.group_privileges if self.entity else dict()

    
    @property
    def all_privileges(self):
        return self.entity.all_privileges if self.entity else set()

    @property
    def privilege_info(self):
        return {
            "privileges": self.entity.privileges,
            "group_privileges": self.entity.group_privileges
        } if self.entity else {}


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
