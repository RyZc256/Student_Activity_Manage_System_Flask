# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: dev.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午5:27
from . import Config


class DevelopementConfig(Config):
    """开发模式下的配置"""
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
