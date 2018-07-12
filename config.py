# coding:utf-8
import redis
class Config(object):
    SECRET_KEY = "lsidjfoiupojsajdoisahfow"
    # 工程的配置信息

    # 配置数据库的信息
    SQLALCHEMT_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flask_aijia"
    # 跟踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 配置redis
    redis_host = "127.0.0.1"
    redis_port = 6379
    # session的配置信息
    SESSION_TYPE = "redis" # 把session存储在redis里面
    SESSION_USE_SINGLE = True # 把cookie中的session_id进行加密
    SESSION_REDIS = redis.StrictRedis(host=redis_host,port=redis_port)
    PERMENANT_SESSION_LIFETIME = 86400 # 设置session的过期时间,以秒为单位
class DevelopmentConfig(Config):
    # 开发模式
    DEBUG = True
class ProductionConfig(Config):
    # 线上模式
    pass
config_dict = {
    "DevelopmentConfig":DevelopmentConfig,
    "ProductionConfig":ProductionConfig
}