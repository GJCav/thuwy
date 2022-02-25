from email.policy import default
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
wish_total = [0, 1, 2, oo, oo]

class Lecture(db.Model):
    __tablename__ = "lecture"
    lecture_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(WECHAT_OPENID)
    position = db.Column(VARCHAR(50))
    title = db.Column(VARCHAR(50))
    theme = db.Column(VARCHAR(50))
    drawn = db.Column(INTEGER, default = 0)
    visible = db.Column(INTEGER)
    total = db.Column(INTEGER)
    subject = db.Column(VARCHAR(50))
    teacher = db.Column(VARCHAR(50))
    brief_intro = db.Column(VARCHAR(255))
    detail_intro = db.Column(JSON)
    publish_time = db.Column(BIGINT, default = lambda: Timetools.now())
    deadline = db.Column(BIGINT)
    holding_time = db.Column(BIGINT)

    lecture_enrollment: List["Lecture_enrollment"] = relationship(
        "Lecture_enrollment", back_populates="lecture"
    )

    def toDict(self) -> Dict:
        return {
            "lecture_id": self.lecture_id,
            "user_id": self.user_id,
            "position" : self.position, 
            "title": self.title,
            "theme": self.theme,
            "state": self.getstate(),
            "visible": self.visible,
            "total": self.total,
            "first": getLectureWishCount(1, self.lecture_id),
            "second": getLectureWishCount(2, self.lecture_id),
            "third": getLectureWishCount(3, self.lecture_id),
            "subject": self.subject,
            "teacher": self.teacher,
            "brief_intro": self.brief_intro,
            "detail_intro": self.detail_intro,
            "publish_time" : self.publish_time, 
            "deadline": self.deadline,
            "holding_time": self.holding_time,
        }

    def toDictNoDetail(self) -> Dict:
        return {
            "lecture_id": self.lecture_id,
            "user_id": self.user_id,
            "position" : self.position, 
            "title": self.title,
            "theme": self.theme,
            "state": self.getstate(),
            "visible": self.visible,
            "total": self.total,
            "first": getLectureWishCount(1, self.lecture_id),
            "second": getLectureWishCount(2, self.lecture_id),
            "third": getLectureWishCount(3, self.lecture_id),
            "subject": self.subject,
            "teacher": self.teacher,
            "brief_intro": self.brief_intro,
            "publish_time" : self.publish_time, 
            "deadline": self.deadline,
            "holding_time": self.holding_time,
        }

    # 更新状态
    def getstate(self) :
        if self.drawn == 0 :
            if Timetools.now() >= self.deadline :
                return 2
            else :
                return 1
        else : 
            if Timetools.now() >= self.holding_time :
                return 4
            else :
                return 3
    
    # 抽签
    def updatedraw(self) :
        self.drawn = 1

        random.shuffle(self.lecture_enrollment)
        self.lecture_enrollment.sort(key = takeWish)

        for i in range(self.total, len(self.lecture_enrollment)) :
            if self.lecture_enrollment[i].delete :
                break
            e = self.lecture_enrollment[i]
            e.lottery = 0

        db.session.commit()


class Lecture_enrollment(db.Model):
    __tablename__ = "lecture_enrollment"
    enrollment_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    lecture_id = db.Column(INTEGER, ForeignKey("lecture.lecture_id"))
    user_id = db.Column(WECHAT_OPENID)
    wish = db.Column(INTEGER)
    lottery = db.Column(INTEGER, default = 1) # 初始值设为1，在之后计算志愿时更容易
    delete = db.Column(INTEGER, default = 0)
    enrollment_time = db.Column(BIGINT, default = lambda: Timetools.now())

    lecture: Lecture = relationship("Lecture", back_populates="lecture_enrollment")

    def toDict(self) -> dict :
        return {
            "enrollment_id" : self.enrollment_id, 
            "lecture_id" : self.lecture_id, 
            "user_id" : self.user_id, 
            "wish" : self.wish, 
            "state" : self.getstate(), 
            "enrollment_time" : self.enrollment_time, 
            "lecture" : self.lecture.toDictNoDetail()
        }
    
    def getstate(self) :
        if self.delete == 1 :
            return 4
        elif self.lecture.drawn == 0 :
            return 1
        return self.lottery + 2

def takeWish(enrollment : Lecture_enrollment) :
    return enrollment.delete * 10 + enrollment.wish

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
            Lecture_enrollment.enrollment_time >= firstDayOfMonth(), 
            Lecture_enrollment.lottery == 1
        )
        .scalar()
    )
    return int(a)

def getWishRemain(wish : int, user_id) -> int :
    return wish_total[wish] - getUserWishCount(wish, user_id)