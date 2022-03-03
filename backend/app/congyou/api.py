from crypt import methods
from flask import request
from flask import g

from app.comerrs import *
from app.auth import requireScope, challengeScope
import app.checkargs as CheckArgs
import app.timetools as Timetools

from .model import *
from . import congyouRouter
from .errcode import *

def goodTimeSpace(deadline: int, holding_time: int) :
    return deadline > Timetools.daysAfter(2) and holding_time >= Timetools.daysAfter(2, deadline) 

@congyouRouter.route("/lecture/", methods=["GET", "POST"])
@requireScope(["profile", "congyou profile"])
def lectureList():
    if request.method == "GET" and challengeScope(["profile"]):  # 获取从游坊列表
        page = request.args.get("p", "1")
        try:
            page = int(page)
        except:
            return CODE_ARG_TYPE_ERR
        page -= 1
        if not CheckArgs.isUint64(page):
            return CODE_ARG_INVALID

        qry = (
            db.session.query(Lecture)
            .filter(Lecture.visible == 1)
            .order_by(Lecture.deadline.desc())
        )

        if "subject" in request.args:
            subject = request.args.get("subject", None, str)
            if subject:
                qry = qry.filter(Lecture.subject == subject)

        if "state" in request.args:
            state = request.args.get("state", None, int)
            if state:
                if state == 1 :
                    qry = qry.filter(Lecture.drawn == 0, Lecture.deadline > Timetools.now())
                elif state == 2 :
                    qry = qry.filter(Lecture.drawn == 0, Lecture.deadline <= Timetools.now())
                elif state == 3 :
                    qry = qry.filter(Lecture.drawn == 1, Lecture.holding_time > Timetools.now())
                elif state == 4 :
                    qry = qry.filter(Lecture.drawn == 1, Lecture.holding_time <= Timetools.now())

        lectureCount = qry.count()
        lectures = qry.limit(20).offset(20 * page).all()

        lectures = [e.toDictNoDetail() for e in lectures]

        ret = {
            "lecture-count": lectureCount, 
            "page": page + 1, 
            "lectures": lectures
        }
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "POST" and challengeScope(["profile congyou"]): # 添加从游坊
        reqJson = request.json
        if reqJson == None:
            return CODE_ARG_INVALID
        if not CheckArgs.hasAttrs(
            reqJson, ["title", "theme", "position", "total", "subject", "teacher", "brief-intro", "detail-intro", "deadline", "holding_time"]):
            return CODE_ARG_MISSING
        if ((
            not CheckArgs.areStr(
                reqJson, ["title", "theme", "position", "subject", "teacher", "brief-intro"]
            ))or (not CheckArgs.areInt(
                reqJson, ["total"]
            ))or (not CheckArgs.areUint64(
                reqJson, ["deadline", "holding_time"]
            ))):
            return CODE_ARG_TYPE_ERR
        
        if not goodTimeSpace(reqJson["deadline"], reqJson["holding_time"]) :
            return CODE_ARG_INVALID

        lecture = Lecture()
        try:
            lecture.user_id = g.openid
            lecture.position = reqJson["position"]
            lecture.title = reqJson["title"]
            lecture.theme = reqJson["theme"]
            lecture.visible = 1
            lecture.total = reqJson["total"]
            lecture.subject = reqJson["subject"]
            lecture.teacher = reqJson["teacher"]
            lecture.brief_intro = reqJson["brief-intro"]
            lecture.detail_intro = reqJson["detail-intro"]
            lecture.deadline = reqJson["deadline"]
            lecture.holding_time = reqJson["holding_time"]
        except:
            return CODE_ARG_TYPE_ERR

        try:
            db.session.add(lecture)
            db.session.commit()
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR

        ret = {"Lecture-id": lecture.lecture_id}
        ret.update(CODE_SUCCESS)
        return ret

    return CODE_ACCESS_DENIED

