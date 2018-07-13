# coding:utf-8
from . import api_flask
from ihome.utils.captcha.captcha import captcha
from ihome import redis_flask,constants
from ihome.libs.yuntongxun import SendTemplateSMS
from flask import current_app,jsonify,make_response,request
from ihome.utils.response_code import RET
import random
@api_flask.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    # 获取参数
    # 校验参数
    # 业务处理
    # 1.生成验证码图片 generate_captcha方法返回三个值 名字,验证码真实值,图片的二进制数据
    name,text,image_data= captcha.generate_captcha()
    try:
        # 2.把编号和真实值保存进redis 用字符串类型
        #redis_flask.set("image_code%s"%image_code_id,text)
        # 设置有效期
        #redis_flask.expires("image_code%s"%image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES)
        # 上面两条的简写
        redis_flask.setex("image_code%s"%image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        # 在日志中记录异常
        current_app.logger.error(e)
        resp = {
            "errno":RET.DBERR,
            "errmsg":"save image in redis failed"
        }
        return jsonify(resp)
    # 返回结果
    resp=make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
# GET 需要接受手机号 图片验证码 图片验证码的编号
@api_flask.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def send_sms_code(mobile):
    # 获取参数
    # 获取图片验证码的编号
    image_code_id = request.args.get("image_code_id")
    # 获取用户写入的验证码
    image_code = request.args.get("image_code")
    # 校验参数
    if not all([image_code_id,image_code]):
        resp = {
            "errno": RET.PARAMERR,
            "errmsg": "missing canshu"
        }
        return jsonify(resp)
    # 判断验证码是否成功取出
    try:
        real_image_code = redis_flask.get("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": " get real_image_code error"
        }
        return jsonify(resp)
    # 判断有效期
    if real_image_code is None:
        resp = {
            "errno": RET.DATAERR,
            "errmsg": " real_image_code out of data"
        }
        return jsonify(resp)
    # 删除图片验证码
    try:
        redis_flask.delete("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    # 判断验证码是否与用户输入一致
    if real_image_code.lower() != image_code.lower():
        resp = {
            "errno": RET.DATAERR,
            "errmsg": " real_image_code not equal to image_code"
        }
        return jsonify(resp)
    # 创建短信验证码
    sms_code = "%06d"%random.randint(0,999999)
    # 保存短信验证码
    try:
        redis_flask.setex("sms_code_%s"%image_code_id,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": " set sms_code error "
        }
        return jsonify(resp)
    # 发送短信
    try:
        ccp = SendTemplateSMS.CCP()
        result=ccp.send_template_sms(mobile,[sms_code,str(constants.SMS_CODE_REDIS_EXPIRES/60)],1)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.THIRDERR,
            "errmsg": " send sms_code error "
        }
        return jsonify(resp)
    if result == 0:
        # 发送成功
        resp = {
            "errno": RET.OK,
            "errmsg": " send sms_code success "
        }
        return jsonify(resp)
    else:
        resp = {
            "errno": RET.THIRDERR,
            "errmsg": " send sms_code error "
        }
        return jsonify(resp)
    # 返回值