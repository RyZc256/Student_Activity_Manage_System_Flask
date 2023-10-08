# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: WeChat
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 下午5:09
import json

import requests
from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

WX_APPID = app.config['WX_APPID']
WX_SECRET = app.config['WX_SECRET']


def wx_login(code):
    wxUrl = f"https://api.weixin.qq.com/sns/jscode2session?appid={WX_APPID}&secret={WX_SECRET}&js_code={code}&grant_type=authorization_code"
    web_requests = requests.get(url=wxUrl)
    print(web_requests.text)
    return json.loads(web_requests.text)