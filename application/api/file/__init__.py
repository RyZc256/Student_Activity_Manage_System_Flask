# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: __init__.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午2:06
from flask import Blueprint


file_blu = Blueprint("file_blu", __name__)

from .file import *