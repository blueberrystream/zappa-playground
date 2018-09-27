from flask import Blueprint
logs_blueprint = Blueprint('logs', __name__, url_prefix='/logs')

from . import routes
