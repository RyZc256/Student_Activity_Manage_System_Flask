# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: Obj_2_Json
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午4:01
import json

from models.Models import *


def UserObj_2_Json(obj: User):
    """
    User对象 转换 Json数据（User Not Key information）
    :param obj: User对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        return {"id": obj.id,
                # "openid": obj.openid,
                # "session_key": obj.session_key,
                # "password": obj.password,
                "role": obj.role_ForeignKey.name,
                "last_login": obj.last_login,
                "status": obj.status
                }
    except Exception as e:
        print(e)
        return "error"


def UserInfo_2_Json(obj: Userinfo):
    """
    UserInfo对象 转换 Json数据（UserInfo ALL）
    :param obj: Userinfo对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        user = User.query.filter_by(id=obj.id).first()
        if user.role == 3:
            # 普通用户直接使用
            classTable = obj.class_ForeignKey
        else:
            # 管理员班级为空,需要重新查找
            classTable = Classtable.query.filter_by(administrator=obj.id).all()
        departmentServer = DepartmentServe.query.filter_by(user=obj.id).all()
        return {
            "id": obj.id,
            "name": obj.name,
            "tel": obj.tel,
            "age": obj.age,
            "role": user.role_ForeignKey.name,
            "mail": obj.mail,
            "sex": "男" if obj.sex else "女",
            "wechat": "未绑定" if user.openid is None else "已绑定",
            "avatar": obj.avatar,
            "class": Class_2_Json(classTable),
            "department": DepartmentServe_2_JSON(departmentServer),
            "idcard": str(obj.idcard[0:4]) + "************" + str(obj.idcard[16:18]),
            "address": obj.address,
            "join_time": str(obj.join_time)
        }
    except Exception as e:
        print(e)
        return "error"


def DepartmentServe_2_JSON(obj: DepartmentServe):
    """
    DepartmentServe对象 转换 Json数据
    :param obj: DepartmentJob对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        if isinstance(obj, list):
            data = []
            for i in obj:
                data.append({
                    "id": i.id,
                    "department": Department_2_JSON(i.department_ForeignKey),
                    "job": Job_2_JSON(i.department_job_ForeignKey),
                    "start_time": i.start_date,
                    "end_time": i.end_date
                })
            return data
        else:
            return {
                "id": obj.id,
                "department": Department_2_JSON(obj.department_ForeignKey),
                "job": Job_2_JSON(obj.job_ForeignKey),
                "start_time": obj.start_date,
                "end_time": obj.end_date
            }
    except Exception as e:
        print(e)
        return "error"


def Job_2_JSON(obj: DepartmentJob):
    """
    DepartmentJob对象 转换 Json数据
    :param obj: Job对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        return {
            "id": obj.id,
            "name": obj.name
        }
    except Exception as e:
        print(e)
        return "error"


def Department_2_JSON(obj: Department):
    """
    Department对象 转换 Json数据
    :param obj: Department对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        return {
            "id": obj.id,
            "name": obj.name,
            "administrator": AdminInfo_2_Json(obj.administrator_ForeignKey)
        }
    except Exception as e:
        print(e)
        return "error"


def College_2_Json(obj: College):
    """
    College对象 转换 JSON 数据
    :param obj: College对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        return {
            "id": obj.id,
            "name": obj.name
        }
    except Exception as e:
        print(e)
        return "error"


def SimpleUserInfo_2_Json(obj: Userinfo):
    """
    UserInfo对象 转换 Json数据（UserInfo Simple）
    :param obj: Userinfo对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        user = User.query.filter_by(id=obj.id).first()
        classTable = Classtable.query.filter_by(administrator=obj.id).all()
        return {
            "id": obj.id,
            "name": obj.name,
            # "wechat": "未绑定" if user.openid is None else "已经绑定",
            "avatar": obj.avatar,
            "tel": obj.tel,
            "mail": obj.mail,
            "role": user.role_ForeignKey.name,
            "class": Class_2_Json(obj.class_ForeignKey) if user.role == 3 else Class_2_Json(classTable),
            "join_time": str(obj.join_time)
        }
    except Exception as e:
        print(e)
        return "error"


def AdminInfo_2_Json(obj: Userinfo):
    """
    UserInfo对象 转换 Json数据（Admin）
    :param obj: Userinfo对象
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        return {
            "id": obj.id,
            "name": obj.name,
            "tel": obj.tel,
            "mail": obj.mail,
            "avatar": obj.avatar,
            "join_time": str(obj.join_time)
        }
    except Exception as e:
        print(e)
        return "error"


