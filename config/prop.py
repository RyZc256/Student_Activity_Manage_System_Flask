# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: prop.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/1/2023 下午5:27
from . import Config


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = False
