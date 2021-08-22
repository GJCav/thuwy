from flask import Blueprint

authRouter = Blueprint('auth', __name__)
from . import authapi
from .authapi import requireLogin, requireBinding, requireAdmin