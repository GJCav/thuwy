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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column('i--d', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __str__(self):
        return f'{self.name} {self.id} {self.city}'

class Item(db.Model):
    __tablename__ = "items"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.Text)
    available     = db.Column(db.Integer)
    delete        = db.Column(db.Integer)
    rsvMethod     = db.Column('rsv_method', db.Integer, nullable=False)
    briefIntro    = db.Column('brief_intro', db.Text)
    thumbnail     = db.Column(db.Text)
    mdIntro       = db.Column('md_intro', db.Text)

    def toDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'available': bool(self.available),
            'brief-intro': self.briefIntro,
            'thumbnail': self.thumbnail,
            'rsv-method': self.rsvMethod
        }

    # no value check on dic
    def fromDict(self, dic):
        self.name = dic['name']
        self.id = dic['id']
        self.briefIntro = dic['brief-intro']
        self.thumbnail = dic['thumbnail']
        self.rsvMethod = dic['rsv-method']

    def __repr__(self) -> str:
        return f'Item({self.name}, {self.briefIntro}, {self.id}, {self.mdIntro if len(self.mdIntro) < 30 else (self.mdIntro[:27]+"...")})'

class Num(db.Model):
    a = db.Column(db.Integer, primary_key = True)

    def __init__(self, a) -> None:
        self.a = a

db.create_all()

@app.route('/')
def hello():
    # db.session.add(Num(1))
    # db.session.add(Num(2))
    # db.session.add(Num(3))
    # db.session.add(Num(4))
    # db.session.add(Num(5))
    # db.session.add(Num(6))
    # db.session.add(Num(7))
    db.session.commit()

    arr = db.session.query(Num.a).filter(*{
        or_(
            # 1 <= Num.a <= 3,
            # 6 <= Num.a <= 10

            and_(Num.a >= 1, Num.a <= 3),
            and_(Num.a >= 6, Num.a <= 10)
        )
    }).all()

    arr = [dict(e) for e in arr]

    return {'arr': arr}

@app.route('/showall/')
def showall():
    s = ''
    # for stu in Student.query.all():
    #     stu: Student
    #     s += str(stu) + '<br/>'
    for t in Student.query.all():
        s += str(t) + '<br/>'
        print(t)
    return s

@app.route('/addpage/')
def addstupage():
    return render_template('addstu.html')

@app.route('/add/', methods=['POST', 'GET'])
def addstu():
    if request.method == 'POST':
        s = Student()
        s.name = request.form['name']
        s.id = request.form['id']
        s.city = request.form['city']
    else:
        s = Student()
        s.name = None
        s.id = '122102'
        s.city = Json.dumps({'dict': {'arr': [1, 2, 3]}})

    
    db.session.add(s)
    db.session.commit()
    return redirect('/showall/')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        session['user'] = request.form['user']
        return redirect('/testlogin/')

@app.route('/logout/')
def logout():
    if session.get('user'):
        session.pop('user')
        return 'logout.'
    else:
        return 'you havent loggin'

# 如果客户端的cookie还保存但服务器重启了(secret_key)不同，会视为没有登录，但cookie不会自动去除
@app.route('/testlogin/')
def testlogin():
    if session.get('user'):
        return f'You have logged in. {session["user"]}'
    else:
        return 'You haven\tt logged in.'


@app.route('/foo')
def foo():
    r = db.session.query(Num).filter(Num.a.op('&')(2)).all()
    pprint(r)
    return 'yes'

if __name__ == '__main__':
    app.run(debug=1)