def Class_2_Json(obj: Classtable):
    """
    Classtable 转换 JSON 数据
    :param obj: Classtable
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        if isinstance(obj, list):
            data = []
            for i in obj:
                data.append({"id": i.id,
                             "college": College_2_Json(i.college_ForeignKey),
                             "name": i.name,
                             "administrator": AdminInfo_2_Json(Userinfo.query.filter_by(id=i.administrator).first()),
                             "abbreviation": i.abbreviation})
            return data
        else:
            return {"id": obj.id,
                    "college": College_2_Json(obj.college_ForeignKey),
                    "name": obj.name,
                    "administrator": AdminInfo_2_Json(Userinfo.query.filter_by(id=obj.administrator).first()),
                    "abbreviation": obj.abbreviation}
    except Exception as e:
        print(e)
        return "error"


def ClassUserInfo_2_Json(obj1: Classtable, obj2):
    """
    Classtable&UserInfo对象 转换 JSON数据
    :param obj1: Classtable
    :param obj2: UserInfo对象
    :return: JSON数据
    """
    if obj2 is None or obj2 is None: return "null"
    try:
        result = {
            "class": Class_2_Json(obj1),
            "userNumber": obj2.count(),
        }
        # 班级成员信息
        userInfoList = []
        for userinfo in obj2:
            userInfoList.append({
                "id": userinfo.id,
                "name": userinfo.name,
                "tel": userinfo.tel,
                "mail": userinfo.mail,
                "avatar": userinfo.avatar,
                "join_time": str(userinfo.join_time)
            })
        result['userInfoList'] = userInfoList
        return result
    except Exception as e:
        print(e)
        return "error"


def Json_2_UserInfo_User(obj: Userinfo, data: json):
    """
    JSON 数据转换 Userinfo 对象 (User)
    :param obj: userinfo对象
    :param data: json数据
    :return: 更新转换后的Userinfo对象
    """
    if obj is None or data is None: return "null"
    try:
        obj.tel = data['tel']
        obj.mail = data['mail']
        obj.address = data['address']
        return obj
    except Exception as e:
        print(e)
        return "error"


def Activity_2_Json(obj: Activity):
    """
    Activity对象 转换 JSON 数据
    :param obj: Activity
    :return: JSON数据
    """
    if obj is None: return "null"
    try:
        if isinstance(obj, list):
            data = []
            for i in obj:
                data.append({"id": i.id,
                             "name": i.name,
                             "detail": i.detail,
                             "regiser_time": str(i.regiser_time),
                             "cutoff_time": str(i.cutoff_time),
                             "limit_number": i.limit_number,
                             "start_time": str(i.start_time),
                             "end_time": str(i.end_time),
                             "address": i.address,
                             "administrator": AdminInfo_2_Json(i.administrator_ForeignKey),
                             "user": SimpleUserInfo_2_Json(i.user_ForeignKey)})
            return data
        else:
            return {
                "id": obj.id,
                "name": obj.name,
                "detail": obj.detail,
                "regiser_time": str(obj.regiser_time),
                "cutoff_time": str(obj.regiser_time),
                "limit_number": obj.limit_number,
                "start_time": str(obj.start_time),
                "end_time": str(obj.end_time),
                "address": obj.address,
                "administrator": AdminInfo_2_Json(obj.administrator_ForeignKey),
                "user": SimpleUserInfo_2_Json(obj.user_ForeignKey)
            }
    except Exception as e:
        print(e)
        return "error"

