from flask import Blueprint

congyouRouter = Blueprint("congyou", __name__)

from . import api as congyou_api
