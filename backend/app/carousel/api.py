from flask import request, session
import traceback
from sqlalchemy import desc

from . import carouselRouter
from .model import CarouselMsg

from app.auth import requireScope
from app.models import db
from app.comerrs import *
from .errcode import *
from app import carouselIdPool
from app import checkargs as CheckArgs


@carouselRouter.route("/carousel/")
def getCarouselList():
    arr = [e.toDict() for e in CarouselMsg.queryCurrentMsgList()]

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["carousels"] = arr

    return rtn


@carouselRouter.route("/carousel/", methods=["POST"])
@requireScope(["profile admin"])
def addCarousel():
    json = request.get_json()

    if json == None:
        return CODE_ARG_INVALID
    if not CheckArgs.hasAttrs(json, ["st", "ed", "content"]):
        return CODE_ARG_MISSING
    if not CheckArgs.areUint64(json, ["st", "ed"]):
        return CODE_ARG_TYPE_ERR
    if json["st"] >= json["ed"]:
        return CODE_ARG_INVALID
    if not CheckArgs.isStr(json["content"]):
        return CODE_ARG_TYPE_ERR

    new = CarouselMsg()
    new.id = carouselIdPool.next()
    new.owner = session["openid"]
    new.st = json["st"]
    new.ed = json["ed"]
    new.content = json["content"]
    new.hide = 0
    new.lastVerison = None

    db.session.add(new)
    try:
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        return CODE_DATABASE_ERROR

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["id"] = new.id
    return rtn


@carouselRouter.route("/carousel/<int:carouselId>/")
@requireScope(["profile admin"])
def getCarouselInfo(carouselId):
    msg = CarouselMsg.queryById(carouselId)

    if msg == None:
        return CODE_MSG_NOT_FOUND

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["carousel"] = msg.toDict(True)

    return rtn


@carouselRouter.route("/carousel/<int:carouselId>/", methods=["POST"])
@requireScope(["profile admin"])
def modifyCarouselMsg(carouselId):
    msg = CarouselMsg.queryById(carouselId)
    if msg == None:
        return CODE_MSG_NOT_FOUND

    json = request.get_json()
    if json == None:
        return CODE_ARG_INVALID

    new = msg.clone()
    hasChange = False

    if "st" in json:
        if not CheckArgs.isUint64(json["st"]):
            return CODE_ARG_TYPE_ERR
        new.st = json["st"]
        hasChange = True

    if "ed" in json:
        if not CheckArgs.isUint64(json["ed"]):
            return CODE_ARG_TYPE_ERR
        new.ed = json["ed"]
        hasChange = True

    if "content" in json:
        if not CheckArgs.isStr(json["content"]):
            return CODE_ARG_TYPE_ERR
        new.content = json["content"]
        hasChange = True

    if "hide" in json:
        if not CheckArgs.isInt(json["hide"]):
            return CODE_ARG_TYPE_ERR
        new.hide = json["hide"]
        hasChange = True

    rtn = {}

    if hasChange:
        new.lastVerison = msg.id
        msg.hide = True
        rtn["id"] = new.id

        db.session.add(new)
        try:
            db.session.commit()
        except:
            traceback.print_exc()
            return CODE_DATABASE_ERROR
    else:
        rtn["id"] = msg.id

    rtn.update(CODE_SUCCESS)
    return rtn


@carouselRouter.route("/carousel/history/", methods=["POST"])
@requireScope(["profile admin"])
def getHistory():
    qry = db.session.query(CarouselMsg)

    st = request.args.get("st", None)
    if st != None:
        if not CheckArgs.isUint64(st):
            return CODE_ARG_TYPE_ERR
        qry = qry.filter(CarouselMsg.st >= int(st))

    ed = request.args.get("ed", None)
    if ed != None:
        if not CheckArgs.isUint64(ed):
            return CODE_ARG_TYPE_ERR
        qry = qry.filter(CarouselMsg.ed <= int(ed))

    hide = request.args.get("hide", None)
    if hide != None:
        if not CheckArgs.isUint64(hide):
            return CODE_ARG_TYPE_ERR
        qry = qry.filter(CarouselMsg.hide == int(hide))

    lastVersion = request.args.get("last-ver", None)
    if lastVersion != None:
        if not CheckArgs.isUint64(lastVersion):
            return CODE_ARG_TYPE_ERR
        qry = qry.filter(CarouselMsg.lastVerison == int(lastVersion))

    page = request.args.get("page", 1, int)
    if not CheckArgs.isUint64(page):
        return CODE_ARG_TYPE_ERR

    arr = qry.order_by(desc(CarouselMsg.id)).limit(20).offset((page - 1) * 20).all()
    arr = [e.toDict(True) for e in arr]

    rtn = {}
    rtn.update(CODE_SUCCESS)
    rtn["carousels"] = arr

    return rtn
