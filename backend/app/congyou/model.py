from typing import List
from app.models import db

from sqlalchemy import BIGINT, INTEGER, TEXT, VARCHAR, JSON, ForeignKey
from app.models import WECHAT_OPENID, SNOWFLAKE_ID
from sqlalchemy.orm import relationship

class Lecture(db.Model):
    __tablename__ = "lecture"
    lecture_id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(SNOWFLAKE_ID)
    title = db.Column(VARCHAR(50))
    theme = db.Column(VARCHAR(50))
    state = db.Column(INTEGER)
    visible = db.Column(INTEGER)
    total = db.Column(INTEGER)
    subject = db.Column(VARCHAR(50))
    teacher = db.Column(VARCHAR(50))
    brief_intro = db.Column(VARCHAR(255))
    detail_intro = db.Column(JSON)
    start_time = db.Column(BIGINT)
    deadline = db.Column(BIGINT)
    holding_time = db.Column(BIGINT)

    lecture_enrollment : List["Lecture_enrollment"] = relationship("Lecture_enrollment", back_populates = "lecture")
    # TODO first second third

class Lecture_enrollment(db.Model):
    __tablename__ = "lecture_enrollment"
    enrollment_id = db.Column(INTEGER, primary_key = True)
    lecture_id = db.Column(INTEGER, ForeignKey("lecture.lecture_id"))
    user_id = db.Column(SNOWFLAKE_ID)
    wish = db.Column(INTEGER)
    state = db.Column(INTEGER)
    delete = db.Column(INTEGER)

    lecture: Lecture = relationship("Lecture", back_populates="lecture_enrollment")



