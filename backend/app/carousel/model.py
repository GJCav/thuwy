from app import carouselIdPool
from app.models import db
from app.auth.model import User
import app.timetools as timestamp

class CarouselMsg(db.Model):
    __tablename__ = 'carousel'
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.Text, nullable=False)
    st = db.Column(db.Integer, nullable=False)
    ed = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    hide = db.Column(db.Integer, default=0)
    lastVerison = db.Column('last_ver', db.Integer) # 修改Carousel将会造成id变化

    def toDict(self, all=False):
        rtn = {
            'id': self.id,
            'owner': User.queryName(self.owner),
            'st': self.st,
            'ed': self.ed,
            'content': self.content
        }
        if all:
            rtn.update({
                'owner-id': self.owner,
                'hide': self.hide,
                'last-version': self.lastVerison
            })
        return rtn

    def queryCurrentMsgList():
        curTime = timestamp.now()
        return db.session.query(CarouselMsg)\
            .filter(CarouselMsg.hide == 0)\
            .filter(CarouselMsg.st <= curTime)\
            .filter(CarouselMsg.ed > curTime)\
            .all()
    
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
        return db.session.query(CarouselMsg)\
            .filter(CarouselMsg.id == id)\
            .one_or_none()
