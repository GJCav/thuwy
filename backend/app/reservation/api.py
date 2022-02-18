from flask import request, session
import json as Json
import time as Time
from sqlalchemy import desc

from . import rsvRouter

from app import rsvIdPool, MACHINE_ID
from .errcode import *
from app.comerrs import *
import app.checkargs as CheckArgs
from . import rsv_state as RsvState
from .model import *
from app.models import _Dict
from app.auth import requireScope
import app.timetools as timestamp
import app.snowflake as Snowflake

from config import userSysName

from app.reservation.email import sendEmailByTHUWY, MANAGER_NAMES, MANAGER_EMAILS
from app.reservation.subscription import sendRsvSubscMsg

@rsvRouter.route("/reservation/")
@requireScope(["profile admin"])
def getRsvList():

    qry = db.session.query(Reservation).order_by(desc(Reservation.id))

    st = request.args.get("st")
    ed = request.args.get("ed")
    state = request.args.get("state", None, type=int)
    method = request.args.get("method", None, type=int)
    p = request.args.get("p", 1, type=int)

    if st:
        if not CheckArgs.isDate(st):
            return CODE_ARG_FORMAT_ERR
        st = timestamp.parseDate(st)
        qry = qry.filter(Reservation.st >= st)

    if ed and CheckArgs.isDate(ed):
        if not CheckArgs.isDate(ed):
            return CODE_ARG_FORMAT_ERR
        ed = timestamp.parseDate(ed)
        qry = qry.filter(Reservation.ed < ed)

    if state != None:
        qry = qry.filter(Reservation.state.op("&")(state))

    if method != None:
        qry = qry.filter(Reservation.method == method)

    qryRst = qry.limit(20).offset(20 * (p - 1)).all()

    arr = []
    groupRsvSet = set()
    for rsv in qryRst:
        if rsv.id in groupRsvSet:
            continue

        if LongTimeRsv.isChildRsv(rsv):
            rsv = LongTimeRsv.getFatherRsv(rsv)
            if state != None and not (
                rsv.state & state
            ):  # 父节点state更新，但子节点state不会更新，所以要多检测一遍
                # 现在的情况是其他函数保证子预约state的更新是同步的，但还是保留把。
                continue

        if LongTimeRsv.isFatherRsv(rsv):
            choreJson = Json.loads(rsv.chore)
            groupRsvSet |= set(choreJson["group-rsv"]["sub-rsvs"])
            groupRsvSet.add(rsv.id)

        arr.append(rsv.toDict())

    rtn = {"page": p, "rsvs": arr}
    rtn.update(CODE_SUCCESS)

    return rtn


