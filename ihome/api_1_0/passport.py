# coding:utf-8
from . import api_flask
from ..models import User
from flask import request,jsonify,current_app,session
from ..utils.response_code import RET
from ihome import redis_flask,db
import re
# 密码加密
from werkzeug.security import generate_password_hash

# POST
@api_flask.route("/users", methods=["POST"])
def register():
    # 接收参数
    print 1
    sms_dict = request.get_json()
    mobile = sms_dict.get("mobile")
    sms_code = sms_dict.get("sms_code")
    password = sms_dict.get("password")
    # 校验参数
    if not all([mobile,sms_code,password]):
        resp = {
            "errno":RET.PARAMERR,
             "errmsg":"missing"
        }
        return jsonify(resp)
    # 判断手机格式是否正确
    if not re.match(r"1[34578]\d{9}",mobile):
        resp = {
            "errno": RET.DATAERR,
            "errmsg": "mobile error"
        }
        return jsonify(resp)
    # 业务处理
    # 判断短信验证码是否过期
    sms_code_id = "sms_code_%s"%mobile
    try:
        real_sms_code = redis_flask.get(sms_code_id)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": "redis error"
        }
        return jsonify(resp)
    if real_sms_code is None:
        resp = {
            "errno": RET.NODATA,
            "errmsg": "sms_code out of data "
        }
        return jsonify(resp)
    # 判断sms_code是否正确
    if  real_sms_code != sms_code:
        resp = {
            "errno": RET.DATAERR,
            "errmsg": "sms_code error "
        }
        return jsonify(resp)
    # 删除短信验证码
    try:
        redis_flask.delete("sms_code_%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
    # 判断手机号是否已经被注册
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     resp = {
    #         "errno": RET.DBERR,
    #         "errmsg": "mysql error"
    #     }
    #     return jsonify(resp)
    # if user is None:
    #     resp = {
    #         "errno": RET.DATAEXIST,
    #         "errmsg": " user exist "
    #     }
    #     return jsonify(resp)
    # 保存用户的数据到数据库
    # 创建一个user对象
    user = User(name=mobile, mobile=mobile)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DATAERR,
            "errmsg": "mobile is exist"
        }
        return jsonify(resp)
    # 记住登陆状态
    session["user_id"] = user.id
    session["name"] = mobile
    session["mobile"] = mobile
    # 返回
    resp = {
            "errno": RET.OK,
            "errmsg": " register success "
        }
    return jsonify(resp)