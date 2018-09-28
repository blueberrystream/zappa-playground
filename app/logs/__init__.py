from flask import Blueprint
logs_blueprint = Blueprint('logs', __name__)

from . import routes
