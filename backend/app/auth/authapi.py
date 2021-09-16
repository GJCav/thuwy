from flask import request, session
import requests as R
import requests.exceptions as RE
import json as Json
import time as Time
import functools
import os
import traceback

from . import authRouter
from config import WX_APP_ID, WX_APP_SECRET, MACHINE_ID
from config import config
from app import db
from app import adminReqIdPool
from app import comerrs as ErrCode
from app.models import Admin, AdminRequest, User, UserBinding
import app.checkargs as CheckArgs

@authRouter.route('/login/', methods=['POST'])
def login():
    data: dict = request.get_json()
    if not data or not data.get('code', None):
        return ErrCode.CODE_ARG_MISSING

    try:
        res = R.get(f'https://api.weixin.qq.com/sns/jscode2session?'  \
            + f'appid={WX_APP_ID}&secret={WX_APP_SECRET}&'      \
            + f"js_code={data['code']}&grant_type=authorization_code", timeout=5)
    
        if res.status_code != 200:
            return ErrCode.Auth.CODE_LOGIN_NOT_200

        resJson: dict = Json.loads(res.text)
        if  'openid' not in resJson \
            or not resJson['openid'] \
            or 'session_key' not in resJson \
            or not resJson['session_key']:

            # print(C.Red('incomplete wx res'), end='')
            # pprint(resJson)
            return ErrCode.Auth.CODE_LOGIN_INCOMPLETE_WX_RES

        if 'errcode' in resJson and resJson['errcode'] != 0:
            rtn = {}
            rtn.update(ErrCode.Auth.CODE_LOGIN_WEIXIN_REJECT)
            rtn.update({
                 'wx-code': resJson['errcode'], 
                 'wx-errmsg': resJson.get('errmsg', '')
            })
            return rtn

        openid = str(resJson['openid'])
        session['wx-skey'] = str(resJson["session_key"])
        session['openid'] = openid
        session.permanent = True
    except RE.Timeout:
        return ErrCode.Auth.CODE_LOGIN_TIMEOUT
    except RE.ConnectionError as e:
        return ErrCode.Auth.CODE_LOGIN_CNT_ERROR
    except Exception as e:
        # print(C.Red(str(e)))
        # pprint(resJson)
        return ErrCode.Auth.CODE_LOGIN_UNKOWN

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
        # if skipLoginAndBind and not session.get('openid', None):
        #     session['openid'] = 'openid for debug'
        #     session['wx-skey'] = 'secret key for debug'
        #     return handler(*args, **kwargs)
        if not session.get('openid'):
            return ErrCode.CODE_NOT_LOGGED_IN
        elif not User.fromOpenid(session.get('openid')):
            # return ErrCode.CODE_NOT_LOGGED_IN # 这里意味着用户登录过，但数据库中没有记录，多半是管理员删库了
            return ErrCode.CODE_DATABASE_ERROR
        else:
            return handler(*args, **kwargs)
    return inner

def didilogin():
    if skipLoginAndBind and not session.get('openid'):
        return 'skipped'
    if not session.get('openid'):
        return 'no'
    elif not User.fromOpenid(session.get('openid')):
        return 'yes but database lost your record.'
    else:
        return 'yes'

