# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: activity
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午2:05
from datetime import datetime

from flask import session, request
from sqlalchemy import and_, or_

from application.api.activity import activity_blu
from models import ResultTemplate
from models.Models import *
from models.ObjectJsonConvert import *


@activity_blu.route('/getnear', methods=['POST'])
def get_activity():
    try:
        user = User.query.filter_by(id=session.get("uid")).first()
        type = request.values.get("type")
        if type == "live":
            time_now = datetime.now()
            activityList = Activity.query.filter(or_(and_(Activity.start_time > time_now,
                                                      Activity.cutoff_time == None),
                                                 or_(Activity.cutoff_time > time_now))).all()
            return ResultTemplate.SUCCESS(Activity_2_Json(activityList))
        else:
            time_now = datetime.now()
            activityList = Activity.query.filter(Activity.start_time > time_now).all()
            return ResultTemplate.SUCCESS(Activity_2_Json(activityList))
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()
