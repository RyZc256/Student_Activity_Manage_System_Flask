# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: login
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午7:56
import datetime

from application.api.authority import authority_blu
from flask import request

from application.api.utils.database import mysql_commit
from models.Models import *
from models import ResultTemplate

from utils.JwtToken import generate_token, identify
from utils.WeChatUtils import wx_login


@authority_blu.route('/login', methods=['POST'])
def login():
    """
    登录接口    path: /authority/login?code={parameter} methods: POST
    使用微信小程序临时登录凭证， 微信小程序调用wx.login()
    :return: REFRESH TOKEN JSON
    """
    try:
        # 微信小程序临时登录凭证
        code = request.values.get("code")
        # 获取微信OPENID & SESSION_KEY
        wx_response = wx_login(code)
        # 验证OPENID是否绑定
        user = User.query.filter_by(openid=wx_response['openid']).first()
        # 无法通过openid查询到账号
        if user is None:
            return ResultTemplate.CAUSE("账号未绑定微信号")
        # 长时效Token 48小时
        refresh_token = generate_token(type="refresh", uid=user.id)
        # 更改数据库中的session_key
        """ sessionkey 使用redis存储 """
        # user.session_key = wx_response['session_key']
        """ sessionkey 使用redis存储 """
        # 记录最后登录时间
        user.last_login = datetime.datetime.utcnow()
        # 操作数据库
        return mysql_commit(user, refresh_token)
    except Exception as e:
        print(e.args)
        return ResultTemplate.SYSTEM_ERROR()


@authority_blu.route('/accesstoken', methods=['POST'])
def GenerateAccessToken():
    """
    ACCESS TOKEN 生成接口   path: /authority/accesstoken?refresh_token={parameter}  methods: POST
    需在请求参数中携带refresh Token
    :return: ACCESS TOKEN JSON
    """
    try:
        # 长时效TOKEN
        refresh_token = request.values.get("refresh_token")
        # 验证TOKEN是否有效
        verification = identify(refresh_token)
        # TOKEN无效 或为 ACCESS TOKEN 不允许进行后续换领ACCESS TOKEN操作
        if not verification or verification["type"] == "access":
            return ResultTemplate.CAUSE("Token 失效")
        # 查询TOKEN用户名是否存在数据库当中
        user = User.query.filter_by(id=verification["uid"]).first()
        # 创建ACCESS TOKEN
        access_token = generate_token(uid=user.id)
        # 返回JSON结果
        return ResultTemplate.SUCCESS(access_token)
    except Exception as e:
        print(e.args)
        return ResultTemplate.SYSTEM_ERROR()


@authority_blu.route('/bindwx', methods=['POST'])
def bindwx():
    """
    绑定微信接口  path: /authority/bindwx methods: POST
    使用json body传递参数, 参数包括 账号、密码、微信小程序临时登录凭证
    微信小程序临时登录凭证调用wx.login()
    :return: 操作结果JSON
    """
    try:
        body = request.json
        # 验证账号密码是否正确
        user = User.query.filter_by(id=body['uid'], password=body['password']).first()
        # 账号密码错误
        if user is None:
            return ResultTemplate.CAUSE("账号或密码错误")
        # 账号已被停用
        if user.status == 1:
            return ResultTemplate.CAUSE("账号已被停用")
        # 账号已被绑定
        if user.openid is not None:
            return ResultTemplate.CAUSE("账号已绑定微信")
        # 获取微信OPENID & SESSION_KEY
        wx_response = wx_login(body['code'])
        # 验证OPENID是否已被绑定
        user_openid = User.query.filter_by(openid=wx_response['openid']).first()
        if user_openid is not None:
            return ResultTemplate.CAUSE("微信号已被绑定账号")
        # 绑定微信OPENID
        user.openid = wx_response['openid']
        """ sessionkey 使用redis存储 """
        # user.session_key = wx_response['session_key']
        """ sessionkey 使用redis存储 """
        # 操作数据库
        return mysql_commit(user, "微信号绑定成功")
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()


@authority_blu.route('/temptest', methods=['GET'])
def temptest():
    try:
        id = request.values.get("id")
        password = request.values.get("password")
        user = User.query.filter_by(id=id, password=password).first()
        refresh_token = generate_token(type="refresh", uid=user.id)
        return ResultTemplate.SUCCESS(refresh_token)
    except Exception as e:
        print(e.args)
        return ResultTemplate.SYSTEM_ERROR()
