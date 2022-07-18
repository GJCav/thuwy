from typing import List
from flask import request, session, g
import requests as R
import requests.exceptions as RE
import json as Json
import time as Time
import functools
import os
import traceback

from app.auth import util

from . import authRouter
from config import WX_APP_ID, WX_APP_SECRET, config, DevelopmentConfig
from app.comerrs import *
from .errcode import *
import app.checkargs as CheckArgs
from app import timetools as timestamp

from .model import (
    db,
    User,
    UserBinding
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
        db.session.query(User.openid, User.schoolId)
        .filter(User.openid == openid)
        .limit(1)
        .one_or_none()
    )

    if user == None:
        db.session.add(User(openid))
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

    if user.schoolId != None:
        return CODE_ALREADY_BOUND

    bdnInfo = UserBinding.check(schoolId, name, clazz)
    if bdnInfo == None:
        return CODE_INVALID_BIND
    if bdnInfo.openid != None:
        return CODE_TARGET_BOUND

    try:
        user.name = name
        user.schoolId = schoolId
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

    rtn = user.toDict()
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
        return CODE_ARG_INVALID
    profile = user.toDict()
    profile.update(CODE_SUCCESS)
    return profile


@authRouter.route("/user/")
@requireScope(["UserAdmin"])
def getUserList():
    PageLimit = 30

    clazz = request.args.get("clazz", None)
    page = request.args.get("p", 1, int)

    qry = db.session.query(User)
    if clazz:
        qry = qry.filter(User.clazz == clazz)

    qry = qry.limit(PageLimit).offset((page - 1) * PageLimit)

    qryRst = qry.all()
    proArr = [e.toDict() for e in qryRst]

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["profiles"] = proArr
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

    user.schoolId = None
    user.name == None
    user.clazz = None
    ubdn.openid = None

    try:
        db.session.commit()
    except:
        traceback.print_exc()
        return CODE_DATABASE_ERROR

    return CODE_SUCCESS


@authRouter.route("/user/<openid>/scope/", methods=["GET", "POST"])
@requireScope(["ScopeAdmin"])
def usrScopeInfo(openid):
    user = User.fromOpenid(openid)
    if not user: return CODE_USER_NOT_FOUND

    if request.method == "GET":
        rtn = {"scopes": list(user.privileges)}
        rtn.update(CODE_SUCCESS)
        return rtn
    elif request.method == "POST":
        json = request.get_json()
        if not json: return CODE_ARG_MISSING
        if "scope" not in json: return CODE_ARG_MISSING
        if not CheckArgs.isStr(json["scope"]): return CODE_ARG_INVALID

        scopeStr = json["scope"]
        if scopeStr in user.privileges:
            return CODE_PRIVILEGE_EXISTED
        
        scope = Scope.fromName(scope)
        if not scope: return CODE_SCOPE_NOT_FOUND

        user.entity.scopes.append(scope)

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
