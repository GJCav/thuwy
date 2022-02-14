from . import congyouRouter
from app.comerrs import *
from app.auth import requireScope

SAMPLE_LECTURE = {
    "lecture_id" : 123
    "user_id" : 456
    "title" : "Title"
    "theme" : "asd"
    "state" : 1
    "visible" : 1
    "total" : 789
    "first" : 12
    "second" : 34
    "third" : 56
    "subject" : "qwe"
    "teacher" : "fgh"
    "brief_intro" : "jkl"
    "detail_intro" : None
    "deadline" : 

}

@congyouRouter.route("/lecture/", methods = ["GET"])
@requireScope(["profile"])
def lecturelist() :
