from math import ceil
from typing import List
from flask import abort, request, send_file, session, g
import flask
import requests as R
import requests.exceptions as RE
import json as Json
import time as Time
import functools
import os
import traceback
import re as Regex
from flask_socketio import Namespace, emit
from app import socketio_app

from app.auth import util
import app.wxapi as wxapi

from . import authRouter
from config import WX_APP_ID, WX_APP_SECRET, config, DevelopmentConfig
from app.comerrs import *
from .errcode import *
import app.checkargs as CheckArgs
from app import timetools as timestamp
import app.models as Model

from .model import (
    Entity,
    EntityAssociation,
    EntityType,
    Permission,
    db,
    User,
    UserBinding,
    selectEntityAssociation,
    selectPermission
)
from .model import Scope


@authRouter.route("/login/", methods=["POST"])
def login():
    data: dict = request.get_json()
    if not data or not data.get("code", None):
        return CODE_ARG_MISSING

    try:
        res = R.get(
            f"https://api.weixin.qq.com/sns/jscode2session?"
            + f"appid={WX_APP_ID}&secret={WX_APP_SECRET}&"
            + f"js_code={data['code']}&grant_type=authorization_code",
            timeout=5,
        )

        if res.status_code != 200:
            return CODE_LOGIN_NOT_200

        resJson: dict = Json.loads(res.text)
        if (
            "openid" not in resJson
            or not resJson["openid"]
            or "session_key" not in resJson
            or not resJson["session_key"]
        ):

            # print(C.Red('incomplete wx res'), end='')
            # pprint(resJson)
            return CODE_LOGIN_INCOMPLETE_WX_RES

        if "errcode" in resJson and resJson["errcode"] != 0:
            rtn = {}
            rtn.update(CODE_LOGIN_WEIXIN_REJECT)
            rtn.update(
                {"wx-code": resJson["errcode"], "wx-errmsg": resJson.get("errmsg", "")}
            )
            return rtn

        openid = str(resJson["openid"])
        session["wx-skey"] = str(resJson["session_key"])
        session["openid"] = openid
        session.permanent = True
    except RE.Timeout:
        return CODE_LOGIN_TIMEOUT
    except RE.ConnectionError as e:
        return CODE_LOGIN_CNT_ERROR
    except Exception as e:
        # print(C.Red(str(e)))
        # pprint(resJson)
        return CODE_LOGIN_UNKOWN

    user = (
        db.session.query(User.openid, User.school_id)
        .filter(User.openid == openid)
        .limit(1)
        .one_or_none()
    )

    if user == None:
        db.session.add(User(openid=openid))
        db.session.commit()
        user = (None, None)

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["bound"] = user[1] != None
    return rtn


def challengeScope(requirerules: List[str]):
    openid = session.get("openid")
    if not openid:
        return False
    
    user = User.fromOpenid(openid)
    if not user:
        return False

    if not user.entity:
        return False

    privileges = user.entity.all_privileges
    for rule in requirerules:
        requireScopes = set(rule.split(" "))
        if not requireScopes.issubset(privileges):
            return False

    g.openid = openid
    return True


def requireScope(requirerules: List[str]):
    # validate scopes here
    from app import app
    with app.app_context():
        unknown_scopes = set()  
        for rule in requirerules:
            for scopeStr in rule.split(" "):
                if not Scope.fromName(scopeStr):
                    unknown_scopes.add(scopeStr)
        
        if unknown_scopes:
            raise ValueError(f"unknown scopes: {unknown_scopes}")

    def _checkScope(handler):
        @functools.wraps(handler)
        def inner(*args, **kwargs):
            canAccess = challengeScope(requirerules)
            if canAccess: return handler(*args, **kwargs)
            else: return CODE_ACCESS_DENIED
        return inner

    return _checkScope


@authRouter.route("/bind/", methods=["POST"])
def bind():
    if not session.get("openid"):
        return CODE_NOT_LOGGED_IN
    elif not User.fromOpenid(session.get("openid")):
        # return CODE_NOT_LOGGED_IN # 这里意味着用户登录过，但数据库中没有记录，多半是管理员删库了
        return CODE_DATABASE_ERROR

    reqJson: dict = request.get_json()
    if (
        not reqJson
        or "id" not in reqJson
        or not reqJson["id"]
        or "name" not in reqJson
        or not reqJson["name"]
        or "clazz" not in reqJson
        or not reqJson["clazz"]
    ):
        return CODE_ARG_MISSING

    try:
        schoolId = str(reqJson["id"])
        name = str(reqJson["name"])
        clazz = str(reqJson["clazz"])
    except:
        return CODE_ARG_TYPE_ERR

    openid = session["openid"]
    user = User.fromOpenid(openid)

    if user.school_id != None:
        return CODE_ALREADY_BOUND

    bdnInfo = UserBinding.check(schoolId, name, clazz)
    if bdnInfo == None:
        return CODE_INVALID_BIND
    if bdnInfo.openid != None:
        return CODE_TARGET_BOUND

    try:
        user.name = name
        user.school_id = schoolId
        user.clazz = clazz
        bdnInfo.openid = openid

        db.session.commit()
    except:
        traceback.print_exc()
        return CODE_DATABASE_ERROR

    return CODE_SUCCESS


