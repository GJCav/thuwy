from app import db
from flask_sqlalchemy import SQLAlchemy

# db: SQLAlchemy
# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column('id', db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     city = db.Column(db.String(100))


class Admin(db.Model):
    __tablename__ = 'admins'
    openid        = db.Column(db.Text, primary_key = True)

class User(db.Model):
    __tablename__ = "users"
    openid        = db.Column(db.Text, primary_key = True)
    schoolId      = db.Column('school_id', db.Text, unique=True)
    name          = db.Column(db.Text)
    clazz         = db.Column(db.Text)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __init__(self, openid, *args, **kwargs) -> None:
        self.openid = openid
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'User({self.name}, {self.schoolId}, {self.clazz}, {self.openid})'

class Item(db.Model):
    __tablename__ = "items"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.Text, nullable=False)
    rsvMethod     = db.Column('rsv_method', db.Integer, nullable=False)
    briefIntro    = db.Column('brief_intro', db.Text)
    thumbnail     = db.Column(db.Text)
    mdIntro       = db.Column('md_intro', db.Text)

    def toDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'brief-intro': self.briefIntro,
            'thumbnail': self.thumbnail,
            'rsv-method': self.rsvMethod,
            'rsv-info': []
        }

    # no value check on dic
    def fromDict(self, dic):
        self.name = dic['name']
        self.id = dic['id']
        self.briefIntro = dic['brief-intro']
        self.thumbnail = dic['thumbnail']
        self.rsvMethod = dic['rsv-method']

    def __repr__(self) -> str:
        return f'Item({self.name}, {self.briefIntro}, {self.id}, {self.mdIntro if len(self.mdIntro) < 30 else (self.mdIntro[:27]+"...")})'

class Reservation(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    itemId   = db.Column('item_id', db.Integer)
    guest    = db.Column(db.Text, nullable=False)
    reason   = db.Column(db.Text, nullable=False)
    method   = db.Column(db.Integer, nullable=False)
    st       = db.Column(db.Integer, nullable=False)
    ed       = db.Column(db.Integer, nullable=False)
    state    = db.Column(db.Integer, nullable=False)
    approver = db.Column(db.Text)
    examRst  = db.Column('exam_rst', db.Text)
    chore    = db.Column(db.Text)


class RsvMethodLongTimeRsv:
    methodValue = 1
    methodMask = 1
    
    morningStartHour   = 8
    morningEndHour     = 12
    morningCode        = 1
    afternoonStartHour = 13
    afternoonEndHour   = 17
    afternoonCode      = 2
    nightStartHour     = 17
    nightEndHour       = 23
    nightCode          = 3

    weekendCode = 4

class RsvMethodFlexibleTimeRsv:
    methodValue = 2
    meghodMask  = 2