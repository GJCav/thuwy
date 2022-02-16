from flask import request
from flask import g

from app.comerrs import *
from app.auth import requireScope, challengeScope
import app.checkargs as CheckArgs

from .model import db, Lecture, Lecture_enrollment
from . import congyouRouter
from .errcode import *

SAMPLE_LECTURE = {
    "lecture_id": 123,
    "user_id": 456,
    "title": "Title",
    "theme": "asd",
    "state": 1,
    "visible": 1,
    "total": 789,
    "first": 12,
    "second": 34,
    "third": 56,
    "subject": "qwe",
    "teacher": "fgh",
    "brief_intro": "jkl",
    "detail_intro": None,
    "deadline": 202202152359,
}

SAMPLE_ENROLLMENT = {
    "enrollment_id": 987,
    "lecture_id": 123,
    "user_id": 765,
    "wish": 1,
    "state": 2,
    "lecture": SAMPLE_LECTURE,
}


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
        lectures = [e.toDictNoDetail() for e in lectures]

        ret = {"lecture-count": lectureCount, "page": page, "lectures": lectures}
        ret.update(CODE_SUCCESS)
        return ret

    elif request.method == "POST" and challengeScope(["profile congyou"]):
        reqJson = request.json
        if reqJson == None:
            return CODE_ARG_INVALID
        if not CheckArgs.hasAttrs(
            reqJson,
            [
                "title",
                "theme",
                "total",
                "subject",
                "teacher",
                "brief-intro",
                "detail-intro",
                "deadline",
                "holding_time",
            ],
        ):
            return CODE_ARG_MISSING
        if (
            (
                not CheckArgs.areStr(
                    reqJson, ["title", "theme", "subject", "teacher", "brief-intro"]
                )
            )
            or (not CheckArgs.areInt(reqJson, ["total"]))
            or (not CheckArgs.areUint64(reqJson, ["deadline", "holding_time"]))
        ):
            return CODE_ARG_TYPE_ERR

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


@congyouRouter.route("/lecture_enrollment/", methods=["GET", "POST"])
@requireScope(["profile"])
def lectureEnrollmentList():
    if request.method == "POST":  ######################################## TODO
        """
        reqJson = request.json
        if reqJson == None :
            return CODE_ARG_INVALID
        if(not reqJson.get("Lecture_enrollment")) :
        """
        ret = {"enrollment_id": 135}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "GET":  ######################################## TODO
        ret = {"lecture-count": 1, "page": 1, "enrollments": SAMPLE_ENROLLMENT}
        ret.update(CODE_SUCCESS)
        return ret


@congyouRouter.route("/lecture_enrollment/<int:id>/", methods=["POST", "DELETE"])
@requireScope(["profile"])
def lectureEnrollmentModify(id: int):
    if request.method == "POST":  ######################################## TODO
        reqJson = request.json
        ret = {}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "DELETE":  ######################################## TODO
        ret = {}
        ret.update(CODE_SUCCESS)
        return ret


@congyouRouter.route("/wish_remain/", methods=["GET"])
@requireScope(["profile"])
def userWish(id: int):  ######################################## TODO
    ret = {"first": 1, "second": 2}
    ret.update(CODE_SUCCESS)
    return ret
