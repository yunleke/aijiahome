# coding=utf-8
from . import api_flask
from ihome import db

@api_flask.route("/index")
def index():
    return "hahah"
