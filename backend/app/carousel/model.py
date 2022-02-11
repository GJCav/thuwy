from app import carouselIdPool
from app.models import db
from app.auth.model import User
import app.timetools as timestamp

from sqlalchemy import BIGINT, INTEGER, TEXT
from app.models import WECHAT_OPENID, SNOWFLAKE_ID


class CarouselMsg(db.Model):
    __tablename__ = "carousel"
    id = db.Column(SNOWFLAKE_ID, primary_key=True)
    owner = db.Column(WECHAT_OPENID, nullable=False)
    st = db.Column(BIGINT, nullable=False)
    ed = db.Column(BIGINT, nullable=False)
    content = db.Column(TEXT)
    hide = db.Column(INTEGER, default=0)
    lastVerison = db.Column("last_ver", SNOWFLAKE_ID)  # 修改Carousel将会造成id变化

    def toDict(self, all=False):
        rtn = {
            "id": self.id,
            "owner": User.queryName(self.owner),
            "st": self.st,
            "ed": self.ed,
            "content": self.content,
        }
        if all:
            rtn.update(
                {
                    "owner-id": self.owner,
                    "hide": self.hide,
                    "last-version": self.lastVerison,
                }
            )
        return rtn

    def queryCurrentMsgList():
        curTime = timestamp.now()
        return (
            db.session.query(CarouselMsg)
            .filter(CarouselMsg.hide == 0)
            .filter(CarouselMsg.st <= curTime)
            .filter(CarouselMsg.ed > curTime)
            .all()
        )

    def clone(self):
        """
        Example:
            new = oldCarouselMsg.createModificationClone()
            new.st = ...
            ...

            oldCarouselMsg.hide = True
            new.lastVersion = oldCarouselMsg.id

            db.session.add(new) # dont forget this line.
            db.session.commit()
        """
        new = CarouselMsg()
        new.id = carouselIdPool.next()
        new.owner = self.owner
        new.st = self.st
        new.ed = self.ed
        new.content = self.content
        new.hide = self.hide
        new.lastVerison = self.lastVerison
        return new

    def queryById(id):
        return db.session.query(CarouselMsg).filter(CarouselMsg.id == id).one_or_none()
