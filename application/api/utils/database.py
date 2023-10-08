# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: mysql
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 9/1/2023 上午3:52
from application import db
from models import ResultTemplate
from models.Models import *


def mysql_commit(obj, response):
    """
    Mysql数据库操作 增加、删除
    :param obj: 对象
    :param response: 响应内容
    :return:
    """
    try:
        # 更新数据库数据
        db.session.add(obj)
        db.session.commit()
        # 返回JSON结果
        return ResultTemplate.SUCCESS(response)
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e
        return ResultTemplate.SYSTEM_ERROR()