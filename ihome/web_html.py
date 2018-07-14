# coding:utf-8
from flask import Blueprint,current_app ,make_response # current_app 是app的一个代理人
from flask_wtf.csrf import generate_csrf
html = Blueprint("html",__name__)


@html.route("/<re(r'.*'):file_name>")
def get_static_html(file_name):
    # 根据用户访问的文件名来返回相应的页面
    # 如果用户没有输入html信息,跳转到首页
    if not file_name:
        file_name="index.html"
    if file_name !="favicon.ico":
        file_name = "html/"+file_name
    # 生成csrf_token字符串 为用户设置cookie
    csrf_token = generate_csrf()
    resp = make_response(current_app.send_static_file(file_name))
    # 用make_response对象把csrf_token设置入cookie,为了保证每次进入页面都是不同的csrf_token，这里不设置过期时间
    resp.set_cookie("csrf_token",csrf_token)
    return resp