from flask import Blueprint, request, session, current_app
import requests as R
import requests.exceptions as RE
import json as Json
import functools
import time as Time
from copy import copy

from config import WX_APP_ID, WX_APP_SECRET, MACHINE_ID, skipLoginAndBind, skipAdmin
from . import db
from . import rsvIdPool, itemIdPool
from . import comerrs as ErrCode
from . import timetools as timestamp
from . import rsvstate as RsvState
from . import snowflake as Snowflake
from . import checkargs as CheckArgs
from . import models as Models
from .models import Admin, User, Item, Reservation
from .models import LongTimeRsv as LongTimeRsv
from .models import FlexTimeRsv as FlexTimeRsv

from . import ColorConsole as C
from pprint import pprint

router = Blueprint('router', __name__)

# -----------------   鉴权    ----------------------

@router.route('/login/', methods=['POST'])
def login():
    CODE_LOGIN_NOT_200 = {'code': 201, 'errmsg': 'not 200 response'}
    CODE_LOGIN_INCOMPLETE_WX_RES = {'code': 202, 'errmsg': 'incomplete wx responce'}
    CODE_LOGIN_WEIXIN_REJECT = {'code': 203, 'errmsg': 'wx reject svr' } # , 'wx-code': resJson['errcode'], 'wx-errmsg': resJson.get('errmsg', '')}
    CODE_LOGIN_TIMEOUT = {'code': 102, 'errmsg': 'svr request timeout'}
    CODE_LOGIN_CNT_ERROR = {'code': 103, 'errmsg': 'svr cnt err'}
    CODE_LOGIN_UNKOWN = {'code': 200, 'errmsg': 'unknown error, foolish gjm didn\'t cosider this case..'}

    data: dict = request.get_json()
    if not data or not data.get('code', None):
        return ErrCode.CODE_ARG_MISSING

    try:
        res = R.get(f'https://api.weixin.qq.com/sns/jscode2session?'  \
            + f'appid={WX_APP_ID}&secret={WX_APP_SECRET}&'      \
            + f"js_code={data['code']}&grant_type=authorization_code", timeout=5)
    
        if res.status_code != 200:
            return CODE_LOGIN_NOT_200

        resJson: dict = Json.loads(res.text)
        if  'openid' not in resJson \
            or not resJson['openid'] \
            or 'session_key' not in resJson \
            or not resJson['session_key']:

            # print(C.Red('incomplete wx res'), end='')
            # pprint(resJson)
            return CODE_LOGIN_INCOMPLETE_WX_RES

        if 'errcode' in resJson and resJson['errcode'] != 0:
            rtn = {}
            rtn.update(CODE_LOGIN_WEIXIN_REJECT)
            rtn.update({
                 'wx-code': resJson['errcode'], 
                 'wx-errmsg': resJson.get('errmsg', '')
            })
            return rtn

        openid = str(resJson['openid'])
        session['wx-skey'] = str(resJson["session_key"])
        session['openid'] = openid
    except RE.Timeout:
        return CODE_LOGIN_TIMEOUT
    except RE.ConnectionError as e:
        return CODE_LOGIN_CNT_ERROR
    except Exception as e:
        # print(C.Red(str(e)))
        # pprint(resJson)
        return CODE_LOGIN_UNKOWN

    user = db.session \
        .query(User.openid, User.schoolId) \
        .filter(User.openid==openid) \
        .limit(1)\
        .one_or_none()

    if user == None:
        db.session.add(User(openid))
        db.session.commit()
        user = (None, None)
    
    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['bound'] = user[1] != None
    return rtn

