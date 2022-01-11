from flask import Blueprint

rsvRouter = Blueprint('reservation', __name__)

from . import api
