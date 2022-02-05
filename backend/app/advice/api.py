from flask import request, session

from .model import db, Advice

from . import adviceRouter
from app.auth import requireScope
from app.comerrs import *
from .errcode import *
from app import adviceIdPool
from app import timetools as timestamp
from app import checkargs as CheckArgs
from app import snowflake


@adviceRouter.route("/advice/")
@requireScope(["profile admin"])
def getAdviceList():
    st = request.args.get("st", None)
    ed = request.args.get("ed", None)
    state = request.args.get("state", None, int)
    page = request.args.get("p", None)

    try:
        page = int(page)
    except:
        return CODE_ARG_TYPE_ERR

    if not CheckArgs.isUint64(page) or page <= 0:
        return CODE_ARG_INVALID

    qry = db.session.query(Advice)

    if st != None:
        try:
            st = timestamp.parseDate(st)
        except Exception as e:
            return CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id >= snowflake.makeId(st, 0, 0))

    if ed != None:
        try:
            ed = timestamp.parseDate(ed)
        except Exception as e:
            return CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id < snowflake.makeId(ed, 0, 0))

    if state != None:
        qry = qry.filter(Advice.state == state)

    qryRst = qry.limit(20).offset(20 * (page - 1)).all()

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["page"] = page
    rtn["advice"] = []
    for advice in qryRst:
        rtn["advice"].append(advice.toDict())
    return rtn


@adviceRouter.route("/advice/<int:adviceId>/")
@requireScope(["profile admin"])
def getAdviceInfo(adviceId):

    if not CheckArgs.isUint64(adviceId):
        return CODE_ARG_INVALID

    advice = Advice.queryById(adviceId)

    if not advice:
        return CODE_ADVICE_NOT_FOUND

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["advice"] = advice.toDict(True)
    return rtn


@adviceRouter.route("/advice/me/")
@requireScope(["profile"])
def getMyAdviceList():
    st = request.args.get("st", None)
    ed = request.args.get("ed", None)
    state = request.args.get("state", None, int)
    page = request.args.get("p", None)

    try:
        page = int(page)
    except:
        return CODE_ARG_TYPE_ERR

    if not CheckArgs.isUint64(page) or page <= 0:
        return CODE_ARG_INVALID

    qry = db.session.query(Advice).filter(Advice.proponent == session["openid"])

    if st != None:
        try:
            st = timestamp.parseDate(st)
        except Exception as e:
            return CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id >= snowflake.makeId(st, 0, 0))

    if ed != None:
        try:
            ed = timestamp.parseDate(ed)
        except Exception as e:
            return CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id < snowflake.makeId(ed, 0, 0))

    if state != None:
        qry = qry.filter(Advice.state == state)

    qryRst = qry.limit(20).offset(20 * (page - 1)).all()

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["page"] = page
    rtn["advice"] = []
    for advice in qryRst:
        rtn["advice"].append(advice.toDict())
    return rtn


@adviceRouter.route("/advice/<int:adviceId>/", methods=["POST"])
@requireScope(["profile"])
def responseAdvice(adviceId):
    if not CheckArgs.isUint64(adviceId):
        return CODE_ARG_INVALID

    json = request.get_json()
    if json == None:
        return CODE_ARG_INVALID
    if "response" not in json:
        return CODE_ARG_MISSING
    if not CheckArgs.isStr(json["response"]):
        return CODE_ARG_TYPE_ERR

    advice = Advice.queryById(adviceId)

    if not advice:
        return CODE_ADVICE_NOT_FOUND

    advice.response = json["response"]
    advice.state = Advice.STATE_END

    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        return CODE_DATABASE_ERROR

    return CODE_SUCCESS


@adviceRouter.route("/advice/", methods=["POST"])
@requireScope(["profile"])
def adminAdvice():
    json = request.get_json()

    if not json:
        return CODE_ARG_INVALID
    if not CheckArgs.hasAttrs(json, ["title", "content"]):
        return CODE_ARG_MISSING
    if not CheckArgs.areStr(json, ["title", "content"]):
        return CODE_ARG_TYPE_ERR

    advice = Advice()
    advice.id = adviceIdPool.next()
    advice.proponent = session["openid"]
    advice.title = json["title"]
    advice.content = json["content"]
    advice.state = Advice.STATE_WAIT

    db.session.add(advice)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return CODE_DATABASE_ERROR

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["advice-id"] = advice.id
    return rtn
