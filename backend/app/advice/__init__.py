from flask import Blueprint

adviceRouter = Blueprint('advice', __name__)

from . import adviceapi