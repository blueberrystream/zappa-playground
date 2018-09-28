import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    register_blueprints(app)
    register_home_routing(app)

    return app


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.logs import logs_blueprint

    app.register_blueprint(logs_blueprint)


def register_home_routing(app):
    @app.route('/home')
    def home_index(event=None, context=None):
        stage = os.environ.get('STAGE')
        return 'hello from Flask! this stage is %s.' % stage


# for zappa
app = create_app()
