from pyparsing import java_style_comment
from config4test import R, UseAccount, baseUrl

import sys
sys.path.append("..")

from app.comerrs import *
from app.congyou.errcode import *
import app.checkargs as CheckArgs
import app.timetools as Timetools

import pytest

import math
import random
import string

test_lecture_url = baseUrl + "lecture/"

Subjects = ["qwe", "asd", "zxc", "ert", "fgh"]

class _TestLecture :
    def __init__(self) :
        self.title = "".join(random.sample(string.ascii_letters + string.digits, 8))
        self.theme = "".join(random.sample(string.ascii_letters + string.digits, 8))
        self.position = "".join(random.sample(string.ascii_letters + string.digits, 8))
        self.total = random.randint(1, 100)
        self.subject = Subjects[random.randint(0, 4)]
        self.teacher = "".join(random.sample(string.ascii_letters + string.digits, 8))
        self.brief_intro = "".join(random.sample(string.ascii_letters + string.digits, 8))
        self.detail_intro = {
            "asd" : "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "qwe" : "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "zxc" : "".join(random.sample(string.ascii_letters + string.digits, 8))
        }
        self.deadline = Timetools.hoursAfter(Timetools.daysAfter(2), random.randint(1, 20))
        self.holding_time = Timetools.hoursAfter(Timetools.daysAfter(2, self.deadline), random.randint(1, 20))

    def toDict(self):
        return {
            "title" : self.title, 
            "theme" :self.theme, 
            "position" : self.position, 
            "total" : self.total, 
            "subject" : self.subject, 
            "teacher" : self.teacher, 
            "brief-intro" : self.brief_intro, 
            "detail-intro" : self.detail_intro,
            "deadline" : self.deadline, 
            "holding_time" : self.holding_time
        }
    
    def rand_to_dict(self) :
        ret = {}
        if random.randint(0, 1) == 1 :
            ret.update({"title" : self.title})
        if random.randint(0, 1) == 1 :
            ret.update({"theme" :self.theme})
        if random.randint(0, 1) == 1 :
            ret.update({"position" : self.position})
        if random.randint(0, 1) == 1 :
            ret.update({"total" : self.total})
        if random.randint(0, 1) == 1 :
            ret.update({"subject" : self.subject})
        if random.randint(0, 1) == 1 :
            ret.update({"teacher" : self.teacher})
        if random.randint(0, 1) == 1 :
            ret.update({"brief-intro" : self.brief_intro})
        if random.randint(0, 1) == 1 :
            ret.update({"detail-intro" : self.detail_intro})
        if random.randint(0, 1) == 1 :
            ret.update({"deadline" : self.deadline})
        if random.randint(0, 1) == 1 :
            ret.update({"holding_time" : self.holding_time})
        return ret

def _isLectureObject_noD(lecture : dict) :
    assert {
        "lecture_id", 
        "user_id", 
        "position", 
        "title", 
        "theme", 
        "state", 
        "visible", 
        "total", 
        "first", 
        "second", 
        "third", 
        "subject", 
        "teacher", 
        "brief_intro", 
        "publish_time", 
        "deadline", 
        "holding_time"
    } == lecture.keys()
    assert CheckArgs.areStr(lecture, ["user_id", "position", "title", "theme", "subject", "teacher", "brief_intro"])
    assert CheckArgs.areInt(lecture, ["lecture_id", "state", "visible", "total", "first", "second", "third"])
    assert CheckArgs.areUint64(lecture, ["publish_time", "deadline", "holding_time"])

def _isLectureObject(lecture : dict) :
    assert {
        "lecture_id", 
        "user_id", 
        "position", 
        "title", 
        "theme", 
        "state", 
        "visible", 
        "total", 
        "first", 
        "second", 
        "third", 
        "subject", 
        "teacher", 
        "brief_intro", 
        "detail_intro" ,
        "publish_time", 
        "deadline", 
        "holding_time"
    } == lecture.keys()
    assert CheckArgs.areStr(lecture, ["user_id", "position", "title", "theme", "subject", "teacher", "brief_intro"])
    assert CheckArgs.areInt(lecture, ["lecture_id", "state", "visible", "total", "first", "second", "third"])
    assert CheckArgs.areUint64(lecture, ["publish_time", "deadline", "holding_time"])

