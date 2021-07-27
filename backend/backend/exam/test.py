from flask import Flask, request, redirect, session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json as Json

import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __str__(self):
        return f'{self.name} {self.id} {self.city}'



@app.route('/')
def hello():
    return 'hello, world. DEBUG mode'

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
        s.city = {'dict': {'arr': [1, 2, 3]}}
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

if __name__ == '__main__':
    app.run(debug=1)