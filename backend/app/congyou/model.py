from itertools import count
from select import select
from typing import Any, Dict, List

from app.models import db

from sqlalchemy import BIGINT, INTEGER, TEXT, VARCHAR, JSON, ForeignKey, func
from app.models import WECHAT_OPENID, SNOWFLAKE_ID
from sqlalchemy.orm import relationship

import time
import datetime
import app.timetools as Timetools

import random

oo = 1000000000
wish_total = [0, 1, 2, oo]

class Lecture(db.Model):
    __tablename__ = "lecture"
    lecture_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(WECHAT_OPENID)
    title = db.Column(VARCHAR(50))
    theme = db.Column(VARCHAR(50))
    state = db.Column(INTEGER)
    visible = db.Column(INTEGER)
    total = db.Column(INTEGER)
    subject = db.Column(VARCHAR(50))
    teacher = db.Column(VARCHAR(50))
    brief_intro = db.Column(VARCHAR(255))
    detail_intro = db.Column(JSON)
    deadline = db.Column(BIGINT)
    holding_time = db.Column(BIGINT)

    lecture_enrollment: List["Lecture_enrollment"] = relationship(
        "Lecture_enrollment", back_populates="lecture"
    )

    def toDict(self) -> Dict:
        return {
            "lecture_id": self.lecture_id,
            "user_id": self.user_id,
            "title": self.title,
            "theme": self.theme,
            "state": self.state,
            "visible": self.visible,
            "total": self.total,
            "first": getLectureWishCount(1, self.lecture_id),
            "second": getLectureWishCount(2, self.lecture_id),
            "third": getLectureWishCount(3, self.lecture_id),
            "subject": self.subject,
            "teacher": self.teacher,
            "brief_intro": self.brief_intro,
            "detail_intro": self.detail_intro,
            "deadline": self.deadline,
            "holding_time": self.holding_time,
        }

    def toDictNoDetail(self) -> Dict:
        return {
            "lecture_id": self.lecture_id,
            "user_id": self.user_id,
            "title": self.title,
            "theme": self.theme,
            "state": self.state,
            "visible": self.visible,
            "total": self.total,
            "first": getLectureWishCount(1, self.lecture_id),
            "second": getLectureWishCount(2, self.lecture_id),
            "third": getLectureWishCount(3, self.lecture_id),
            "subject": self.subject,
            "teacher": self.teacher,
            "brief_intro": self.brief_intro,
            "deadline": self.deadline,
            "holding_time": self.holding_time,
        }

    # 更新状态
    def updatestate(self) :
        pre_state = self.state
        if pre_state == 1 and Timetools.now() > self.deadline :
            self.state = 2
        elif pre_state == 3 and Timetools.now() > self.holding_time :
            self.state = 4
    
    # 抽签
    def updatedraw(self) :
        self.updatestate()
        if (self.state == 2) :
            self.state = 3

            random.shuffle(self.lecture_enrollment)
            self.lecture_enrollment.sort(key = takeWish)

            for i in range(self.total, len(self.lecture_enrollment)) :
                e = self.lecture_enrollment[i]
                e.state = 3

        db.session.commit()


class Lecture_enrollment(db.Model):
    __tablename__ = "lecture_enrollment"
    enrollment_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    lecture_id = db.Column(INTEGER, ForeignKey("lecture.lecture_id"))
    user_id = db.Column(WECHAT_OPENID)
    wish = db.Column(INTEGER)
    state = db.Column(INTEGER)
    delete = db.Column(INTEGER)
    enrollment_time = db.Column(BIGINT)

    lecture: Lecture = relationship("Lecture", back_populates="lecture_enrollment")

    def toDict(self) -> dict :
        return {
            "enrollment_id" : self.enrollment_id, 
            "lecture_id" : self.lecture_id, 
            "user_id" : self.user_id, 
            "wish" : self.wish, 
            "state" : self.state, 
            "enrollment_time" : self.enrollment_time, 
            "lecture" : self.lecture.toDictNoDetail()
        }

def takeWish(enrollment : Lecture_enrollment) :
    return enrollment.wish

def getLectureWishCount(wish: int, lecture_id: int) -> int:
    a = (
        db.session.query(func.count("*"))
        .select_from(Lecture_enrollment)
        .filter(
            Lecture_enrollment.lecture_id == int(lecture_id),
            Lecture_enrollment.wish == int(wish),
        )
        .scalar()
    )
    return int(a)

def firstDayOfMonth() :
    today = datetime.date.today()
    fd = datetime.datetime(today.year, today.month, 1)
    tp = fd.timetuple()
    stamp = time.mktime(tp)
    return stamp * 1000

def getUserWishCount(wish: int, user_id) -> int:
    a = (
        db.session.query(func.count("*"))
        .select_from(Lecture_enrollment)
        .filter(
            Lecture_enrollment.user_id == user_id,
            Lecture_enrollment.wish == wish,
            Lecture_enrollment.enrollment_time >= firstDayOfMonth()
        )
        .scalar()
    )
    return int(a)

def getWishRemain(wish : int, user_id) -> int :
    return wish_total[wish] - getUserWishCount(wish, user_id)