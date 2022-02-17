from flask import request
from flask import g

from app.comerrs import *
from app.auth import requireScope, challengeScope
import app.checkargs as CheckArgs
import app.timetools as Timetools

from .model import *
from . import congyouRouter
from .errcode import *

######################################## TODO 定时更新或多线程操作


def goodTimeSpace(deadline: int, holding_time: int) :
    return holding_time >= Timetools.hoursAfter(deadline, 2)

@congyouRouter.route("/lecture/", methods=["GET", "POST"])
@requireScope(["profile", "congyou profile"])
def lectureList():
    if request.method == "GET" and challengeScope(["profile"]):
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
                qry = qry.filter(Lecture.state == state)

        lectureCount = qry.count()
        lectures = qry.limit(20).offset(20 * page).all()

        for e in lectures :
            e.updatestate()

        lectures = [e.toDictNoDetail() for e in lectures]

        ret = {
            "lecture-count": lectureCount, 
            "page": page, 
            "lectures": lectures
        }
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "POST" and challengeScope(["profile congyou"]):
        reqJson = request.json
        if reqJson == None:
            return CODE_ARG_INVALID
        if not CheckArgs.hasAttrs(
            reqJson, ["title", "theme", "total", "subject", "teacher", "brief-intro", "detail-intro", "deadline", "holding_time"]):
            return CODE_ARG_MISSING
        if ((
            not CheckArgs.areStr(
                reqJson, ["title", "theme", "subject", "teacher", "brief-intro"]
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
            lecture.title = reqJson["title"]
            lecture.theme = reqJson["theme"]
            lecture.state = 1
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


@congyouRouter.route("/lecture/<int:lectureId>/", methods=["GET", "POST", "DELETE"])
@requireScope(["profile", "profile congyou"])
def lectureDetail(lectureId: int):
    if not CheckArgs.isInt(lectureId):
        return CODE_ARG_INVALID

    dataLecture = db.session.query(Lecture).filter(Lecture.lecture_id == lectureId)
    lecture: Lecture = dataLecture.one_or_none()
    if not lecture:
        return CODE_LECTURE_NOT_FOUND

    lecture.updatestate()
    dataLecture = db.session.query(Lecture).filter(Lecture.lecture_id == lectureId)

    if request.method == "GET" and challengeScope(["profile"]):
        ret = {"lecture": lecture.toDict()}
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "POST" and challengeScope(["profile congyou"]):
        reqJson = request.json
        try:
            if "theme" in reqJson:
                lecture.theme = str(reqJson["theme"])
            if "title" in reqJson:
                lecture.title = str(reqJson["title"])
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

    elif request.method == "DELETE" and challengeScope(["profile congyou"]):
        try:
            dataLecture.delete()
            db.session.commit()
            return CODE_SUCCESS
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR

def not_a_wish(wish) :
    return wish < 1 or wish > 3

@congyouRouter.route("/lecture_enrollment/", methods=["GET", "POST"])
@requireScope(["profile"])
def lectureEnrollmentList():
    if request.method == "POST":  
        reqJson = request.json
        if reqJson == None :
            return CODE_ARG_INVALID
        if not CheckArgs.hasAttrs(
            reqJson, ["lecture_id", "wish"]):
            return CODE_ARG_MISSING
        if not CheckArgs.areInt(
            reqJson, ["lecture_id", "wish"]):
            return CODE_ARG_TYPE_ERR
        
        wish = reqJson["wish"]
        if not_a_wish(wish) :
            return CODE_ARG_INVALID
        
        if getWishRemain(wish, g.openid) < 1 :
            return CODE_WISH_NOT_ENOUGH[wish]

        lecture_id = reqJson["lecture_id"]
        
        lecture : Lecture = (
            db.session.query(Lecture)
            .filter(Lecture.lecture_id == lecture_id)
            .one_or_none()
        )

        if not lecture :
            return CODE_LECTURE_NOT_FOUND

        lecture.updatestate()

        if lecture.state != 1 :
            return CODE_LECTURE_CANT_ENROLLMENT

        enrollment = Lecture_enrollment()
        enrollment.lecture_id = lecture_id
        enrollment.user_id = g.openid
        enrollment.wish = wish
        enrollment.state = 2
        enrollment.delete = 0
        enrollment.enrollment_time = Timetools.now()

        try:
            db.session.add(enrollment)
            db.session.commit()
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR

        ret = {"enrollment_id": enrollment.enrollment_id}
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "GET": 
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
                qry = qry.filter(Lecture.state == state)

        enrollmentCount = qry.count()
        enrollments : List["Lecture_enrollment"] = qry.limit(20).offset(20 * page).all()

        for e in enrollments :
            e.lecture.updatestate()

        enrollments = [e.toDict() for e in enrollments]

        ret = {
            "lecture-count": enrollmentCount, 
            "page": 1, 
            "enrollments": enrollments
        }
        ret.update(CODE_SUCCESS)
        return ret


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

    if request.method == "POST":
        lecture = enrollment.lecture
        
        lecture.updatestate()

        if lecture.state != 1 :
            return CODE_LECTURE_CANT_ENROLLMENT

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

    elif request.method == "DELETE":
        try:
            dataEnrollment.delete()
            db.session.commit()
            return CODE_SUCCESS
        except:
            db.session.rollback()
            return CODE_DATABASE_ERROR


@congyouRouter.route("/wish_remain/", methods=["GET"])
@requireScope(["profile"])
def userWish():
    ret = {"first": getWishRemain(1, g.openid), 
            "second": getWishRemain(2, g.openid)}
    ret.update(CODE_SUCCESS)
    return ret