def requireLogin(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if skipLoginAndBind and not session.get('openid', None):
            session['openid'] = 'openid for debug'
            session['wx-skey'] = 'secret key for debug'
            return handler(*args, **kwargs)
        if not session.get('openid', None):
            return ErrCode.CODE_NOT_LOGGED_IN
        else:
            return handler(*args, **kwargs)
    return inner

def requireBinding(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if skipLoginAndBind:
            return handler(*args, **kwargs)

        openid = session['openid']
        schoolId = db.session.query(User.schoolId).filter(User.openid == openid).one_or_none()[0] # 这里可以安全的直接使用[0]，因为这个函数总在 requireLogin 后调用

        if schoolId == None:
            return ErrCode.CODE_UNBOUND
        else:
            return handler(*args, **kwargs)
    return inner

def requireAdmin(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if skipAdmin:
            return handler(*args, **kwargs)
        
        openid = session['openid']
        exist = db.session.query(Admin.openid).filter(Admin.openid == openid).one_or_none()
        if exist:
            return handler(*args, **kwargs)
        else:
            return ErrCode.CODE_NOT_ADMIN
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
        return ErrCode.CODE_ARG_MISSING

    try:
        schoolId = str(reqJson['id'])
        name = str(reqJson['name'])
        clazz = str(reqJson['clazz'])
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    if not CheckArgs.isSchoolId(schoolId) or not CheckArgs.isClazz(clazz):
        return ErrCode.CODE_ARG_INVALID

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

@router.route('/profile/')
@requireLogin
def getProfile():
    rtn = db.session.query(User).filter(User.openid == session['openid']).one().toDict()
    rtn.update(ErrCode.CODE_SUCCESS)
    return rtn


# ---------------- /item/ 系列 ----------------------

@router.route('/item/', methods=['GET'])
def itemlist():
    page = request.args.get('p', '1')
    try:
        page = int(page)
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    page -= 1
    if page >= (1<<65)-1 or page < 0:
        return ErrCode.CODE_ARG_INVALID
    
    itemCount = db.session.query(Item.id).filter(Item.delete == 0).count()
    items = Item.query.filter(Item.delete == 0).limit(20).offset(20*page).all()
    items = [e.toDict() for e in items]

    # pprint(items)

    rst = ErrCode.CODE_SUCCESS.copy()
    rst.update({
        'item-count': itemCount,
        'page': page+1,
        'items': items
    })

    return rst

# TODO: 在testItemAPI.py中添加测试代码
@router.route('/item/<int:itemId>', methods=['GET'])
def itemInfo(itemId):

    if not CheckArgs.isUint64(itemId):
        return ErrCode.CODE_ARG_INVALID
    
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none()
    if not item:
        return ErrCode.Item.CODE_ITEM_NOT_FOUND
    else:
        rst = {}
        rst.update(ErrCode.CODE_SUCCESS)
        rst['item'] = item.toDict()
        return rst

@router.route('/item/', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def addItem():
    reqJson = request.json

    if not reqJson.get('name') \
        or not reqJson.get('brief-intro') \
        or not reqJson.get('md-intro') \
        or not reqJson.get('thumbnail') \
        or reqJson.get('rsv-method') == None:

        # pprint(reqJson)
        return ErrCode.CODE_ARG_MISSING

    if not CheckArgs.areStr(reqJson, ['name', 'brief-intro', 'md-intro', 'thumbnail']) \
        or not CheckArgs.areInt(reqJson, ['rsv-method']):
        # pprint(reqJson)
        return ErrCode.CODE_ARG_TYPE_ERR

    try:
        item            = Item()
        item.id         = itemIdPool.next()
        item.name       = reqJson['name']
        item.available  = True
        item.delete     = False
        item.rsvMethod  = int(reqJson['rsv-method'])
        item.briefIntro = reqJson['brief-intro']

        if not CheckArgs.isUrl(reqJson['thumbnail']): # TODO: 这里可以进一步限制
            return ErrCode.CODE_ARG_FORMAT_ERR
        item.thumbnail  = reqJson['thumbnail']
        item.mdIntro    = reqJson['md-intro']
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    try:
        db.session.add(item)
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['item-id'] = item.id
    return rtn


@router.route('/item/<int:itemId>', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def modifyItem(itemId):
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none()
    if not item: return ErrCode.Item.CODE_ITEM_NOT_FOUND

    itemJson = request.json

    try:
        if 'name' in itemJson: item.name              = str(itemJson['name'])
        if 'available' in itemJson: item.available    = bool(itemJson['available'])
        if 'rsv-method' in itemJson: item.rsvMethod   = int(itemJson['rsv-method'])
        if 'brief-intro' in itemJson: item.briefIntro = itemJson['brief-intro']
        if 'thumbnail' in itemJson: item.thumbnail    = itemJson['thumbnail']
        if 'md-intro' in itemJson: item.mdIntro       = itemJson['md-intro']
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR

    return ErrCode.CODE_SUCCESS


@router.route('/item/<int:itemId>', methods=['DELETE'])
@requireLogin
@requireBinding
@requireAdmin
def delItem(itemId):
    if not CheckArgs.isUint64(itemId): return ErrCode.CODE_ARG_INVALID
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none() 
    if not item: return ErrCode.Item.CODE_ITEM_NOT_FOUND

    try:
        item.delete = True
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    
    return ErrCode.CODE_SUCCESS



# -------------------- /reservation/ --------------------

@router.route('/item/<int:itemId>/reservation')
def itemRsvInfo(itemId):
    qryRst = \
        db.session.query(
            Reservation.id,     # 0
            Reservation.method, 
            Reservation.state,
            Reservation.st,     # 3
            Reservation.ed,
            Reservation.chore   # 6, 记得最后返回时删除这个属性
        ) \
        .filter(Reservation.itemId == itemId) \
        .filter(Reservation.st >= timestamp.today()) \
        .filter(Reservation.ed <= timestamp.aWeekAfter()) \
        .all()  

    rst = {}
    rst.update(ErrCode.CODE_SUCCESS)

    rsvArr = Models.mergeAndBeautify(qryRst)
    def _process(e): # TODO: 想个好名字吧。。。
        e = dict(e)
        del e['chore']
        del e['st']
        del e['ed']
        return e

    rst['rsvs'] = [_process(e) for e in rsvArr] # 因为字段名和协议中属性名相同，所以不用多处理
    return rst


@router.route('/reservation/<int:rsvId>', methods=['GET'])
def getRsvInfo(rsvId):
    CODE_RSV_NOT_FOUND = {'code': 101, 'errmsg': 'reservation not found.'}

    if rsvId < 0 or rsvId > (1<<65)-1:
        return ErrCode.CODE_ARG_INVALID

    rsv = Reservation.fromRsvId(rsvId)
    if not rsv:
        return CODE_RSV_NOT_FOUND
    
    if   rsv.method == LongTimeRsv.methodValue: rsvJson = LongTimeRsv.toDict(rsv)
    elif rsv.method == FlexTimeRsv.methodValue: rsvJson = FlexTimeRsv.toDict(rsv)
    else: return ErrCode.CODE_DATABASE_ERROR # 如果执行这个分支，说明存在外部添加 Rsv 的行为，或代码出Bug

    rtn = {'rsv': rsvJson}
    rtn.update(ErrCode.CODE_SUCCESS)
    return rtn

@router.route('/reservation/', methods=['POST'])
@requireLogin
@requireBinding
def reserve():
    CODE_TIME_CONFLICT = {'code': 101, 'errmsg': 'time conflict'}
    CODE_TIME_OUT_OF_RANGE = {'code': 102, 'errmsg': 'reservation time out of range'}

    reqJson:dict = request.get_json()
    if not reqJson or \
        not CheckArgs.hasAttrs(reqJson, ['item-id', 'rsv-req', 'reason']):

        return ErrCode.CODE_ARG_MISSING

    if not CheckArgs.areStr(reqJson, ['reason']) \
        or not CheckArgs.areInt(reqJson, ['item-id', 'method']):

        return ErrCode.CODE_ARG_TYPE_ERR

    itemId = reqJson['item-id']
    reason = reqJson['reason']
    method = reqJson['method']

    r = Reservation()
    # r.id = rsvIdPool.next() 下面单独生成
    r.itemId = itemId
    r.guest = session['openid']
    r.reason = reason
    r.method = method
    r.state = RsvState.STATE_WAITING
    r.chore = ''

    if method == LongTimeRsv.methodValue:
        if not isinstance(reqJson['inteval'], list):
            return ErrCode.CODE_ARG_TYPE_ERR
        if len(reqJson['inteval']) == 0:
            return ErrCode.CODE_ARG_MISSING
        
        interval: list = reqJson['interval']
        r.chore = {'group-rsv': {}} # remember to cast to str

        rsvGroup = []

        for itl in interval:
            st, ed = LongTimeRsv.parseInterval(itl)
            if ed == None: return ErrCode.CODE_ARG_FORMAT_ERR
            elif ed == -1: return ErrCode.CODE_ARG_INVALID

            if ed > timestamp.aWeekAfter() or st < timestamp.now():
                return CODE_TIME_OUT_OF_RANGE

            new = copy(r)
            new.id = rsvIdPool.next()
            new.st, new.ed = LongTimeRsv.parseInterval(itl)
            rsvGroup.append(new)
        
        rsvGroup[0].chore['group-rsv']['sub-rsvs'] = []
        for i in range(1, len(rsvGroup)):
            rsvGroup[0].chore['group-rsv']['sub-rsvs'].append(rsvGroup[i].id)
            rsvGroup[i].chore['group-rsv']['fth-rsv'] = rsvGroup[0].id
        
        for e in rsvGroup:
            if e.hasTimeConflict():
                return CODE_TIME_CONFLICT

        for e in rsvGroup:
            e.chore = Json.dumps(e.chore)
            db.session.add(e)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error: ' + str(e))
            return ErrCode.CODE_DATABASE_ERROR

        rtn = {}
        rtn.update(ErrCode.CODE_SUCCESS)
        rtn['rsv-id'] = rsvGroup[0].id
        return rtn

    elif method == FlexTimeRsv.methodValue:
        if not isinstance(reqJson['interval'], str):
            return ErrCode.CODE_ARG_TYPE_ERR

        interval = reqJson['interval']

        st, ed = FlexTimeRsv.parseInterval(interval)
        if ed == None:
            return ErrCode.CODE_ARG_FORMAT_ERR
        elif ed == -1:
            return ErrCode.CODE_ARG_INVALID
        
        if ed > timestamp.aWeekAfter() or st < timestamp.now():
                return CODE_TIME_OUT_OF_RANGE

        r.id = rsvIdPool.next()
        r.st, r.ed = st, ed

        if r.hasTimeConflict():
            return CODE_TIME_CONFLICT

        db.session.add(r)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error: ' + str(e))
            return ErrCode.CODE_DATABASE_ERROR

        rtn = {}
        rtn.update(ErrCode.CODE_SUCCESS)
        rtn['rsv-id'] = r.id
        return rtn
        
    else:
        return ErrCode.CODE_ARG_INVALID


@router.route('/reservation/me')
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

    st = request.args.get('st', None)
    if st and CheckArgs.isDate(st):
        try:
            stId = makeSnowId(st, 0)
            sql = sql.filter(Reservation.id >= stId)
        except:
            return ErrCode.CODE_ARG_INVALID
    
    ed = request.args.get('ed', None)
    if ed and CheckArgs.isDate(ed):
        try:
            edId = makeSnowId(ed, 0)
            sql = sql.filter(Reservation.ed <= edId)
        except:
            return ErrCode.CODE_ARG_INVALID
    
    rsvJsonArr = Models.mergeAndBeautify(sql.all())
    adminNames = {} # openid --> name
    qryRst = db.session\
        .query(Admin.openid, User.name)\
        .join(User, User.openid == Admin.openid) \
        .all()
    for row in qryRst:
        adminNames[row.openid] = row.name

    def _pcs(e):
        nonlocal adminNames
        e = dict(e)
        del e['st']
        del e['ed']
        del e['chore']
        e['exam-rst'] = e.pop('examRst')
        e['item-id'] = e.pop('itemId')
        e['approver'] = adminNames[e['approver']]
        return e

    rst = {}
    rst.update(ErrCode.CODE_SUCCESS)
    rst['my-rsv'] = [_pcs(e) for e in rsvJsonArr]
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
        return ErrCode.CODE_ARG_MISSING

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
