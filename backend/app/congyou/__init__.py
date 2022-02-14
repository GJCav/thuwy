from flask import Blueprint

itemRouter = Blueprint("congyou", __name__)

from . import api as item_api
