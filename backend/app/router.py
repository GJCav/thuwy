from flask import Blueprint, request, session
import requests as R
import requests.exceptions as RE
import json as Json
import functools
from re import escape, match as reMatch
import time as Time

from .models import *
from config import WX_APP_ID, WX_APP_SECRET, MACHINE_ID
from . import rsvIdPool
from . import comerrs as ErrCode
from . import timetools as timestamp
from .models import RsvMethodLongTimeRsv as LongTimeRsv
from .models import RsvMethodFlexibleTimeRsv as FlexTimeRsv
from . import rsvstate as RsvState
from . import snowflake as Snowflake

router = Blueprint('router', __name__)

@router.route('/login/', methods=['POST'])
def login():
    data: dict = request.get_json()
    if not data or not data.get('code', None):
        return ErrCode.CODE_ARG_MESSING

    try:
        res = R.get(f'https://api.weixin.qq.com/sns/jscode2session?'  \
            + f'appid={WX_APP_ID}&secret={WX_APP_SECRET}&'      \
            + f"js_code={data['code']}&grant_type=authorization_code", timeout=5)
    
        if res.status_code != 200:
            return {'code': 201, 'errmsg': 'not 200 response'}

        resJson: dict = Json.loads(res.text)
        if 'errcode' not in resJson \
            or 'openid' not in resJson \
            or not resJson['openid'] \
            or 'session_key' not in resJson \
            or not resJson['session_key']:

            return {'code': 202, 'errmsg': 'incomplete wx responce'}

        if resJson['errcode'] != 0:
            return {'code': 203, 'errmsg': 'wx reject svr', 'wx-code': resJson['errcode'], 'wx-errmsg': resJson.get('errmsg', '')}

        openid = str(resJson['openid'])
        session['wx-skey'] = str(resJson["session_key"])
        session['openid'] = openid
    except RE.Timeout:
        return {'code': 102, 'errmsg': 'svr request timeout'}
    except RE.ConnectionError as e:
        return {'code': 103, 'errmsg': 'svr cnt err'}
    except:
        return {'code': 200, 'errmsg': 'unknown error'}

    exist = db.session \
        .query(User.openid) \
        .filter(User.openid==openid) \
        .limit(1) \
        .count()

    
    if exist == 0:
        db.session.add(User(openid))
        db.session.commit()

    return {"code": 0, 'errmsg': 'success'}


