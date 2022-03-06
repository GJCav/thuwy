from flask import Blueprint

notiRouter = Blueprint("notification", __name__)

from . import api
