from flask import Blueprint

issueRouter = Blueprint("issue", __name__)

from . import api as issue_api
