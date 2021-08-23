
from app import db
from sqlalchemy import or_, and_
from sqlalchemy.engine.row import Row
import json as Json
import re as Regex
import base64
import os

from . import timetools as timestamp
from app import snowflake as Snowflake
from config import userSysName

# db: SQLAlchemy
# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column('id', db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     city = db.Column(db.String(100))


class Admin(db.Model):
    __tablename__ = 'admin'
    openid        = db.Column(db.Text, primary_key = True)

    def fromId(id):
        return db.session.query(Admin).filter(Admin.openid == id).one_or_none()

class User(db.Model):
    __tablename__ = "user"
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

    def fromOpenid(openid):
        return db.session.query(User).filter(User.openid == openid).one_or_none()

    def queryProfile(openId):
        openId = str(openId)
        usr = db.session.query(User).filter(User.openid == openId).one_or_none()
        if usr == None:
            return None
        else:
            usr = usr.toDict()
            usr['admin'] = bool(Admin.fromId(openId))
            return usr

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
    __tablename__ = "item"
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

    def querySupportedMethod(id):
        """
        return none if item not found.
        """
        qry = db.session\
            .query(Item.rsvMethod)\
            .filter(Item.id == id)\
            .one_or_none()
        return qry[0] if qry else None

    def __repr__(self) -> str:
        return f'Item({self.name}, {self.briefIntro}, {self.id}, {self.mdIntro if len(self.mdIntro) < 30 else (self.mdIntro[:27]+"...")})'

