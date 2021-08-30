from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import config
from config import MACHINE_ID
from .snowflake import Snowflake

app = Flask(__name__)

cfg = config.config
app.config.from_object(cfg)
cfg.set(app)

db = SQLAlchemy(app, use_native_unicode='utf8')
from . import models as Models
db.create_all()
Models.init_db()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
from . import jobs

rsvIdPool      = Snowflake(MACHINE_ID)
itemIdPool     = Snowflake(MACHINE_ID)
adminReqIdPool = Snowflake(MACHINE_ID)
accessKeyPool  = Snowflake(MACHINE_ID)
adviceIdPool   = Snowflake(MACHINE_ID)


from .auth import authRouter
from .item import itemRouter
from .reservation import rsvRouter
from .advice import adviceRouter
app.register_blueprint(authRouter)
app.register_blueprint(itemRouter)
app.register_blueprint(rsvRouter)
app.register_blueprint(adviceRouter)