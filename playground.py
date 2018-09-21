import os

from datetime import datetime
from flask import Flask, request
from flask_dynamo import Dynamo

from models import Log

def create_app():
    app = Flask(__name__)

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

        log = Log(name, request.remote_addr, datetime.now())
        log.save()

        return 'wrote! your name is %s.' % name

    @app.route('/dynamo/read')
    @app.route('/dynamo/read/<name>')
    def read_table(event=None, context=None, name=None):
        if name is None:
            name = '名無しさん'

        log = Log.get(name)

        return str(log)
    return app

# この app という変数が zappa_setting.json の app_function で指定したもの
app = create_app()