@rsvRouter.route("/reservation/", methods=["POST"])
@requireScope(["profile"])
def reserve():
    reqJson: dict = request.get_json()
    if not reqJson or not CheckArgs.hasAttrs(
        reqJson, ["item-id", "method", "reason", "interval"]
    ):

        return CODE_ARG_MISSING

    if not CheckArgs.areStr(reqJson, ["reason"]) or not CheckArgs.areInt(
        reqJson, ["item-id", "method"]
    ):

        return CODE_ARG_TYPE_ERR

    itemId = reqJson["item-id"]
    reason = reqJson["reason"]
    method = reqJson["method"]

    supportedMethod = Item.querySupportedMethod(itemId)
    if supportedMethod == None:
        return CODE_ITEM_NOT_FOUND
    if not CheckArgs.isPowOf2(method):
        return CODE_DUPLICATE_METHOD
    if not supportedMethod & method:
        return CODE_METHOD_NOT_SUPPORT

    if method == LongTimeRsv.methodValue:
        if not isinstance(reqJson["interval"], list):
            return CODE_ARG_TYPE_ERR
        if len(reqJson["interval"]) == 0:
            return CODE_ARG_MISSING

        interval: list = reqJson["interval"]
        rsvGroup = []
        for itl in interval:
            st, ed = LongTimeRsv.parseInterval(itl)
            if ed == None:
                return CODE_ARG_FORMAT_ERR  # date str fmt error
            elif ed == -1:
                return CODE_ARG_INVALID  # date is not saturday, time code invalid

            if st > timestamp.aWeekAfter() or ed < timestamp.now():
                return CODE_TIME_OUT_OF_RANGE

            new = _Dict()
            new.id = rsvIdPool.next()
            new.st = st
            new.ed = ed
            new.itemId = itemId
            new.chore = {"group-rsv": {}}  # remember to cast to str
            rsvGroup.append(new)

        rsvGroup[0].chore["group-rsv"]["sub-rsvs"] = []
        for i in range(1, len(rsvGroup)):
            rsvGroup[0].chore["group-rsv"]["sub-rsvs"].append(rsvGroup[i].id)
            rsvGroup[i].chore["group-rsv"]["fth-rsv"] = rsvGroup[0].id

        for cur, e in enumerate(rsvGroup):
            if Reservation.hasTimeConflict(e):
                return CODE_TIME_CONFLICT

            for i in range(
                cur
            ):  # 避免内部出现时间冲突，防止有尝试传入 ['2021-5-16 1', '2021-5-16 1'] 这种导致bug
                if (
                    e.st <= rsvGroup[i].st < e.ed
                    or e.st < rsvGroup[i].ed < e.ed
                    or rsvGroup[i].st <= e.st
                    and e.ed <= rsvGroup[i].ed
                ):
                    return CODE_TIME_CONFLICT

        rsvGroup = [
            Reservation(
                id=e.id,
                itemId=itemId,
                guest=session["openid"],
                reason=reason,
                method=method,
                st=e.st,
                ed=e.ed,
                state=RsvState.STATE_WAIT,
                approver=None,
                examRst=None,
                chore=Json.dumps(e.chore),
            )
            for e in rsvGroup
        ]
        db.session.add_all(rsvGroup)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error: " + str(e))
            return CODE_DATABASE_ERROR

        finalRsv = rsvGroup[0]

    elif method == FlexTimeRsv.methodValue:
        if not isinstance(reqJson["interval"], str):
            return CODE_ARG_TYPE_ERR

        interval = reqJson["interval"]

        st, ed = FlexTimeRsv.parseInterval(interval)
        if ed == None:
            return CODE_ARG_FORMAT_ERR
        elif ed == -1:
            return CODE_ARG_INVALID

        if st > timestamp.aWeekAfter() or ed < timestamp.now():
            return CODE_TIME_OUT_OF_RANGE

        r = Reservation()
        r.id = rsvIdPool.next()
        r.itemId = itemId
        r.guest = session["openid"]
        r.reason = reason
        r.method = method
        r.state = RsvState.STATE_WAIT
        r.chore = ""
        r.st, r.ed = st, ed

        if r.hasTimeConflict():
            return CODE_TIME_CONFLICT

        db.session.add(r)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error: " + str(e))
            return CODE_DATABASE_ERROR

        finalRsv = r

    else:
        return CODE_ARG_INVALID

    rtn = {}

    if Item.Attr.isAutoAccept(Item.Attr.queryAttrById(finalRsv.itemId)):
        finalRsv.examRst = f"auto accept by {userSysName}"
        finalRsv.approver = userSysName
        finalRsv.changeState(RsvState.STATE_START)
        try:
            db.session.commit()
            rtn["auto-accept"] = "success"
        except Exception as e:
            print(e)
            rtn["auto-accept"] = "fail"

    rtn.update(          )
    rtn["rsv-id"] = finalRsv.id

    sendRsvSubscMsg(finalRsv)
    sendEmailByTHUWY(1, MANAGER_NAMES, MANAGER_EMAILS)

    return rtn


@rsvRouter.route("/reservation/me/")
@requireScope(["profile"])
def querymyrsv():
    openid = session["openid"]

    def makeSnowId(date, flow):
        return Snowflake.makeId(
            Time.mktime(Time.strptime(date, "%Y-%m-%d")), MACHINE_ID, flow
        )

    sql = (
        db.session.query(Reservation)
        .filter(Reservation.guest == openid)
        .order_by(desc(Reservation.id))
    )

    st = request.args.get("st", None)
    if st and CheckArgs.isDate(st):
        try:
            stId = makeSnowId(st, 0)
            sql = sql.filter(Reservation.id >= stId)
        except:
            return CODE_ARG_INVALID

    ed = request.args.get("ed", None)
    if ed and CheckArgs.isDate(ed):
        try:
            edId = makeSnowId(ed, 0)
            sql = sql.filter(Reservation.ed <= edId)
        except:
            return CODE_ARG_INVALID

    state = request.args.get("state", None, type=int)
    if state != None:
        sql = sql.filter(Reservation.state.op("&")(state))

    # rsvJsonArr = mergeAndBeautify(sql.all())

    rsvJsonArr = []
    groupRsvSet = set()
    for rsv in sql.all():
        if rsv.id in groupRsvSet:
            continue

        if LongTimeRsv.isChildRsv(rsv):
            rsv = LongTimeRsv.getFatherRsv(rsv)

        if LongTimeRsv.isFatherRsv(rsv):
            choreJson = Json.loads(rsv.chore)
            groupRsvSet |= set(choreJson["group-rsv"]["sub-rsvs"])
            groupRsvSet.add(rsv.id)

        rsvJsonArr.append(rsv.toDict())

    def _pcs(e):
        del e["guest"]
        return e

    rst = {}
    rst.update(CODE_SUCCESS)
    rst["my-rsv"] = [_pcs(e) for e in rsvJsonArr]
    return rst