def requireLogin(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if not session.get('openid', None):
            return ErrCode.CODE_NOT_LOGGED_IN
        else:
            return handler(*args, **kwargs)
    return inner


def requireBinding(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        openid = session['openid']
        schoolId = db.session.query(User.schoolId).filter(User.openid == openid).one_or_none()
        if schoolId == None:
            return ErrCode.CODE_UNBOUND
        else:
            return handler(*args, **kwargs)
    return inner


@router.route('/bind/', methods=['POST'])
@requireLogin
def bind():
    CODE_BIND_SCHOOLID_EXISTED = {
        'code': 101,
        'errmsg': 'school id existed'
    }

    reqJson: dict = request.get_json()
    if not reqJson \
        or 'id' not in reqJson \
        or not reqJson['id'] \
        or 'name' not in reqJson \
        or not reqJson['name'] \
        or 'clazz' not in reqJson \
        or not reqJson['clazz']:
        return ErrCode.CODE_ARG_MESSING

    try:
        schoolId = str(reqJson['id'])
        name = str(reqJson['name'])
        clazz = str(reqJson['clazz'])
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    def match(pat, val):
        if not reMatch(pat, val):
            return ErrCode.CODE_ARG_FORMAT_ERR
    
    match(r'^\d{10}$', schoolId)
    match('^\d+$', name)
    match('^未央-.+\d\d$', clazz)
    openid = session['openid']

    exist = db.session.query(User.schoolId) \
        .filter(User.schoolId==schoolId) \
        .count() >= 1

    if exist:
        return CODE_BIND_SCHOOLID_EXISTED
    
    User.query \
        .filter(User.openid == openid) \
        .update({
            'schoolId': schoolId,
            'name': name,
            'clazz': clazz
        })
    db.session.commit()

    return ErrCode.CODE_SUCCESS


@router.route('/itemlist/')
def itemlist():
    page = request.args.get('p', '1')
    try:
        page = int(page)
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    page -= 1
    
    itemCount = db.session.query(Item.id).count()
    items = Item.query.limit(20).offset(20*page).all()
    items = [e.toDict() for e in items]

    rst = ErrCode.CODE_SUCCESS.copy()
    rst.update({
        'item-count': itemCount,
        'page': page+1,
        'items': items
    })


def _makeRsvInfoArr(qryRst, _makeRsvJson):
    """
    dealwith query result like this
    db.session.query(
        Reservation.id,     # 0
        Reservation.method, 
        Reservation.state,
        Reservation.st,     # 3
        Reservation.ed,
        Reservation.chore   # 6
    )
    """

    def _singleInterval(row):
        if row[1] == LongTimeRsv.methodValue:
            hour = timestamp.getHour(row[3])
            if hour == LongTimeRsv.morningStartHour:
                return f'{timestamp.date(row[3])()} {LongTimeRsv.morningCode}'
            elif hour == LongTimeRsv.afternoonStartHour:
                return f'{timestamp.date(row[3])()} {LongTimeRsv.afternoonCode}'
            elif hour == LongTimeRsv.nightStartHour:
                return f'{timestamp.date(row[3])()} {LongTimeRsv.nightCode}'
            else:
                return f'{timestamp.date(row[3])()} {LongTimeRsv.weekendCode}'

        elif row[1] == FlexTimeRsv.methodValue:
            return f'{timestamp.date(row[3])} {timestamp.clock(row[3])}-{timestamp.clock(row[4])}'

        groups = {}
        rsvArr = []
        for row in qryRst:
            rsv = _makeRsvJson(row)
            if rsv['method'] == FlexTimeRsv.methodValue:
                rsv['interval'] = _singleInterval(row)
                rsvArr.append(rsv)
            elif rsv['method'] == LongTimeRsv.methodValue:
                relation: dict = Json.loads(row[6])['group-rsv']
                if 'sub-rsvs' in relation:
                    rsv['interval'] = []
                    rsv['interval'].append(_singleInterval(row))
                    groups[rsv['id']] = rsv
                    rsvArr.append(rsv)
                else:
                    groups[relation['fth-rsv']]['interval'].append(_singleInterval(row))
        return rsvArr

@router.route('/itemrsvinfo/')
def itemrsvinfo():
    reqJson: dict = request.get_json()
    if not reqJson \
        or not reqJson.get('item-id', None):
        return ErrCode.CODE_ARG_MESSING
    
    try:
        itemId = int(reqJson['item-id'])
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    qryRst = \
        db.session.query(
            Reservation.id,     # 0
            Reservation.method, 
            Reservation.state,
            Reservation.st,     # 3
            Reservation.ed,
            Reservation.chore   # 6
        ) \
        .filter(Reservation.itemId == itemId) \
        .filter(Reservation.st >= timestamp.today()) \
        .filter(Reservation.ed <= timestamp.aWeekAfter()) \
        .all()

    def _makeRsvJson(row):
        rsvJson = {
            'id': row[0],
            'method': row[1],
            'state': row[2],
            'interval': None
        }
        return rsvJson

    rst = {}
    rst.update(ErrCode.CODE_SUCCESS)
    rst['rsvs'] = _makeRsvInfoArr(qryRst, _makeRsvJson)
    return rst

# TODO: 增加检查目标预约时间是否已经被预约了
@router.route('/reserve/', methods=['POST'])
@requireLogin
@requireBinding
def reserve():
    reqJson:dict = request.get_json()
    if not reqJson \
        or not reqJson.get('item-id', None) \
        or not reqJson.get('rsv-req', None) \
        or not reqJson.get('reason', None):

        return ErrCode.CODE_ARG_MESSING
    
    try:
        itemId = str(reqJson['item-id'])
        reason = str(reqJson['reason'])
        reqRsv: dict = reqJson['rsv-req']

        if not isinstance(reqRsv, dict): return ErrCode.CODE_ARG_TYPE_ERR
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    if not reqRsv \
        or reqRsv.get('method', None) \
        or reqRsv.get('interval', None):
        return ErrCode.CODE_ARG_MESSING
    
    try:
        method = int(reqRsv['method'])
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    def makeLongTimeRsv(interval: str):
        dateStr, codeStr = interval.split(' ')
        r = Reservation()
        r.id = rsvIdPool.next()
        r.itemId = itemId
        r.guest = session['openid']
        r.reason = reason
        r.method = method
        r.state = RsvState.STATE_WAITING
        r.chore = {'group-rsv': {}} # remember to cast to str
        
        code = int(codeStr)
        if code == LongTimeRsv.morningCode:
            r.st = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.morningStartHour
            )
            r.ed = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.morningEndHour
            )
        elif code == LongTimeRsv.afternoonCode:
            r.st = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.afternoonStartHour
            )
            r.ed = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.afternoonEndHour
            )
        elif code == LongTimeRsv.nightCode:
            r.st = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.nightStartHour
            )
            r.ed = timestamp.hoursAfter(
                timestamp.dateToTimestamp(dateStr),
                LongTimeRsv.nightEndHour
            )
        elif code == LongTimeRsv.weekendCode:
            r.st = timestamp.dateToTimestamp(dateStr)
            if timestamp.getWDay(r.st) != 6:
                raise Exception()
            r.ed = timestamp.daysAfter(r.st, 2)
        else:
            raise Exception()
    
    def makeFlexTimeRsv():
        dateStr, durationStr = reqRsv['inteval'].split(' ')
        stStr, edStr = durationStr.split('-')
        datePart = timestamp.dateToTimestamp(dateStr)
        toArgs = lambda x: [int(e) for e in x.split(':')]

        r = Reservation()
        r.id = rsvIdPool.next()
        r.itemId = itemId
        r.guest = session['openid']
        r.method = method
        r.state = RsvState.STATE_WAITING
        r.chore = ''

        r.st = timestamp.clockAfter(datePart, *toArgs(stStr))
        r.ed = timestamp.clockAfter(datePart, *toArgs(edStr))

        return r

    if method == LongTimeRsv.methodValue:
        if not isinstance(reqRsv['inteval'], list):
            return ErrCode.CODE_ARG_TYPE_ERR
        if len(reqRsv['inteval']) == 0:
            return ErrCode.CODE_ARG_MESSING
        
        rsvGroup = []
        try:
            for itl in reqRsv['inteval']:
                rsvGroup.append(makeLongTimeRsv(itl))
        except:
            return ErrCode.CODE_ARG_INVALID
        
        rsvGroup[0].chore['group-rsv']['sub-rsvs'] = []
        for i in range(1, len(rsvGroup)):
            rsvGroup[0].chore['group-rsv']['sub-rsvs'].append(rsvGroup[i].id)
            rsvGroup[i].chore['group-rsv']['fth-rsv'] = rsvGroup[0].id
        
        for e in rsvGroup:
            e.chore = Json.dumps(e.chore)
            db.session.add(e)
        db.session.commit()

    elif method == FlexTimeRsv.methodValue:
        rsv = makeFlexTimeRsv()
        db.session.add(rsv)
        db.session.commit()

    else:
        return ErrCode.CODE_ARG_INVALID
    
    return ErrCode.CODE_SUCCESS

