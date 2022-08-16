from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import Model
import config
from config import MACHINE_ID
from .snowflake import Snowflake
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)

socketio_app = SocketIO(app)

CORS(app,
    origins=config.CORS_ORIGINS,
    expose_headers=config.CORS_EXPOSE_HEADERS,
    supports_credentials=True
)

cfg = config.config
app.config.from_object(cfg)
cfg.set(app)

rsvIdPool = Snowflake(MACHINE_ID)
itemIdPool = Snowflake(MACHINE_ID)
accessKeyPool = Snowflake(MACHINE_ID)
adviceIdPool = Snowflake(MACHINE_ID)
carouselIdPool = Snowflake(MACHINE_ID)

from . import models as Models
Models.init_db(app)

from .auth import authRouter
from .item import itemRouter
from .reservation import rsvRouter
from .advice import adviceRouter
from .carousel import carouselRouter
from .congyou import congyouRouter
from .issue import issueRouter
from . import minio

app.register_blueprint(authRouter)
app.register_blueprint(itemRouter)
app.register_blueprint(rsvRouter)
app.register_blueprint(adviceRouter)
app.register_blueprint(carouselRouter)
app.register_blueprint(congyouRouter)
app.register_blueprint(issueRouter)
app.register_blueprint(minio.router)

with app.app_context():
    Models.db.create_all()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
from . import jobs

migrate = Migrate(app, Models.db)