@congyouRouter.route("/lecture/<int:lectureId>/", methods=["GET", "POST", "DELETE"])
@requireScope(["profile", "profile congyou"])
def lectureDetail(lectureId: int):
    if not CheckArgs.isInt(lectureId):
        return CODE_ARG_INVALID

    dataLecture = db.session.query(Lecture).filter(Lecture.lecture_id == lectureId)
    lecture: Lecture = dataLecture.one_or_none()
    if not lecture:
        return CODE_LECTURE_NOT_FOUND

    dataLecture = db.session.query(Lecture).filter(Lecture.lecture_id == lectureId)

    if request.method == "GET" and challengeScope(["profile"]): # 获取从游坊详细信息
        ret = {"lecture": lecture.toDict()}
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "POST" and challengeScope(["profile congyou"]): # 修改从游坊        
        if lecture.getstate() != 1 :
            return CODE_LECTURE_DRAWING    

        reqJson = request.json
        try:
            if "theme" in reqJson:
                lecture.theme = str(reqJson["theme"])
            if "title" in reqJson:
                lecture.title = str(reqJson["title"])
            if "position" in reqJson :
                lecture.position = str(reqJson["position"])
            if "total" in reqJson:
                lecture.total = int(reqJson["total"])
            if "subject" in reqJson:
                lecture.subject = str(reqJson["subject"])
            if "teacher" in reqJson:
                lecture.teacher = str(reqJson["teacher"])
            if "brief-intro" in reqJson:
                lecture.brief_intro = str(reqJson["brief-intro"])
            if "detail-intro" in reqJson:
                lecture.detail_intro = reqJson["detail-intro"]
            if "deadline" in reqJson:
                if not CheckArgs.isUint64(reqJson["deadline"]):
                    return CODE_ARG_TYPE_ERR
                lecture.deadline = reqJson["deadline"]
            if "holding_time" in reqJson:
                if not CheckArgs.isUint64(reqJson["holding_time"]):
                    return CODE_ARG_TYPE_ERR
                lecture.holding_time = reqJson["holding_time"]
        except:
            return CODE_ARG_TYPE_ERR
        
        if not goodTimeSpace(lecture.deadline, lecture.holding_time) :
            db.session.rollback()
            return CODE_ARG_INVALID

        try:
            db.session.commit()
            return CODE_SUCCESS
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR

    elif request.method == "DELETE" and challengeScope(["profile congyou"]): # 删除从游坊
        if lecture.getstate() != 1 :
            return CODE_LECTURE_DRAWING    

        try:
            dataLecture.delete()
            db.session.commit()
            return CODE_SUCCESS
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR

    return CODE_ACCESS_DENIED

def not_a_wish(wish) :
    return wish < 1 or wish > 3

def Enrollment_a_Lecture(lecture_id, user_id, wish, state, errmsg) :
    lecture : Lecture = (
            db.session.query(Lecture)
            .filter(Lecture.lecture_id == lecture_id)
            .one_or_none()
        )

    if not lecture :
            return CODE_LECTURE_NOT_FOUND
    if lecture.getstate() != state :
        return errmsg
    
    erollmented : Lecture_enrollment = (
            db.session.query(Lecture_enrollment)
            .filter(Lecture_enrollment.lecture_id == lecture_id, 
                    Lecture_enrollment.user_id == user_id)
            .one_or_none()
        )
    if erollmented :
        return CODE_ENROLLMENTED
    
    if getWishRemain(wish, user_id) < 1 :
            return CODE_WISH_NOT_ENOUGH[wish]
    
    enrollment = Lecture_enrollment()
    enrollment.lecture_id = lecture_id
    enrollment.user_id = user_id
    enrollment.wish = wish

    try:
        db.session.add(enrollment)
        db.session.commit()
    except:
        db.session.rollback()
        return CODE_DATABASE_ERROR

    ret = {"enrollment_id": enrollment.enrollment_id}
    ret.update(CODE_SUCCESS)
    return ret


