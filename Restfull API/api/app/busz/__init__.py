from flask import Blueprint

busz = Blueprint('busz', __name__)

from . import views