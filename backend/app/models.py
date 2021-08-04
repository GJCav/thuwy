from operator import and_
from app import db
from sqlalchemy import or_, and_
import json as Json

from . import timetools as timestamp

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

    def toDict(self):
        return {
            'school-id': self.schoolId,
            'name': self.name,
            'clazz': self.clazz
        }

    def queryName(openid):
        """
        return: name of openid, none if not found.
        """

        rst = db.session\
            .query(User.name)\
            .filter(User.openid == openid)\
            .one_or_none()
        return rst[0] if rst else None

class Item(db.Model):
    __tablename__ = "items"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.Text, nullable=False)
    available     = db.Column(db.Integer)
    delete        = db.Column(db.Integer)
    rsvMethod     = db.Column('rsv_method', db.Integer, nullable=False)
    briefIntro    = db.Column('brief_intro', db.Text)
    thumbnail     = db.Column(db.Text)
    mdIntro       = db.Column('md_intro', db.Text)

    def toDict(self):
        """
        json without md-intro
        """
        return {
            'name': self.name,
            'id': self.id,
            'available': bool(self.available),
            'brief-intro': self.briefIntro,
            'thumbnail': self.thumbnail,
            'rsv-method': self.rsvMethod
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

    def hasTimeConflict(self):
        # 不支持连续小于号
        # cdn = {or_(
        #     self.st <= Reservation.st < self.ed,
        #     self.st <= Reservation.ed < self.ed,
        #     Reservation.st <= self.st < Reservation.ed,
        # )}

        cdn = {or_(
            and_(Reservation.st >= self.st, Reservation.st < self.ed),
            and_(Reservation.ed >= self.st, Reservation.ed < self.ed),
            and_(Reservation.st <= self.st, Reservation.ed >= self.ed)
        )}

        conflict = db.session\
            .query(Reservation.st, Reservation.ed) \
            .filter(Reservation.itemId == self.itemId)\
            .filter(*cdn) \
            .first() != None

        return conflict

    def fromRsvId(rsvId):
        return db.session\
            .query(Reservation)\
            .filter(Reservation.id == rsvId)\
            .one_or_none()


class LongTimeRsv:
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

    weekendStartHour   = 0
    weekendCode = 4

    def parseInterval(interval: str) -> tuple or None:
        """
        return: (st, ed) timestamp, 
                or (None, None) if format of interval is wrong
                or (None, -1) if interval is invalid
        """
        dateStr, codeStr = interval.split(' ')
        try:
            code = int(codeStr)
        except:
            return (None, None)
        
        st, ed = None, None
        try:
            if code == LongTimeRsv.morningCode:
                st = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.morningStartHour
                )
                ed = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.morningEndHour
                )
            elif code == LongTimeRsv.afternoonCode:
                st = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.afternoonStartHour
                )
                ed = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.afternoonEndHour
                )
            elif code == LongTimeRsv.nightCode:
                st = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.nightStartHour
                )
                ed = timestamp.hoursAfter(
                    timestamp.dateToTimestamp(dateStr),
                    LongTimeRsv.nightEndHour
                )
            elif code == LongTimeRsv.weekendCode:
                st = timestamp.dateToTimestamp(dateStr)
                if timestamp.getWDay(st) != 6:
                    return (None, -1)  # means dateStr is invalid as it should be a Saturday.
                ed = timestamp.daysAfter(st, 2)
        except:
            pass # this means the format of dateStr is wrong..

        return (st, ed)

    def timestamp2Interval(st) -> str:
        """
        timestamp to str
        """
        dateStr = timestamp.getDate(st)
        hour = timestamp.getHour(st)
        if hour == LongTimeRsv.morningStartHour:
            return f'{dateStr} {LongTimeRsv.morningCode}'
        elif hour == LongTimeRsv.afternoonStartHour:
            return f'{dateStr} {LongTimeRsv.afternoonCode}'
        elif hour == LongTimeRsv.nightStartHour:
            return f'{dateStr} {LongTimeRsv.nightCode}'
        elif hour == LongTimeRsv.weekendStartHour:
            return f'{dateStr} {LongTimeRsv.weekendCode}' 

    def getInterval(rsv: Reservation):
        rsv = LongTimeRsv.getFatherRsv(rsv)
        interval = []
        interval.append(LongTimeRsv.timestamp2Interval(rsv.st))
        for rsvId in Json.loads(rsv.chore)['group-rsv']['sub-rsvs']:
            st = db.session\
                .query(Reservation.st)\
                .filter(Reservation.id == rsvId)\
                .one()[0]
            interval.append(LongTimeRsv.timestamp2Interval(st))
        return interval

    def getFatherRsv(rsv: Reservation):
        choreJson: dict = Json.loads(rsv.chore)
        if 'sub-rsvs' in choreJson['group-rsv']:
            return rsv
        else:
            return db.session\
                .query(Reservation)\
                .filter(Reservation.id == choreJson['group-rsv']['fth-rsv'])\
                .one()

    def toDict(rsv: Reservation):
        if rsv.method != LongTimeRsv.methodValue:
            raise ValueError(f'this is not a long time reservation. id: {rsv.id}')

        rsvDict = {
            'id': rsv.id,
            'item-id': rsv.itemId,
            'guest': User.queryName(rsv.guest),
            'reason': rsv.reason,
            'method': rsv.method,
            'state': rsv.state,
            'interval': LongTimeRsv.getInterval(rsv),
            'approver': User.queryName(rsv.approver),
            'exam-rst': rsv.examRst
        }
        return rsvDict