@congyouRouter.route("/lecture_enrollment/", methods=["GET", "POST"])
@requireScope(["profile"])
def lectureEnrollmentList():
    if request.method == "POST":  # 普通用户报名从游坊
        reqJson = request.json
        if reqJson == None :
            return CODE_ARG_INVALID
        if not CheckArgs.hasAttrs(
            reqJson, ["lecture_id", "wish"]):
            return CODE_ARG_MISSING
        if not CheckArgs.areInt(
            reqJson, ["lecture_id", "wish"]):
            return CODE_ARG_TYPE_ERR

        lecture_id = reqJson["lecture_id"]

        wish = reqJson["wish"]
        if not_a_wish(wish) :
            return CODE_ARG_INVALID
        
        return Enrollment_a_Lecture(lecture_id, g.openid, wish, 1, CODE_LECTURE_DRAWING)

    elif request.method == "GET":  # 用户获取自己报名的从游坊
        page = request.args.get("p", "1")
        try:
            page = int(page)
        except:
            return CODE_ARG_TYPE_ERR
        page -= 1
        if not CheckArgs.isUint64(page):
            return CODE_ARG_INVALID
        
        qry = (
            db.session.query(Lecture_enrollment)
            .join(Lecture)
            .filter(Lecture_enrollment.user_id == g.openid)
            .order_by(Lecture.deadline.desc())
        )

        if "subject" in request.args:
            subject = request.args.get("subject", None, str)
            if subject:
                qry = qry.filter(Lecture.subject == subject)
        
        if "state" in request.args:
            state = request.args.get("state", None, int)
            if state:
                if state == 1 :
                    qry = qry.filter(Lecture.drawn == 0)
                elif state == 2 :
                    qry = qry.filter(Lecture_enrollment.lottery == 0)
                elif state == 3 :
                    qry = qry.filter(Lecture_enrollment.lottery == 1)
                elif state == 4 :
                    qry = qry.filter(Lecture_enrollment.delete == 1)

        enrollmentCount = qry.count()
        enrollments : List["Lecture_enrollment"] = qry.limit(20).offset(20 * page).all()

        enrollments = [e.toDict() for e in enrollments]

        ret = {
            "lecture-count": enrollmentCount, 
            "page": page + 1, 
            "enrollments": enrollments
        }
        ret.update(CODE_SUCCESS)
        return ret

@congyouRouter.route("/modi_enrollment/", methods = ["POST"])
@requireScope(["congyou profile"])
def modyEnrollment(): # 从游部手动为用户报名
    reqJson = request.json
    if reqJson == None :
        return CODE_ARG_INVALID
    if not CheckArgs.hasAttrs(
        reqJson, ["lecture_id", "user_id"]):
        return CODE_ARG_MISSING
    
    lecture_id = reqJson["lecture_id"]
    if not CheckArgs.isUint64(lecture_id) :
        return CODE_ARG_TYPE_ERR
    
    user_id = reqJson["user_id"]
    if not CheckArgs.isStr(user_id) :
        return CODE_ARG_TYPE_ERR
    
    return Enrollment_a_Lecture(lecture_id, user_id, 4, 3, CODE_LECTURE_STATE_NOT3)


@congyouRouter.route("/lecture_enrollment/<int:enrollmentId>/", methods=["POST", "DELETE"])
@requireScope(["profile"])
def lectureEnrollmentModify(enrollmentId: int):
    if not CheckArgs.isInt(enrollmentId):
        return CODE_ARG_INVALID
    dataEnrollment = (
        db.session.query(Lecture_enrollment)
        .filter(Lecture_enrollment.enrollment_id == enrollmentId)
    )
    enrollment : Lecture_enrollment = dataEnrollment.one_or_none()

    if not enrollment :
        return CODE_ENROLLMENT_NOT_FOUND
    if enrollment.user_id != g.openid :
        return CODE_ACCESS_DENIED

    lecture = enrollment.lecture

    if request.method == "POST":  # 普通用户修改报名的从游坊
        if lecture.getstate() != 1 :
            return CODE_LECTURE_DRAWING

        reqJson = request.json
        if reqJson == None :
            return CODE_ARG_INVALID
        if not reqJson.get("wish") :
            return CODE_ARG_MISSING
        if not CheckArgs.isInt(reqJson["wish"]) :
            return CODE_ARG_TYPE_ERR
        
        wish = reqJson["wish"]
        if not_a_wish(wish) :
            return CODE_ARG_INVALID
        
        if getWishRemain(wish, g.openid) < 1 :
            return CODE_WISH_NOT_ENOUGH[wish]

        enrollment.wish = wish
        enrollment.enrollment_time = Timetools.now()

        try :
            db.session.commit()
            return CODE_SUCCESS
        except :
            db.session.rollback()
            return CODE_DATABASE_ERROR

    elif request.method == "DELETE": # 普通用户取消报名
        try:
            if lecture.getstate() == 1 or (lecture.getstate() == 3 and enrollment.lottery == 0) :
                dataEnrollment.delete() # 这样删除后不消耗用户志愿
                db.session.commit()
                return CODE_SUCCESS
            elif lecture.getstate() == 2 :
                db.session.rollback()
                return CODE_LECTURE_DRAWING
            elif lecture.getstate() == 3 and enrollment.lottery == 1 : 
                enrollment.delete = 1 # 这样删除后消耗用户志愿
                db.session.commit()
                return CODE_SUCCESS
            elif lecture.getstate() == 4 :
                db.session.rollback()
                return CODE_LECTURE_FINISH
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR


