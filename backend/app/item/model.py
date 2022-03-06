from typing import Text
from app.models import db

from sqlalchemy import BIGINT, INTEGER, TEXT, VARCHAR
from app.models import WECHAT_OPENID, SNOWFLAKE_ID


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(SNOWFLAKE_ID, primary_key=True)
    name = db.Column(VARCHAR(128), nullable=False)
    available = db.Column(INTEGER)
    delete = db.Column(INTEGER)
    rsvMethod = db.Column("rsv_method", INTEGER, nullable=False)
    briefIntro = db.Column("brief_intro", VARCHAR(4096))
    thumbnail = db.Column(VARCHAR(4096))
    mdIntro = db.Column("md_intro", TEXT)
    attr = db.Column(INTEGER)
    group = db.Column(VARCHAR(4096))

    class Attr:
        ATTR_AUTO_ACCEPT = 0b1  # 自动通过，自动完成

        def queryAttrById(id) -> int:
            qryRst = db.session.query(Item.attr).filter(Item.id == id).one_or_none()
            return qryRst[0] if qryRst else None

        def isAutoAccept(attr) -> bool:
            return attr & Item.Attr.ATTR_AUTO_ACCEPT

    def queryItemName(itemId):
        qryRst = db.session.query(Item.name).filter(Item.id == itemId).one_or_none()
        return qryRst[0] if qryRst else None

    def fromId(id):
        return db.session.query(Item).filter(Item.id == id).one_or_none()

    def toDict(self):
        """
        json without md-intro
        """
        return {
            "name": self.name,
            "id": self.id,
            "available": bool(self.available),
            "brief-intro": self.briefIntro,
            "thumbnail": self.thumbnail,
            "rsv-method": self.rsvMethod,
            "attr": self.attr,
            "group": self.group,
        }

    # no use
    # no value check on dic
    # def fromDict(self, dic):
    #     self.name       = dic['name']
    #     self.id         = dic['id']
    #     self.briefIntro = dic['brief-intro']
    #     self.thumbnail  = dic['thumbnail']
    #     self.rsvMethod  = dic['rsv-method']

    def querySupportedMethod(id):
        """
        return none if item not found.
        """
        qry = db.session.query(Item.rsvMethod).filter(Item.id == id).one_or_none()
        return qry[0] if qry else None

    def __repr__(self) -> str:
        return f'Item({self.name}, {self.briefIntro}, {self.id}, {self.mdIntro if len(self.mdIntro) < 30 else (self.mdIntro[:27]+"...")})'
