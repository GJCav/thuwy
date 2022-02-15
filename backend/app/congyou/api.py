from urllib import request
from . import congyouRouter
from app.comerrs import *

from app.auth import requireScope, challengeScope
from flask import g

SAMPLE_LECTURE = {
    "lecture_id" : 123, 
    "user_id" : 456, 
    "title" : "Title", 
    "theme" : "asd", 
    "state" : 1, 
    "visible" : 1, 
    "total" : 789, 
    "first" : 12, 
    "second" : 34, 
    "third" : 56, 
    "subject" : "qwe", 
    "teacher" : "fgh", 
    "brief_intro" : "jkl", 
    "detail_intro" : None, 
    "deadline" : 202202152359
}

SAMPLE_ENROLLMENT = {
    "enrollment_id" : 987, 
    "lecture_id" : 123, 
    "user_id" : 765, 
    "wish" : 1, 
    "state" : 2, 
    "lecture" : SAMPLE_LECTURE
}

@congyouRouter.route("/lecture/", methods = ["GET", "POST"])
@requireScope(["profile", "congyou profile"])
def lecturelist() :
    if request.method == "GET" and challengeScope(["profile"]):
        ret = {"lecture-count" : 1,
                "page" : 1, 
                "lectures" : [SAMPLE_LECTURE]}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "POST" and challengeScope(["profile congyou"]):
        reqJson = request.json
        ret = {"Lecture-id" : 1000}
        ret.update(CODE_SUCCESS)
        return ret

@congyouRouter.route("/lecture/<int:id>/", methods = ["GET", "POST"])
@requireScope(["profile", "profile congyou"])
def lecturelist(id : int) :
    if request.method == "GET" and challengeScope(["profile"]):
        ret = {"lecture" : [SAMPLE_LECTURE]}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "POST" and challengeScope(["profile congyou"]):
        reqJson = request.json
    ret = {}
    ret.update(CODE_SUCCESS)
    return ret

@congyouRouter.route("/lecture_enrollment/", methods = ["GET", "POST"])
@requireScope(["profile"])
def lecturelist() :
    if request.method == "POST" : 
        reqJson = request.json
        ret = {"enrollment_id" : 135}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "GET" : 
        ret = {"lecture-count" : 1, 
            "page" : 1, 
            "enrollments" : SAMPLE_ENROLLMENT}
        ret.update(CODE_SUCCESS)
        return ret

@congyouRouter.route("/lecture_enrollment/<int : id>/", methods = ["POST", "DELETE"])
@requireScope(["profile"])
def lecturelist(id : int) :
    if request.method == "POST" : 
        reqJson = request.json
        ret = {}
        ret.update(CODE_SUCCESS)
        return ret
    elif request.method == "DELETE" : 
        ret = {}
        ret.update(CODE_SUCCESS)
        return ret

@congyouRouter.route("/wish_remain/", methods = ["GET"])
@requireScope(["profile"])
def lecturelist(id : int) :
    ret = {"first" : 1, 
            "second" : 2}
    ret.update(CODE_SUCCESS)
    return ret