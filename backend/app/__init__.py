from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config, MACHINE_ID
from .snowflake import Snowflake

app = Flask(__name__)
app.config.from_object(config['dev'])

db = SQLAlchemy(app)
from .models import Admin, User, Item, Reservation
db.create_all()

rsvIdPool = Snowflake(MACHINE_ID)

from .router import router
app.register_blueprint(router)
