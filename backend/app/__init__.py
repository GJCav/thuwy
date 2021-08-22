from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from config import MACHINE_ID
from .snowflake import Snowflake

app = Flask(__name__)

cfg = config.config
app.config.from_object(cfg)
cfg.set(app)

db = SQLAlchemy(app, use_native_unicode='utf8')
from .models import Admin, User, Item, Reservation
db.create_all()

rsvIdPool      = Snowflake(MACHINE_ID)
itemIdPool     = Snowflake(MACHINE_ID)
adminReqIdPool = Snowflake(MACHINE_ID)
accessKeyPool  = Snowflake(MACHINE_ID)


from .auth import authRouter
from .item import itemRouter
from .reservation import rsvRouter
app.register_blueprint(authRouter)
app.register_blueprint(itemRouter)
app.register_blueprint(rsvRouter)