class Reservation(db.Model):
    __tablename__ = 'reservation'
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

    __subrsvtypes__ = {}

    def hasTimeConflict(self):
        """
        self 不一定必须是 Reservation 类型，只要具有 st, ed, itemId 几个属性即可
        """
        # 不支持连续小于号
        # cdn = {or_(
        #     self.st <= Reservation.st < self.ed,
        #     self.st <= Reservation.ed < self.ed,
        #     Reservation.st <= self.st < Reservation.ed,
        # )}

        cdn = {or_(
            and_(Reservation.st >= self.st, Reservation.st < self.ed),
            and_(Reservation.ed > self.st, Reservation.ed < self.ed),
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
    
    # TODO: 考虑一下要不要修改 __getattr__ 把未知属性也代理下去
    def toDict(self):
        """
        根据 method 的值自动调用恰当的方法。
        """
        return SubRsvDelegator.getDelegator(self).toDict(self)

    def getInterval(self):
        """
        delegate to SubRsvDelegator
        """
        return SubRsvDelegator.getDelegator(self).getInterval(self)

    def changeState(self, newState):
        """
        不会检查这个状态转换是否合法。
        """
        if not isinstance(self, Reservation):
            raise ValueError('this is not an instance of Reservation.')
        return SubRsvDelegator.getDelegator(self).changeState(self, newState)

    def isBegan(self, now = None):
        if not now:
            now = timestamp.now()
        return SubRsvDelegator.getDelegator(self).isBegan(self, now)

class SubRsvDelegator:
    methodValue = 0

    def getDelegator(rsv):
        for cls in SubRsvDelegator.__subclasses__():
            if rsv.method == cls.methodValue:
                return cls
        raise TypeError(f'Unknown method: {rsv.method}')

class LongTimeRsv(SubRsvDelegator):
    methodValue = 1
    methodMask = 1
    
    morningStartHour   = 8
    morningEndHour     = 12
    morningCode        = 1

    afternoonStartHour = 13
    afternoonEndHour   = 17
    afternoonCode      = 2

    nightStartHour     = 18
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
        if not Regex.match(r'^\d{4}-\d{1,2}-\d{1,2} \d$', interval):
            return (None, None)
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
                ed = timestamp.daysAfter(2, st)
            else:
                st = None
                ed = -1
        except Exception as e:
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
        """
        rsv should be father reservation.
        """
        if LongTimeRsv.isChildRsv(rsv):
            raise ValueError('this is not a father rsv')
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

        rsv = LongTimeRsv.getFatherRsv(rsv)

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

    def isChildRsv(rsv: Reservation):
        if rsv.method != LongTimeRsv.methodValue: return False
        chore = Json.loads(rsv.chore)
        return 'fth-rsv' in chore['group-rsv']

    def isFatherRsv(rsv):
        if rsv.method != LongTimeRsv.methodValue: return False
        chore = Json.loads(rsv.chore)
        return 'sub-rsvs' in chore['group-rsv']

    def changeState(rsv: Reservation, newState):
        if LongTimeRsv.isChildRsv(rsv): rsv = LongTimeRsv.getFatherRsv(rsv)
        rsv.state = newState
        choreJson = Json.loads(rsv.chore)
        for rsvId in choreJson['group-rsv']['sub-rsvs']:
            subRsv = Reservation.fromRsvId(rsvId)
            subRsv.state = newState

    def isBegan(rsv: Reservation, now):
        began = (rsv.st <= now < rsv.ed)
        if not began:
            rsv = LongTimeRsv.getFatherRsv(rsv)
            choreJson = Json.loads(rsv.chore)
            for rsvId in choreJson['group-rsv']['sub-rsvs']:
                st, ed = db.session.query(Reservation.st, Reservation.ed) \
                    .filter(Reservation.id == rsvId) \
                    .one()
                if st <= now <= ed:
                    isBegan = True
                    break
        return began

class FlexTimeRsv(SubRsvDelegator):
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
        # return f'{dateStr} {H(st)}:{M(st)}-{H(ed)}:{M(ed)}'
        return '{} {:0>2}:{:0>2}-{:0>2}:{:0>2}'.format(dateStr, H(st), M(st), H(ed), M(ed))

    def getInterval(rsv: Reservation):
        return f'{timestamp.getDate(rsv.st)} {timestamp.clock(rsv.st)}-{timestamp.clock(rsv.ed)}'

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

    def changeState(rsv: Reservation, newState):
        rsv.state = newState

    def isBegan(rsv: Reservation, now):
        return (rsv.st <= now < rsv.ed)


class AdminRequest(db.Model):
    __tablename__ = 'admin_req'
    id            = db.Column(db.Integer, primary_key = True)
    requestor     = db.Column(db.Text)
    approver      = db.Column(db.Text)
    state         = db.Column(db.Integer) # 0: waiting, 1: accept, 2: reject
    reason        = db.Column(db.Text)

    def fromId(id):
        return db.session.query(AdminRequest).filter(AdminRequest.id == id).one_or_none()

    def toDict(self):
        return {
            'id': self.id,
            'requestor': User.fromOpenid(self.requestor).toDict(),
            'approver': User.queryName(self.approver),
            # 'state': self.state,
            'reason': self.reason
        }

class Advice(db.Model):
    STATE_WAIT = 1
    STATE_END = 2

    __tablename__ = 'advice'
    id            = db.Column(db.Integer, primary_key = True)
    proponent     = db.Column(db.Text)
    title        = db.Column(db.Text)
    content       = db.Column(db.Text)
    state         = db.Column(db.Integer)
    response      = db.Column(db.Text)

    def queryById(id):
        rst = db.session.query(Advice).filter(Advice.id == id).one_or_none()
        return rst

    def toDict(self, carryContent = False):
        rst = {
            'id': self.id,
            'proponent': User.queryName(self.proponent),
            'title': self.title,
            'state': self.state
        }
        if carryContent:
            rst['response'] = self.response
        return rst


def init_db():
    with db.app.app_context():
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
    pass

# 太TM神奇了，python的dict没有__dict__属性，不能动态添加属性，如：
#   a = {}
#   a.foo = 10 # 报错：AttributeError
# 此时setattr也没用，因为dict重写了__setattr__
# 但自己写的类默认是有__dict__的，也就是可以setattr
# 如果自己写的类有__slot__，那么也不能动态添加，sqlachemy.engine.row.Row 就这么干的

class _Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def __getattribute__(self, name: str):
        if name in self: return self[name]
        else: return super().__getattribute__(name)

    def __setattr__(self, name: str, value) -> None:
        self[name] = value

"""
即使是LongTimeRsv，也只返回单挑 interval 
"""
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
            return f'{timestamp.getDate(self.st)} {LongTimeRsv.morningCode}'
        elif hour == LongTimeRsv.afternoonStartHour:
            return f'{timestamp.getDate(self.st)} {LongTimeRsv.afternoonCode}'
        elif hour == LongTimeRsv.nightStartHour:
            return f'{timestamp.getDate(self.st)} {LongTimeRsv.nightCode}'
        else:
            return f'{timestamp.getDate(self.st)} {LongTimeRsv.weekendCode}'

    elif self.method == FlexTimeRsv.methodValue:
        return f'{timestamp.getDate(self.st)} {timestamp.clock(self.st)}-{timestamp.clock(self.ed)}'


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
        # e: Row,
        # setattr(e, 'interval', None), 因为 e 是Row类型，不能动态添加属性，所以hack一下
        e = _Dict(**dict(e))
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