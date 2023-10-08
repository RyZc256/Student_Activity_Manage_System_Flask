# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: __init__.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午7:55
from flask import Blueprint


authority_blu = Blueprint("authority_blu", __name__)

from .authority import *
