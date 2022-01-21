from app.models import db
from sqlalchemy import and_
from sqlalchemy import or_

from . import rsv_state as RsvState
from app import timetools as timestamp

import re as Regex
import json as Json

from app.auth.model import User, Admin
from app.item.model import Item

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

        timeCdn = {or_(
            and_(Reservation.st >= self.st, Reservation.st < self.ed),
            and_(Reservation.ed > self.st, Reservation.ed < self.ed),
            and_(Reservation.st <= self.st, Reservation.ed >= self.ed)
        )}

        stateCdn = {or_(
            Reservation.state.op('&')(RsvState.STATE_WAIT),
            Reservation.state.op('&')(RsvState.STATE_START)
        )}

        conflictRsv = db.session\
            .query(Reservation.st, Reservation.ed, Reservation.id) \
            .filter(*stateCdn)\
            .filter(Reservation.itemId == self.itemId)\
            .filter(*timeCdn) \
            .first()

        conflict = conflictRsv != None

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

    def getEndTime(self):
        return SubRsvDelegator.getDelegator(self).getEndTime(self)

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
        return an interval array containing itself and children.
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
        item: Item = Item.fromId(rsv.itemId)

        rsvDict = {
            'id': rsv.id,
            'item': item.name,
            'item-id': rsv.itemId,
            'thumbnail': item.thumbnail,
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
        """
        return True only if rsv is a LongTimeRsv and is sub rsv.
        raise no exception.
        """
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

    def getEndTime(rsv: Reservation):
        rsv = LongTimeRsv.getFatherRsv(rsv)
        ed = rsv.ed
        choreJson = Json.loads(rsv.chore)
        for rsvId in choreJson['group-rsv']['sub-rsvs']:
            subRsvEd = db.session.query(Reservation.ed).filter(Reservation.id == rsvId).one()[0]
            ed = max(ed, subRsvEd)
        return ed

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
        
        item: Item = Item.fromId(rsv.itemId)

        rsvDict = {
            'id': rsv.id,
            'item': item.name,
            'thumbnail': item.thumbnail,
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

    def getEndTime(rsv: Reservation):
        return rsv.ed

    def isBegan(rsv: Reservation, now):
        return (rsv.st <= now < rsv.ed)