class FlexTimeRsv:
    methodValue = 2
    methodMask  = 2

    def parseInterval(interval: str):
        """
        return: (st, ed) or (None, None) if format of interval is wrong
        """
        try:
            dateStr, durationStr = interval.split(' ')
            stStr, edStr = durationStr.split('-')
            datePart = timestamp.dateToTimestamp(dateStr)
            toArgs = lambda x: [int(e) for e in x.split(':')]

            st = timestamp.clockAfter(datePart, *toArgs(stStr))
            ed = timestamp.clockAfter(datePart, *toArgs(edStr))

            return (st, ed)
        except:
            return (None, None) # TODO: 这里的检查可以更精细些，区分INVALID和FORMAT两种错误

    def timestamp2Interval(st, ed):
        dateStr = timestamp.getDate(st)
        H = timestamp.getHour
        M = timestamp.getMins
        return f'{dateStr} {H(st)}:{M(st)}-{H(ed)}:{M(ed)}'


    def toDict(rsv: Reservation):
        if rsv.method != FlexTimeRsv.methodValue:
            raise ValueError(f'this is not a flexiable time reservation. id: {rsv.id}')
        rsvDict = {
            'id': rsv.id,
            'item-id': rsv.itemId,
            'guest': User.queryName(rsv.guest),
            'reason': rsv.reason,
            'method': rsv.method,
            'state': rsv.state,
            'interval': FlexTimeRsv.timestamp2Interval(rsv.st, rsv.ed),
            'approver': User.queryName(rsv.approver),
            'exam-rst': rsv.examRst
        }
        return rsvDict


# post-binding methods for Reservation
def _getIntervalStr(self: Reservation):
    """
    self中至少有Reservation中的如下属性：
        * method
        * st
        * ed
    return: 可读的时间段信息
    """
    if self.method == LongTimeRsv.methodValue:
        hour = timestamp.getHour(self.st)
        if hour == LongTimeRsv.morningStartHour:
            return f'{timestamp.getDate(self.st)()} {LongTimeRsv.morningCode}'
        elif hour == LongTimeRsv.afternoonStartHour:
            return f'{timestamp.getDate(self.st)()} {LongTimeRsv.afternoonCode}'
        elif hour == LongTimeRsv.nightStartHour:
            return f'{timestamp.getDate(self.st)()} {LongTimeRsv.nightCode}'
        else:
            return f'{timestamp.getDate(self.st)()} {LongTimeRsv.weekendCode}'

    elif self.method == FlexTimeRsv.methodValue:
        return f'{timestamp.getDate(self.st)} {timestamp.clock(self.st)}-{timestamp.clock(self.ed)}'
Reservation.getIntervalStr = _getIntervalStr

# TODO: 换个更恰当的名字
def mergeAndBeautify(qryRst: list):
    """
    qryRst中的rsv对象至少包含如下属性：
        * id
        * method
        * st
        * ed
        * chore
    """
    groups = {}
    rsvArr = []
    for e in qryRst:
        e: Reservation
        e.interval = None

        if e.method == FlexTimeRsv.methodValue:
            e.interval = _getIntervalStr(e)
            rsvArr.append(e)
        
        elif e.method == LongTimeRsv.methodValue:
            relation: dict = Json.loads(e.chore)['group-rsv']
            if 'sub-rsvs' in relation:
                e.interval = []
                e.interval.append(_getIntervalStr(e))

                for subRsvIds in relation['sub-rsvs']:
                    if subRsvIds in groups:
                        e.interval.append(_getIntervalStr(groups[subRsvIds]))
                
                groups[e.id] = e
                rsvArr.append(e)
            else:
                if relation['fth-rsv'] in groups:
                    groups[relation['fth-rsv']].interval.append(_getIntervalStr(e))
                else:
                    groups[e.id] = e
    return rsvArr