from flask import Blueprint

authRouter = Blueprint('auth', __name__)
from . import auth_api
from .auth_api import requireLogin, requireBinding, requireAdmin