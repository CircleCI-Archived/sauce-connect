"""hello_app"""
from flask import Flask
APP = Flask(__name__)


@APP.route('/')
def hello():
    """hello"""
    return 'Hello World, I love continuous delivery!'


if __name__ == '__main__':
    APP.run()
