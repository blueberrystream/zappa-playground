from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(event=None, context=None):
    return 'hello from Flask!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=29713)
