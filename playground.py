import os

from datetime import datetime
from flask import Flask, request, jsonify
from flask_dynamo import Dynamo

def create_app():
    app = Flask(__name__)
    app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='zappa-playground-logs',
            KeySchema=[dict(AttributeName='name', KeyType='HASH')],
            ProvisionedThroughput=dict(ReadCapacityUnits=1, WriteCapacityUnits=1)
        )
    ]
    app.config['JSON_AS_ASCII'] = False

    dynamo = Dynamo(app)

    @app.route('/')
    def index(event=None, context=None):
        app.logger.info('Lambda function invoked index()')
        stage = os.environ.get('STAGE')
        return 'hello from Flask! this stage is %s.' % stage

    # アプリを実行するIAM Roleｎ権限上、テーブル作成ができない
    # @app.route('/dynamo/create')
    # def create_table(event=None, context=None):
    #     with app.app_context():
    #         dynamo.create_all()
    #     return 'table is created!'

    @app.route('/dynamo/write')
    @app.route('/dynamo/write/<name>')
    def write_table(event=None, context=None, name=None):
        if name is None:
            name = '名無しさん'

        dynamo.tables['zappa-playground-logs'].put_item(Item={
            'name': name,
            'ip_address': request.remote_addr,
            'timestamp': datetime.now().strftime('%c')
        })

        return 'wrote! your name is %s.' % name

    @app.route('/dynamo/read')
    @app.route('/dynamo/read/<name>')
    def read_table(event=None, context=None, name=None):
        if name is None:
            name = '名無しさん'

        response = dynamo.tables['zappa-playground-logs'].get_item(Key={
            'name': name
        })
        item = response['Item']

        return jsonify(item)
    return app

# この app という変数が zappa_setting.json の app_function で指定したもの
app = create_app()
