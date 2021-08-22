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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __str__(self):
        return f'{self.name} {self.id} {self.city}'

db.create_all()

# 如果客户端的cookie还保存但服务器重启了(secret_key)不同，会视为没有登录，但cookie不会自动去除

@app.route('/list/')
def listStu():
    rst = db.session.query(Student).all()
    buf = ''
    for stu in rst:
        buf += str(stu) + '\r\n'
    return buf

def addstu():
    print('sleep')
    time.sleep(5)
    print('add stu out of request...')
    for i in range(20):
        a = Student()
        a.id = i
        a.city = f'city: {i}'
        a.name = f'name: {i}'
        db.session.add(a)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=1, threaded=4)
    threading.Thread(target=addstu).start()

