from flask import Blueprint

carouselRouter = Blueprint('carousel', __name__)

from . import carousel_api