@authRouter.route("/profile/")
def getMyProfile():
    challengeScope(["User"])
    if not g.get("openid"):
        return CODE_NOT_LOGGED_IN

    user = User.fromOpenid(g.openid)
    if user == None:
        return CODE_ARG_INVALID

    rtn = user.profile
    rtn.update(CODE_SUCCESS)
    return rtn


@authRouter.route("/profile/email/", methods=["POST"])
@requireScope(["User"])
def setMyProfile():
    json = request.get_json()
    if not json: return CODE_ARG_INVALID
    if 'email' not in json: return CODE_ARG_MISSING
    if len(json['email']) > 64: return CODE_ARG_INVALID
    user = User.fromOpenid(g.openid)
    user.email = json['email']

    try:
        db.session.commit()
    except:
        return CODE_DATABASE_ERROR

    return CODE_SUCCESS

@authRouter.route("/profile/<openId>/", methods=["GET"])
@requireScope(["UserAdmin"])
def getProfile(openId):
    openId = str(openId)
    user = User.fromOpenid(openId)
    if user == None:
        return CODE_USER_NOT_FOUND
    profile = user.profile
    profile.update(CODE_SUCCESS)
    return profile


@authRouter.route("/user/")
@requireScope(["UserAdmin"])
def getUserList():
    PageLimit = 30

    clazz = request.args.get("clazz", None)
    page = request.args.get("p", 1, int)
    name = request.args.get("name", None)

    qry = db.session.query(User)
    if clazz:
        qry = qry.filter(User.clazz == clazz)
    if name:
        for c in "\[_%": # 替换特殊字符， `\` 需要最先替换
            name = name.replace(c, f"\\{c}")
        qry = qry.filter(User.name.like(f"%{name}%"))

    pageCount = ceil(qry.count() / PageLimit)

    qry = qry.limit(PageLimit).offset((page - 1) * PageLimit)

    qryRst = qry.all()
    proArr = [e.toDict() for e in qryRst]

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["profiles"] = proArr
    rtn["page_count"] = pageCount
    return rtn


@authRouter.route("/user/<openid>/", methods=["DELETE"])
@requireScope(["UserAdmin"])
def unbindUser(openid):
    if not openid:
        return CODE_ARG_INVALID

    user = User.fromOpenid(openid)
    ubdn: UserBinding = UserBinding.fromOpenId(openid)

    if not user:
        return CODE_USER_NOT_FOUND

    if not ubdn:
        return CODE_DATABASE_CONSISTANCE_ERROR

    user.school_id = None
    user.name == None
    user.clazz = None
    ubdn.openid = None

    try:
        db.session.commit()
    except:
        traceback.print_exc()
        return CODE_DATABASE_ERROR

    return CODE_SUCCESS

########### 用户权限管理 #############

@authRouter.route("/user/<openid>/scope/", methods=["GET", "POST"])
@requireScope(["ScopeAdmin"])
def usrScopeInfo(openid):
    user = User.fromOpenid(openid)
    if not user: return CODE_USER_NOT_FOUND

    if request.method == "GET":
        rtn = { "scopes": user.entity.detailed_privilege_info }
        rtn.update(CODE_SUCCESS)
        return rtn
    elif request.method == "POST":
        json: dict = request.get_json()
        if not json: return CODE_ARG_MISSING
        if "scope" not in json: return CODE_ARG_MISSING
        if not CheckArgs.isStr(json["scope"]): return CODE_ARG_INVALID
        if "expire_at" in json and not CheckArgs.isInt(json["expire_at"]):
            return CODE_ARG_INVALID
        expire_at = json.get("expire_at", 0)

        if expire_at != 0 and expire_at < timestamp.now():
            return CODE_ARG_INVALID

        scopeStr = json["scope"]
        if scopeStr in user.privileges:
            return CODE_PRIVILEGE_EXISTED
        
        scope = Scope.fromName(scopeStr)
        if not scope: return CODE_SCOPE_NOT_FOUND

        db.session.execute(Permission.insert().values(
            entity_id = user.entity_id,
            scope_name = scope.name,
            expire_at = expire_at
        ))

        try:
            db.session.commit()
        except:
            return CODE_DATABASE_ERROR
        
        rtn = {"scopes": list(user.privileges)}
        rtn.update(CODE_SUCCESS)
        return rtn

