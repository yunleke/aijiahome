# coding:utf-8

from flask import Flask
from config import config_dict
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
db = SQLAlchemy()
# 创建一个redis链接
redis_flask = None
# 创建一个csrf对象,开启csrf防范机制
csrf_flask = CSRFProtect()

# 工厂模式

def create_app(config_name):

    app = Flask(__name__)
    config_name = config_dict[config_name]
    app.config.from_object(config_name)

    # 初始化数据库
    db.init_app(app)
    global redis_flask
    redis_flask = redis.StrictRedis(host=config_name.redis_host, port=config_name.redis_port)
    # 初始化csrf
    csrf_flask.init_app(app)
    Session(app)
    import api_1_0
    # 注册蓝图
    app.register_blueprint(api_1_0.api_flask,url_prefix ="/api/v1_0")
    return app