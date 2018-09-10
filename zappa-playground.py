import logging
from flask import Flask

app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index(event=None, context=None):
    logger.info('Lambda function invoked index()')
    return 'hello from Flask!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=29713)