@router.route('/querymyrsv/')
@requireLogin
def querymyrsv():
    openid = session['openid']

    def makeSnowId(date, flow):
        sfTime = Snowflake.convertTimestamp(Time.mktime(Time.strptime(date, '%Y-%m-%d')))
        return Snowflake.makeId(sfTime, MACHINE_ID, flow)

    sql = db.session.query(
        Reservation.id,     # 0
        Reservation.method, 
        Reservation.state,
        Reservation.st,     # 3
        Reservation.ed,
        Reservation.chore,   # 6
        Reservation.itemId,
        Reservation.reason, # 8
        Reservation.approver,
        Reservation.examRst # 10
    ).filter(Reservation.guest == openid)

    try:
        stId = makeSnowId(request.args['st'], 0)
        sql = sql.filter(Reservation.id >= stId)
    except:
        pass
    try:
        stId = makeSnowId(request.args['ed'], 0)
        sql = sql.filter(Reservation.id < stId)
    except:
        pass

    def _makeRsvJson(row):
        return {
            'id': row[0],
            'method': row[1],
            'state': row[2],
            'interval': None,
            'item-id': row[7],
            'reason': row[8],
            'approver': row[9],
            'exam-rst': row[10]
        }
    
    rsvJsonArr = _makeRsvInfoArr(sql.all(), _makeRsvJson)
    adminNames = {}
    for admin in Admin.query.all():
        name = db.session.query(User.name).filter(User.openid == admin.openid).one()[0]
        adminNames[admin.openid] = name

    for rsv in rsvJsonArr:
        rsv['approver'] = adminNames[rsv['approver']]

    rst = {}
    rst.update(ErrCode.CODE_SUCCESS)
    rst['my-rsv'] = rsvJsonArr
    return rst