def requireBinding(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        openid = session['openid']
        schoolId = db.session.query(User.schoolId).filter(User.openid == openid).one_or_none()[0] # 这里可以安全的直接使用[0]，因为这个函数总在 requireLogin 后调用

        if schoolId == None:
            return ErrCode.CODE_UNBOUND
        else:
            return handler(*args, **kwargs)
    return inner

def didibind():
    if didilogin() == 'skipped':
        return 'skipped'
    if 'no' in didilogin():
        return 'no and check your login state'
    openid = session['openid']
    schoolId = db.session.query(User.schoolId).filter(User.openid == openid).one_or_none()
    if not schoolId:
        return 'no and database lost your record'
    if not schoolId[0]:
        return 'no'
    else:
        return 'yes'

def requireAdmin(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        # if skipAdmin:
        #     return handler(*args, **kwargs)
        
        openid = session['openid']
        exist = db.session.query(Admin.openid).filter(Admin.openid == openid).one_or_none()
        if exist:
            return handler(*args, **kwargs)
        else:
            return ErrCode.CODE_NOT_ADMIN
    return inner

def amiadmin():
    if didilogin() != 'yes': return 'no and you did not login'
    if didibind() != 'yes': return 'no and you did not bind'
    openid = session['openid']
    exist = db.session.query(Admin.openid).filter(Admin.openid == openid).one_or_none()
    if exist: return 'yes'
    else: return 'no'

@authRouter.route('/bind/', methods=['POST'])
@requireLogin
def bind():

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

    openid = session['openid']
    user = User.fromOpenid(openid)
    
    if user.schoolId != None:
        return ErrCode.Auth.CODE_ALREADY_BOUND

    bdnInfo = UserBinding.check(schoolId, name, clazz)
    if bdnInfo == None:
        return ErrCode.Auth.CODE_INVALID_BIND
    if bdnInfo.openid != None:
        return ErrCode.Auth.CODE_TARGET_BOUND

    try:
        user.name = name
        user.schoolId = schoolId
        user.clazz = clazz
        bdnInfo.openid = openid

        db.session.commit()
    except:
        traceback.print_exc()
        return ErrCode.CODE_DATABASE_ERROR

    return ErrCode.CODE_SUCCESS

@authRouter.route('/profile/')
@requireLogin
def getMyProfile():
    rtn = User.queryProfile(session['openid'])
    if rtn == None: return ErrCode.CODE_ARG_INVALID
    rtn.update(ErrCode.CODE_SUCCESS)
    return rtn

@authRouter.route('/profile/<openId>/', methods=['GET'])
@requireLogin
@requireBinding
@requireAdmin
def getProfile(openId):
    openId = str(openId)
    profile = User.queryProfile(openId)
    if profile == None: return ErrCode.CODE_ARG_INVALID
    profile.update(ErrCode.CODE_SUCCESS)
    return profile


@authRouter.route('/admin/request/', methods=['POST'])
@requireLogin
@requireBinding
def requestAdmin():
    
    exist = Admin.fromId(session['openid'])
    if exist: return ErrCode.Auth.CODE_ALREADY_ADMIN

    exist = db.session\
        .query(AdminRequest)\
        .filter(AdminRequest.requestor == session['openid']) \
        .filter(AdminRequest.state == 0)\
        .first()
    if exist: return ErrCode.Auth.CODE_ALREADY_REQUESTED

    try:
        req = AdminRequest()
        req.id = adminReqIdPool.next()
        req.requestor = session['openid']
        req.state = 0
        db.session.add(req)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    
    rtn = {'id': req.id}
    rtn.update(ErrCode.CODE_SUCCESS)
    return rtn


@authRouter.route('/admin/request/', methods=['GET'])
@requireLogin
@requireBinding
@requireAdmin
def adminReqList():
    qryRst = db.session\
        .query(AdminRequest)\
        .filter(AdminRequest.state == 0)\
        .all()
    
    arr = []
    for r in qryRst:
        arr.append(r.toDict())
    
    rtn = {'list': arr}
    rtn.update(ErrCode.CODE_SUCCESS)
    return rtn


@authRouter.route('/admin/request/<int:reqId>/', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def examAdminReq(reqId):
    adminReq = AdminRequest.fromId(reqId)
    if not adminReq: return ErrCode.CODE_ARG_INVALID
    if adminReq.state != 0: return ErrCode.CODE_ARG_INVALID
    # TODO: 细分ErrCode

    json = request.get_json()
    if not CheckArgs.hasAttrs(json, ['pass', 'reason']):
        return ErrCode.CODE_ARG_MISSING

    
    if json['pass'] == 1:
        adminReq.state = 1
        admin = Admin()
        admin.openid = adminReq.requestor
        db.session.add(admin)
    elif json['pass'] == 0:
        adminReq.state = 2
    else:
        return ErrCode.CODE_ARG_INVALID
        
    adminReq.reason = json['reason']
    adminReq.approver = session['openid']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    
    return ErrCode.CODE_SUCCESS


@authRouter.route('/admin/<openid>/', methods=['DELETE'])
@requireLogin
@requireBinding
@requireAdmin
def delAdmin(openid):
    openid = str(openid)
    admin = Admin.fromId(openid)
    if not admin:
        return ErrCode.CODE_ARG_INVALID
    
    db.session.delete(admin)
    return ErrCode.CODE_SUCCESS

if getattr(config, 'ENABLE_TEST_ACCOUNT', False):
    print('!!Warning!! Running with testing mode, enable testing account auto-creation.')

    @authRouter.route('/test/login/')
    def loginTestAccount():
        rint = 0
        for b in os.urandom(64):
            rint += b
        rint %= 10000000000
        fakeOpenId = f'test-account-{rint}'
        
        existAccount = User.fromOpenid(fakeOpenId)
        if existAccount:
            existAdmin = Admin.fromId(fakeOpenId)
            if existAdmin:
                db.session.delete(existAdmin)
            db.session.delete(existAccount)
            db.session.commit()

        newAccount = User(fakeOpenId)
        mode = request.args.get('mode', 'user')
        if mode == 'admin':
            newAccount.name = f'TAdmin {rint}'
            admin = Admin()
            admin.openid = fakeOpenId
            db.session.add(admin)
        else:
            newAccount.name = f'TUser {rint}'

        newAccount.schoolId = f'{rint}'
        newAccount.clazz = f'未央-测试'
        db.session.add(newAccount)

        try:
            db.session.commit()
        except:
            return ErrCode.CODE_DATABASE_ERROR
        
        session['openid'] = fakeOpenId
        session.permanent = True

        return ErrCode.CODE_SUCCESS

@authRouter.route('/admin/')
@requireLogin
@requireBinding
@requireAdmin
def getAdminList():

    profileArr = []

    qryRst = db.session.query(Admin).all()
    for admin in qryRst:
        profileArr.append(User.fromOpenid(admin.openid).toDict())
    
    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['profiles'] = profileArr
    return rtn

@authRouter.route('/user/')
@requireLogin
@requireBinding
@requireAdmin
def getUserList():
    PageLimit = 30

    clazz = request.args.get('clazz', None)
    page = request.args.get('p', 1, int)

    qry = db.session.query(User)
    if clazz:
        qry = qry.filter(User.clazz == clazz)
    
    qry = qry.limit(PageLimit).offset((page-1)*PageLimit)

    qryRst = qry.all()
    proArr = [e.toDict() for e in qryRst]
    
    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['profiles'] = proArr
    return rtn

@authRouter.route('/user/<openid>/', methods=['DELETE'])
def unbindUser(openid):
    if not openid:
        return ErrCode.CODE_ARG_INVALID
    
    user = User.fromOpenid(openid)

    if not user:
        return ErrCode.Auth.CODE_USER_NOT_FOUND
    
    user.schoolId = None
    user.name == None
    user.clazz = None

    try:
        db.session.commit()
    except:
        traceback.print_exc()
        return ErrCode.CODE_DATABASE_ERROR
    
    return ErrCode.CODE_SUCCESS
