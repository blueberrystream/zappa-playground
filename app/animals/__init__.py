from flask import Blueprint
animals_blueprint = Blueprint('animals', __name__, url_prefix='/animals')

from . import routes
