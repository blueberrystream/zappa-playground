from datetime import datetime
from flask import request
from flask_restplus import Api, Resource, fields, inputs

from . import logs_blueprint
from app.models import Log as Log


api = Api(
        logs_blueprint,
        version='1.0',
        title='Logs API',
        description='A simple Logs API',
        doc='/doc/'
)

log_def = api.model('Log', {
    'name': fields.String(required=True, description="The user's name"),
    'ip_address': fields.String(description="The user's IP address"),
    'timestamp': fields.DateTime(description="Logged timestamp"),
})
listed_log_def = api.model('ListedLog', {
    'name': fields.String(description="The user's name")
})


@api.route('/<string:name>')
@api.doc(responses={404: "The user's log is not found"}, params={'name': "The user's name"})
class LogResource(Resource):
    @api.doc(description="Get the user's log")
    @api.marshal_with(log_def)
    def get(self, name):
        try:
            return Log.get(name)
        except Log.DoesNotExist:
            api.abort(404, "{}'s log does not exist".format(name))

    @api.doc(description="Put the user's log")
    @api.expect(log_def, validate=True)
    @api.marshal_with(log_def)
    def put(self, name):
        parser = api.parser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('ip_address', type=inputs.ipv4)
        parser.add_argument('timestamp', type=inputs.datetime_from_iso8601)

        args = parser.parse_args()
        ip_address = request.remote_addr if args['ip_address'] is None else args['ip_address']
        timestamp = datetime.now() if args['timestamp'] is None else args['timestamp']

        log = Log(name, ip_address=ip_address, timestamp=timestamp)
        log.save()

        return log


@api.route('/')
class LogListResource(Resource):
    @api.marshal_list_with(listed_log_def)
    def get(self):
        logs = Log.scan()

        return [{'name': log.name} for log in logs]
