from operator import and_
from flask import Flask, request, redirect, session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
import os
import json as Json
import requests
from pprint import pprint
import sqlalchemy
import threading
import time
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = os.urandom(24)

scheduler = APScheduler()
app.config["SCHEDULER_API_ENABLED"] = False
scheduler.init_app(app)
scheduler.start()  # 如果是多进程模型，要用文件锁避免同事创建多个scheduler

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __str__(self):
        return f"{self.name} {self.id} {self.city}"


db.create_all()

# 如果客户端的cookie还保存但服务器重启了(secret_key)不同，会视为没有登录，但cookie不会自动去除


@app.route("/list/")
def listStu():
    rst = db.session.query(Student).all()
    buf = ""
    for stu in rst:
        buf += str(stu) + "\r\n"
    return buf


count = 0


@scheduler.task("cron", minute="*")
def addstu():
    print("schedule task")
    with app.app_context():
        global count
        s = Student()
        s.id = count
        s.name = f"name {count}"
        s.city = f"city {count}"
        count += 1
        db.session.add(s)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=1, threaded=4)