@authRouter.route("/user/<openid>/scope/<scopeStr>/", methods=["DELETE"])
@requireScope(["ScopeAdmin"])
def delUsrScopeInfo(openid, scopeStr):
    user = User.fromOpenid(openid)
    if not user: return CODE_USER_NOT_FOUND

    found = False
    if user.entity:
        for scope in user.entity.scopes:
            if scope.name == scopeStr:
                user.entity.scopes.remove(scope)
                found = True
    
    try:
        db.session.commit()
    except:
        return CODE_DATABASE_ERROR

    if not found: return CODE_PRIVILEGE_NOT_FOUND

    rtn = {"scopes": list(user.privileges)}
    rtn.update(CODE_SUCCESS)
    return rtn


########### 组管理 ###############

@authRouter.route("/auth/group/", methods=["POST"])
@requireScope(["ScopeAdmin"])
def createGroup():
    json = request.get_json()
    if not json: return CODE_ARG_INVALID
    if "name" not in json: return CODE_ARG_MISSING
    if not CheckArgs.isStr(json["name"]): return CODE_ARG_TYPE_ERR

    name = json.get("name")
    expire_at = json.get("expire_at", 0)

    if expire_at != 0 and expire_at < timestamp.now():
        return CODE_ARG_INVALID

    if Entity.fromGroupName(name):
        return CODE_GROUP_EXISTED
    
    group = Entity(name=name, type=EntityType.Group, expire_at=expire_at)
    db.session.add(group)

    try:
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)

    return CODE_SUCCESS


@authRouter.route("/auth/group/<group_name>/", methods=["DELETE"])
@requireScope(["ScopeAdmin"])
def deleteGroup(group_name):
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND
    db.session.delete(group)
    try:
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)

    return CODE_SUCCESS


@authRouter.route("/auth/group/")
@requireScope(["ScopeAdmin"])
def listGroup():
    pageLimit = 30

    expr = request.args.get("regex")
    if expr:
        try:
            Regex.compile(expr)
        except:
            return CODE_ARG_INVALID

    page = int(request.args.get("p", "1"))

    try:
        qry = Entity.selectGroup()

        if expr:
            qry = qry.filter(Entity.name.regexp_match(expr))

        qry = qry.limit(pageLimit).offset((page - 1) * pageLimit)
        rst = qry.all()

        group_arr = [e.brief_info for e in rst]
        rtn = {
            "groups": group_arr
        }
        rtn.update(CODE_SUCCESS)
        return rtn

    except Exception as e:
        return wrap_database_error(e)


############# 组权限管理 ############
@authRouter.route("/auth/group/<group_name>/")
@requireScope(["ScopeAdmin"])
def getGroupInfo(group_name):
    if not group_name: return CODE_ARG_MISSING
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND

    user_list = []

    member_entities = group.members
    for entity in member_entities:
        user = entity.associate_user
        user_list.append(user.toDict())
    
    rtn = group.brief_info
    rtn["members"] = user_list
    rtn["privileges"] = list(group.detailed_privilege_info)
    rtn.update(CODE_SUCCESS)
    return rtn


@authRouter.route("/auth/group/<group_name>/scope/", methods=["POST"])
@requireScope(["ScopeAdmin"])
def addGroupScope(group_name):
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND

    json = request.get_json()
    if not json: return CODE_ARG_INVALID
    if "scope" not in json: return CODE_ARG_MISSING
    if not CheckArgs.isStr(json["scope"]):
        return CODE_ARG_TYPE_ERR
    scope = Scope.fromName(json["scope"])
    if not scope: return CODE_SCOPE_NOT_FOUND

    exist = selectPermission(group, scope).one_or_none()
    if exist:
        return CODE_PRIVILEGE_EXISTED

    expire_at = json.get("expire_at", 0)
    if expire_at != 0 and expire_at < timestamp.now():
        return CODE_ARG_INVALID
    
    sql = Permission.insert().values(
        entity_id=group.id,
        scope_name=scope.name,
        expire_at=expire_at
    )

    try:
        db.session.execute(sql)
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)
    
    return CODE_SUCCESS


@authRouter.route("/auth/group/<group_name>/scope/<scope_name>/", methods=["DELETE"])
@requireScope(["ScopeAdmin"])
def delGroupScope(group_name, scope_name):
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND

    scope = Scope.fromName(scope_name)
    if not scope: return CODE_SCOPE_NOT_FOUND

    exist = selectPermission(group, scope).one_or_none()
    if not exist:
        return CODE_PRIVILEGE_NOT_FOUND
    
    group.scopes.remove(scope)
    try:
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)

    return CODE_SUCCESS


