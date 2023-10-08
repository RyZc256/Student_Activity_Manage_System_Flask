# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: ResultTemplate
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午5:17
import datetime

from flask import jsonify

from models.ApiResultTemplate import ApiResultCode, ApiResultMsg


def SUCCESS(data):
    return jsonify(time=datetime.datetime.utcnow(),
                   code=ApiResultCode.SUCCESS,
                   msg=ApiResultMsg.SUCCESS,
                   data=data)


def FAIL():
    return jsonify(time=datetime.datetime.utcnow(),
                   code=ApiResultCode.FAIL,
                   msg=ApiResultMsg.FAIL)


def SYSTEM_ERROR():
    return jsonify(time=datetime.datetime.utcnow(),
                   code=ApiResultCode.SYSTEM_ERROR,
                   msg=ApiResultMsg.SYSTEM_ERROR)


def CAUSE(data):
    return jsonify(time=datetime.datetime.utcnow(),
                   code=ApiResultCode.FAIL,
                   msg=ApiResultMsg.FAIL,
                   data=data)
