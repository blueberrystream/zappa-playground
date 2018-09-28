from datetime import datetime
from flask import request
from flask_restplus import Api, Resource, fields

from . import logs_blueprint
from app.models import Log as LogModel


api = Api(
        logs_blueprint,
        version='1.0',
        title='Logs API',
        description='A simple Logs API',
        doc='/doc/logs/',
        default='logs'
)
ns = api.namespace('logs')

log_def = api.model('Log', {
    'name': fields.String(required=True, description="The user's name"),
    'ip_address': fields.String(description="The user's IP address"),
    'timestamp': fields.DateTime(dt_format='rfc822', description="Logged timestamp"),
})
listed_log_def = api.model('ListedLog', {
    'name': fields.String(description="The user's name")
})

parser = api.parser()


@ns.route('/<string:name>')
@api.doc(responses={404: "The user's log is not found"}, params={'name': "The user's name"})
class Log(Resource):
    @api.doc(description="Get the user's log")
    @api.marshal_with(log_def)
    def get(self, name):
        try:
            return LogModel.get(name)
        except LogModel.DoesNotExist:
            api.abort(404, "{}'s log does not exist".format(name))

    @api.doc(description="Put the user's log")
    @api.expect(log_def)
    @api.marshal_with(log_def)
    def put(self, name):
        args = parser.parse_args()
        log = LogModel(args['name'], ip_address=request.remote_addr, timestamp=datetime.now())
        log.save()

        return log


@ns.route('/')
class TodoList(Resource):
    @api.marshal_list_with(listed_log_def)
    def get(self):
        logs = LogModel.scan()

        return [{'name': log.name} for log in logs]