############ 组员管理 ############
@authRouter.route("/auth/group/<group_name>/member/", methods=["POST"])
@requireScope(["ScopeAdmin"])
def addGroupMember(group_name):
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND

    json = request.get_json()
    if not json: return CODE_ARG_INVALID
    if "openid" not in json: return CODE_ARG_MISSING

    user = User.fromOpenid(json["openid"])
    if not user: return CODE_USER_NOT_FOUND

    if not user.entity:
        return CODE_DATABASE_CONSISTANCE_ERROR

    exist = selectEntityAssociation(group, user.entity).one_or_none()
    if exist: return CODE_GROUP_MEMBER_EXISTED

    expire_at = json.get("expire_at", 0)
    if expire_at != 0 and expire_at < timestamp.now():
        return CODE_ARG_INVALID

    try:
        sql = EntityAssociation.insert().values(
            group_id = group.id,
            member_id = user.entity.id,
            expire_at = expire_at
        )
        db.session.execute(sql)
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)

    return CODE_SUCCESS


@authRouter.route("/auth/group/<group_name>/member/<openid>/", methods=["DELETE"])
@requireScope(["ScopeAdmin"])
def delGroupMember(group_name, openid):
    group = Entity.fromGroupName(group_name)
    if not group: return CODE_GROUP_NOT_FOUND

    user = User.fromOpenid(openid)
    if not user: return CODE_USER_NOT_FOUND

    if not user.entity:
        return CODE_DATABASE_CONSISTANCE_ERROR

    exist = selectEntityAssociation(group, user.entity).one_or_none()
    if not exist: return CODE_GROUP_MEMBER_NOT_FOUND

    group.members.remove(user.entity)
    try:
        db.session.commit()
    except Exception as e:
        return wrap_database_error(e)

    return CODE_SUCCESS


####### Scope 管理 ##########
@authRouter.route("/auth/scope/")
def listScopes():
    expr = request.args.get("regex", None)
    if expr:
        try:
            Regex.compile(expr)
        except:
            return CODE_ARG_INVALID

    qry = db.session.query(Scope)

    if expr:
        qry = qry.filter(Scope.name.regexp_match(expr))
    
    pageLimit = 30
    page = int(request.args.get("p", "1"))

    qry = qry.limit(pageLimit).offset((page-1) * pageLimit)
    rst = qry.all()

    rtn = {
        "scopes": [Model.to_dict(e) for e in rst]
    }
    rtn.update(CODE_SUCCESS)

    return rtn



####### SocketIO QR Code Auth ###########
class QRAuthNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self._clients = {}
        self._codes = {}


    def on_connect(self, ):
        clients = self._clients
        codes = self._codes

        from .util import randomString

        code = randomString(16)
        if code in codes:
            return False # reject connection
        
        sid = str(request.sid)
        clients[sid] = code
        codes[code] = sid

        emit("code", code)


    def on_disconnect(self):
        clients = self._clients
        codes = self._codes

        code = clients[request.sid]
        del clients[request.sid]
        del codes[code]


qrauth_socketio = QRAuthNamespace("/auth")
socketio_app.on_namespace(qrauth_socketio)

@authRouter.route("/auth/qrcode/<code>/")
def requestQRCode(code):
    if not code: return CODE_ARG_MISSING
    if code not in qrauth_socketio._codes:
        return CODE_ARG_INVALID

    scene = "/auth/" + code
    page  = "pages/setting/auth_qr/auth_qrcode"
    version = "develop" if config == DevelopmentConfig else "release"
    check_path = config != DevelopmentConfig
    
    res: R.Response = wxapi.wx_getUnlimited(
        scene=scene,
        page=page,
        check_path=check_path,
        env_version=version,
        width=280
    )
    
    if not res:
        abort(500)

    return flask.Response(
        res.content, 
        status=200, 
        mimetype=res.headers.get("Content-Type")
    )


@authRouter.route("/auth/authencate/<code>/")
@requireScope(["User"])
def authencateQRAuth(code):
    if not code: return CODE_ARG_MISSING

    clients = qrauth_socketio._clients
    codes = qrauth_socketio._codes

    if code not in codes:
        return CODE_ARG_INVALID
    
    sid = codes[code]
    qrauth_socketio.emit("session", request.headers.get("Session"), room=sid)
    qrauth_socketio.disconnect(sid)
    return CODE_SUCCESS

########### Debug 功能 ##############

if config == DevelopmentConfig:
    @authRouter.route("/testaccount/<openid>/")
    def switchToTestAccount(openid):
        oldOpenid = session.get("openid")

        user = User.fromOpenid(openid)
        session.permanent = True
        if not user:
            if session.get("openid"): session.pop("openid")
            return {"old": oldOpenid, "current": None}
        else:
            session["openid"] = user.openid
            return {"old": oldOpenid, "current": user.openid}


    @authRouter.route("/testqrauth/")
    def testQRAuth():
        return send_file("auth/testqrauth.html")

    
    @authRouter.route("/test_authorize_qr/")
    def testAuthorizeQR():
        return send_file("auth/testqrauth_authorize.html")