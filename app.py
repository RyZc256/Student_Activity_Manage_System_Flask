# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: app.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午5:29
from flask import request, session, render_template

from application import init_app
from models import ResultTemplate
from utils.JwtToken import identify

app = init_app("dev")


@app.route("/")
def index():
    return render_template("index.html")
    # return "Hello world"


# 拦截器
@app.before_request
def before():
    # 当前请求的URL
    url = request.path
    # 拦截器白名单
    passUrl = url.startswith('/authority/')
    # 文件后缀白名单
    suffix = url.endswith('.png') or url.endswith('.jpg') or url.endswith('.css') or url.endswith('.js')
    if url in '/' or passUrl or suffix:
        pass
    else:
        token = request.headers.get("token")
        verification = identify(token)
        # ACCESS TOKEN 无效或为 REFRESH TOKEN 拒绝响应
        if not verification or verification['type'] == 'refresh':
            return ResultTemplate.CAUSE("TOKEN 无效")
        else:
            # 解析后将用户名写入session
            session.permanent = True
            session['uid'] = verification['uid']
            pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500)
