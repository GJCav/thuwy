from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.from_object(config['dev'])

db = SQLAlchemy(app)
from .models import Student

from .router import router
app.register_blueprint(router)

