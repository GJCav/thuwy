from itertools import count
from select import select
from typing import Any, Dict, List

from app.models import db

from sqlalchemy import BIGINT, INTEGER, TEXT, VARCHAR, JSON, ForeignKey, func
from app.models import WECHAT_OPENID, SNOWFLAKE_ID
from sqlalchemy.orm import relationship

first_total = 1
second_total = 2


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
        # TODO 
        #计算并判断当前应该是什么状态
        # pre_state = self.state
        # self.state = now_state
        # db.session.commit()
        return 
    
    # 抽签
    def updatedraw(self) :
        # TODO
        #计算并判断是否需要抽签
        #抽签
        #更改Lecture_enrollment的状态
        # db.sessiong.commit()
        return 


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

def getUserWishCount(wish: int, user_id: int) -> int:
    a = (
        db.session.query(func.count("*"))
        .select_from(Lecture_enrollment)
        .filter(
            Lecture_enrollment.user_id == int(user_id),
            Lecture_enrollment.wish == int(wish),
            # Lecture_enrollment.enrollment_time >= firstDayOfMonth() # TODO 判断一下报名时间在本月1日之后
        )
        .scalar()
    )
    return int(a)