def getLecture_page(now_lecture_url, sym) : # 测试获取从游坊列表中填写了page参数
    with UseAccount("normal_user") :
        res = R.get(f"{now_lecture_url}")
        assert res
        json = res.json()
        assert json["code"] == 0

        assert CheckArgs.hasAttrs(json, ["code", "errmsg", "lecture-count", "page", "lectures"])
        assert CheckArgs.areInt(json, ["lecture-count", "page"])
        assert json["page"] == 1

        maxPage = math.ceil(json["lecture-count"] / 20)
        for i in range(maxPage) :
            res = R.get(f"{now_lecture_url}{sym}p={i + 1}")
            json = res.json()
            assert json["code"] == 0
            assert CheckArgs.hasAttrs(json, ["code", "errmsg", "lecture-count", "page", "lectures"])
            assert CheckArgs.areInt(json, ["lecture-count", "page"])
            assert json["page"] == i + 1

            for lecture in json["lectures"] :
                _isLectureObject_noD(lecture)
        
        res = R.get(f"{now_lecture_url}{sym}p={maxPage + 1}")
        assert len(res.json()["lectures"]) == 0

        res = R.get(f"{now_lecture_url}{sym}p=0")
        assert res.json()["code"] == CODE_ARG_INVALID["code"]

def getLecture_state(now_lecture_url, sym) : # 测试获取从游坊列表中填写了state参数
    with UseAccount("normal_user") :
        getLecture_page(now_lecture_url, sym)
        for i in range(4) :
            state = i + 1
            getLecture_page(f"{now_lecture_url}{sym}state={state}", "&")
        getLecture_page(f"{now_lecture_url}{sym}state=0", "&")
        getLecture_page(f"{now_lecture_url}{sym}state=5", "&")
        getLecture_page(f"{now_lecture_url}{sym}state=asd", "&")

def getLecture_subject(now_lecture_url, sym) : # 测试获取从游坊列表中填写了subject参数    
    with UseAccount("normal_user") :
        getLecture_state(now_lecture_url, sym)
        getLecture_page(now_lecture_url, sym)
        for i in Subjects :
            getLecture_state(f"{now_lecture_url}{sym}subject={i}", "&")
        getLecture_state(f"{now_lecture_url}{sym}subject=123", "&")
        
def test_getLecture() : #  获取从游坊列表
    with UseAccount("normal_user") :
        getLecture_subject(test_lecture_url, "?")
        
    res = R.get(f"{test_lecture_url}")
    assert res
    assert res.json()["code"] == 8

def test_getLectureDetail() : # 获取从游坊详细信息
    with UseAccount("normal_user") :
        res = R.get(f"{test_lecture_url}")
        maxPage = math.ceil(res.json()["lecture-count"] / 20)
        print(res.json()["lecture-count"])
    for i in range(maxPage) :
        page = i + 1
        print(page)
        with UseAccount("normal_user") :
            Res = R.get(f"{test_lecture_url}?p={page}")
        _Json = Res.json()
        for lecture in _Json["lectures"] :
            lecture_id = lecture["lecture_id"]
            now_lecture_url = test_lecture_url + f"{lecture_id}/"
            with UseAccount("normal_user") :
                rres = R.get(f"{now_lecture_url}")
                assert rres
                assert rres.json()["code"] == 0
                _isLectureObject(rres.json()["lecture"])

            rres = R.get(f"{now_lecture_url}")
            assert rres
            assert rres.json()["code"] == 8
        with UseAccount("normal_user") :
            res = R.get(f"{test_lecture_url}123456789/")
            assert res
            assert res.json()["code"] == 101

addLectureCount = 10
def test_addLecture() : # 测试添加从游坊
    with UseAccount("cyuserB") :
        for i in range(addLectureCount) :
            lecture = _TestLecture()
            res = R.post(test_lecture_url, json = lecture.toDict())
            json = res.json()
            assert json["code"] == 0
            assert CheckArgs.hasAttrs(json, ["Lecture-id"])
            assert CheckArgs.isInt(json["Lecture-id"])

    with UseAccount("normal_user") :
        res = R.post(test_lecture_url, json = lecture.toDict())
        print(res)
        assert res.json()["code"] == 8
        
def test_modLecture() : # 测试修改从游坊
    with UseAccount("cyuserB") :
        lecture = _TestLecture()
        asd = lecture.rand_to_dict()
        # print(asd)
        res = R.post(test_lecture_url + "69/", json = asd)
        assert res.json()["code"] == 104

        lecture = _TestLecture()
        asd = lecture.rand_to_dict()
        print(asd)
        res = R.post(test_lecture_url + "70/", json = asd)
        assert res.json()["code"] == 0

        lecture = _TestLecture()
        asd = lecture.rand_to_dict()
        print(asd)
        res = R.post(test_lecture_url + "3/", json = asd)
        assert res.json()["code"] == 0