@router.route('/cancel/')
@requireLogin
@requireBinding
def cancel():
    CODE_RSV_NOT_EXIST = {'code': 101, 'errmsg': 'rsv not exist'}
    CODE_RSV_BEGAN     = {'code': 102, 'errmsg': 'rsv has began'}
    CODE_RSV_COMPLETED = {'code': 103, 'errmsg': 'rsv completed'}
    CODE_RSV_REJECTED  = {'code': 104, 'errmsg': 'rsv rejected'}
    

    reqJson: dict = request.get_json()

    if not reqJson \
        or not reqJson.get('rsv-id', None):
        return ErrCode.CODE_ARG_MESSING

    rsvId = reqJson['rsvId']
    
    rsv: Reservation = Reservation.query \
        .filter(Reservation.id == rsvId) \
        .one_or_none()
    
    if not rsv                           : return CODE_RSV_NOT_EXIST
    if RsvState.isExamRejected(rsv.state): return CODE_RSV_REJECTED
    if RsvState.isCompleted(rsv.state)   : return CODE_RSV_COMPLETED
    
    now = timestamp.now()
    isBegan = rsv.st <= now <= rsv.ed

    if not isBegan and rsv.method == LongTimeRsv.methodValue:
        choreJson: dict = Json.loads(rsv.chore)
        subRsvIdArr = choreJson['group-rsv'].get('sub-rsvs', [])
        for subRsvId in subRsvIdArr:
            st, ed = db.session.query(Reservation.st, Reservation.ed) \
                .filter(Reservation.id == subRsvId) \
                .one()
            if st <= now <= ed:
                isBegan = True
                break
    
    if isBegan: return CODE_RSV_BEGAN

    def toFthRsv(rsv: Reservation) -> Reservation:
        choreJson: dict = Json.loads(rsv.chore)
        if 'fth-rsv' not in choreJson['group-rsv']:
            return rsv
        else:
            fthId = choreJson['group-rsv']['fth-rsv']
            return Reservation.query.filter(Reservation.id == fthId).one()

    rsv = toFthRsv(rsv)
    rsv.state = RsvState.cancel(rsv.state)

    choreJson: dict = Json.loads(rsv.chore)
    subRsvIdArr = choreJson['group-rsv']['sub-rsvs']
    for subRsvId in subRsvIdArr:
        subRsv: Reservation = Reservation.query.filter(Reservation.id == subRsvId).one()
        subRsv.state = RsvState.cancel(subRsv.state)

    db.session.commit()
    return ErrCode.CODE_SUCCESS
