# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: __init__.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午7:58
from flask import Blueprint

user_blu = Blueprint("user_blu", __name__)

from .user import *
from .userinfo import *
