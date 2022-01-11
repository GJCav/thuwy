from flask import Blueprint

authRouter = Blueprint('auth', __name__)
from . import api
from .api import requireLogin, requireBinding, requireAdmin