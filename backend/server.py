import eventlet
from eventlet import wsgi
eventlet.monkey_patch()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER
import datetime

from sqlalchemy import Column

app = Flask("test server")

UNIX_USERNAME = "zyx"
DB_UNIX_SOCK = r"/run/mysqld/mysqld.sock"

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SCHEDULER_TIMEZONE = "Asia/Shanghai"

    def set(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://%s@/thuwy_zyx?unix_socket=%s&charset=utf8mb4"
        % (UNIX_USERNAME, DB_UNIX_SOCK)
    )

    def set(app):
        app.secret_key = "dev ----"
    
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

class Model(db.Model):
    id = Column(INTEGER, primary_key=True)
    num = Column(INTEGER, default=0)

db.create_all()

@app.route('/')
def hello():
    return 'hello'

@app.route('/create')
def create():
    m = Model()
    db.session.add(m)
    db.session.commit()
    return {'id': m.id}

@app.route('/add/<id>')
def add(id):
    id = int(id)
    m = (
        db.session.query(Model)
        .filter(Model.id == id)
        .with_for_update() # 这句话非常关键，保证了多线程并发下数据的正确性，可以注释掉然后运行test.py查看效果
        .one_or_none()
    )
    
    m.num += 1
    db.session.commit()
    return {"id": m.id, "num": m.num}

@app.route('/qry/<id>')
def qry(id):
    m = (
        db.session.query(Model)
        .filter(Model.id == id)
        .one_or_none()
    )
    return {"id": m.id, "num": m.num}


if __name__ == '__main__':
    wsgi.server(eventlet.listen(('', 5000)), app)
    app.run('0.0.0.0', 5000)