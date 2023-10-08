# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: DateTimeUtils
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 下午3:56
import datetime


def Time_Zone_Conversion(GMT: str = "", zone: int = -8):
    GMT = datetime.datetime.strptime(GMT, '%Y-%m-%d %H:%M:%S')
    UTC = GMT + datetime.timedelta(hours=zone)
    return UTC