@rsvRouter.route("/reservation/<int:rsvId>/", methods=["GET"])
def getRsvInfo(rsvId):
    if rsvId < 0 or rsvId > (1 << 65) - 1:
        return CODE_ARG_INVALID

    rsv = Reservation.fromRsvId(rsvId)
    if not rsv:
        return CODE_RSV_NOT_FOUND

    if rsv.method == LongTimeRsv.methodValue:
        rsv = LongTimeRsv.getFatherRsv(rsv)

    if rsv.method == LongTimeRsv.methodValue:
        rsvJson = LongTimeRsv.toDict(rsv)
    elif rsv.method == FlexTimeRsv.methodValue:
        rsvJson = FlexTimeRsv.toDict(rsv)
    else:
        return CODE_DATABASE_ERROR  # 如果执行这个分支，说明存在外部添加 Rsv 的行为，或代码出Bug

    rtn = {"rsv": rsvJson}
    rtn.update(CODE_SUCCESS)
    return rtn


@rsvRouter.route("/reservation/<int:rsvId>/", methods=["POST"])
@requireScope(["profile admin"])
def modifyRsv(rsvId):
    rsv: Reservation = Reservation.query.filter(Reservation.id == rsvId).one_or_none()

    if not rsv:
        return CODE_RSV_NOT_FOUND
    json = request.get_json()
    op = json.get("op")
    if op == None:
        return CODE_ARG_MISSING
    if not CheckArgs.isInt(op):
        return CODE_ARG_TYPE_ERR

    if op == 1:
        return examRsv(rsv, json)
    elif op == 2:
        return completeRsv(rsv)
    else:
        return CODE_SERVER_BUGS


def examRsv(rsv: Reservation, json):
    if RsvState.isStart(rsv.state):
        return CODE_RSV_START
    if RsvState.isReject(rsv.state):
        return CODE_RSV_REJECTED
    if RsvState.isComplete(rsv.state):
        return CODE_RSV_COMPLETED

    if not CheckArgs.hasAttrs(json, ["pass", "reason"]):
        return CODE_ARG_MISSING
    if not CheckArgs.areInt(json, ["pass"]):
        return CODE_ARG_TYPE_ERR
    if not CheckArgs.areStr(json, ["reason"]):
        return CODE_ARG_TYPE_ERR

    # if rsv.method == LongTimeRsv.getFatherRsv:
    #     rsv = LongTimeRsv.getFatherRsv(rsv)

    pazz = json["pass"]
    reason = json["reason"]
    rsv.examRst = reason
    rsv.approver = session["openid"]

    if pazz == 0:
        rsv.changeState(RsvState.COMPLETE_BY_REJECT)  # 对于LongTimeRsv可以保证更新子预约的状态，方便筛选
    elif pazz == 1:
        rsv.changeState(RsvState.STATE_START)
    else:
        return CODE_ARG_INVALID

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return CODE_DATABASE_ERROR

    sendRsvSubscMsg(rsv)

    return CODE_SUCCESS


def completeRsv(rsv: Reservation):
    if RsvState.isWait(rsv.state):
        return CODE_RSV_WAITING
    if RsvState.isComplete(rsv.state):
        return CODE_RSV_COMPLETED
    if not RsvState.isStart(rsv.state):
        return CODE_SERVER_BUGS

    rsv.changeState(RsvState.STATE_COMPLETE)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return CODE_DATABASE_ERROR

    sendRsvSubscMsg(rsv)

    return CODE_SUCCESS


@rsvRouter.route("/reservation/<int:rsvId>/", methods=["DELETE"])
@requireScope(["profile"])
def cancelRsv(rsvId):

    rsv: Reservation = Reservation.query.filter(Reservation.id == rsvId).one_or_none()

    if not rsv:
        return CODE_RSV_NOT_FOUND
    if RsvState.isReject(rsv.state):
        return CODE_RSV_REJECTED
    if RsvState.isComplete(rsv.state):
        return CODE_RSV_COMPLETED
    if rsv.isBegan():
        return CODE_RSV_START

    rsv.changeState(RsvState.COMPLETE_BY_CANCEL)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return CODE_DATABASE_ERROR

    sendRsvSubscMsg(rsv)
    
    return CODE_SUCCESS