@congyouRouter.route("/modi_enrollment/<int:enrollmentId>/", methods = ["DELETE"])
@requireScope(["congyou profile"])
def delEnrollment(enrollmentId : int) : # 从游部为用户手动取消报名
    if not CheckArgs.isInt(enrollmentId):
        return CODE_ARG_INVALID
    dataEnrollment = (
        db.session.query(Lecture_enrollment)
        .filter(Lecture_enrollment.enrollment_id == enrollmentId)
    )
    enrollment : Lecture_enrollment = dataEnrollment.one_or_none()

    if not enrollment :
        return CODE_ENROLLMENT_NOT_FOUND
    
    lecture = enrollment.lecture
    if lecture.getstate() != 3 :
        return CODE_LECTURE_STATE_NOT3
    
    try :
        dataEnrollment.delete() # 这样删除后不消耗用户志愿
        db.session.commit()
        return CODE_SUCCESS
    except :
        db.session.rollback()
        return CODE_DATABASE_ERROR


@congyouRouter.route("/congyou_enrollment/<int:lectureId>/", methods = ["GET", "POST"])
@requireScope(["congyou profile"])
def GetLectureEnrollments(lectureId: int) :
    if not CheckArgs.isInt(lectureId):
        return CODE_ARG_INVALID
    
    lecture : Lecture = db.session.query(Lecture).filter(Lecture.lecture_id == lectureId).one_or_none()
    if not lecture :
        return CODE_LECTURE_NOT_FOUND

    if request.method == "GET" : # 从游部查看从游坊报名信息
        page = request.args.get("p", "1")
        try:
            page = int(page)
        except:
            return CODE_ARG_TYPE_ERR
        page -= 1
        if not CheckArgs.isUint64(page):
            return CODE_ARG_INVALID
        
        qry = (
            db.session.query(Lecture_enrollment).join(Lecture)
            .filter(Lecture.lecture_id == lectureId)
            .order_by(Lecture_enrollment.wish)
        )

        if "state" in request.args :
            state = request.args.get("state", None, int)
            if state :
                if state == 1 :
                    qry = qry.filter(Lecture.drawn == 0)
                elif state == 2 :
                    qry = qry.filter(Lecture_enrollment.lottery == 0)
                elif state == 3 :
                    qry = qry.filter(Lecture_enrollment.lottery == 1)
                elif state == 4 :
                    qry = qry.filter(Lecture_enrollment.delete == 1)
        
        enrollmentCount = qry.count()
        enrollments : List["Lecture_enrollment"] = qry.limit(20).offset(20 * page).all()

        enrollments = [e.toDict() for e in enrollments]

        ret = {
            "enrollment-count" : enrollmentCount, 
            "page" : page + 1, 
            "lecture" : lecture.toDictNoDetail(), 
            "enrollments" : enrollments
        }
        ret.update(CODE_SUCCESS)
        return ret

    if request.method == "POST" : # 从游部提前开始从游坊抽签
        if lecture.getstate() != 2 :
            return CODE_LECTURE_NOT_DRAWING
        lecture.updatedraw()


@congyouRouter.route("/wish_remain/", methods=["GET"])
@requireScope(["profile"])
def userWish(): # 用户获取自己还剩多少志愿
    ret = {"first": getWishRemain(1, g.openid), 
            "second": getWishRemain(2, g.openid)}
    ret.update(CODE_SUCCESS)
    return ret
