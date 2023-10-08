# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: userinfo
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午2:02
import uuid

from PIL import Image
from flask import session, request, make_response

from application.api.user import user_blu
from application.api.utils.database import mysql_commit
from models import ResultTemplate

from models.ObjectJsonConvert import *


@user_blu.route('/info/get', methods=['POST'])
def get_info():
    """
    获取用户信息接口  path: /user/info/get?type=simple  methods: POST
    携带参数type非必选项，未携带返回完全用户信息（关键信息脱敏），携带type且值为simple返回简要用户信息（不包含关键信息）
    :return: 操作结果JSON
    """
    # 用户信息
    try:
        type = request.values.get("type")
        id = request.values.get("id")
        user = User.query.filter_by(id=session.get("uid")).first()
        # 携带ID参数又想查询别人, 想屁呢
        if id is not None and user.role == 3:
            return ResultTemplate.CAUSE("无权限查看")
        # 完全用户信息
        if type is None:
            userInfo = Userinfo.query.filter_by(id=session.get('uid')).first()
            return ResultTemplate.SUCCESS(UserInfo_2_Json(userInfo))
        # 简要用户信息
        elif type == "simple":
            userInfo = Userinfo.query.filter_by(id=session.get('uid')).first()
            return ResultTemplate.SUCCESS(SimpleUserInfo_2_Json(userInfo))
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()


@user_blu.route('/info/getadmin', methods=['POST'])
def get_admin_info():
    """
    获取管理员信息接口  path: /user/info/getadmin?uid={parameter}    methods: POST
    携带参数uid为管理员uid, 返回简要信息（不包括关键信息）
    :return: 操作结果JSON
    """
    # 用户信息
    try:
        # 获取request参数
        uid = request.values.get("uid")
        # 获取发起请求的用户信息
        requestUserInfo = Userinfo.query.filter_by(id=session.get("uid")).first()
        # 获取发起请求的用户
        user = User.query.filter_by(id=session.get("uid")).first()
        # 判断是否是有联系的用户,否则拒绝请求
        if user.role == 1 or user.role == 2 or str(requestUserInfo.class_ForeignKey.administrator) == uid:
            # 查询用户资料
            userInfo = Userinfo.query.filter_by(id=uid).first()
            return ResultTemplate.SUCCESS(AdminInfo_2_Json(userInfo))
        else:
            return ResultTemplate.CAUSE("无权限查看")
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()


@user_blu.route("/avatar/upload", methods=["POST"])
def upload_avatar():
    """
    头像上传接口  path: /user/avatar/upload   methods: POST
    使用form上传头像文件
    :return: 操作结果JSON
    """
    # 1.提取新头像
    try:
        avatar = request.files.get("avatar")
        if avatar:
            # 如果存在用Image打开新图片
            img = Image.open(avatar)
            # 根据session获取的用户id，从数据库匹配并获取用户
            userInfo = Userinfo.query.filter_by(id=session.get('uid')).first()
            # 添加图片路径文件夹
            img_name = str(uuid.uuid4()) + ".jpg"
            img_path = './static/images/user_avatar/' + img_name
            # 将该图片命名并存放到指定路径
            img.save(img_path)
            # 将该用户的头像路径更改为该图片路径
            userInfo.avatar = img_name
            # 数据库操作
            return mysql_commit(userInfo, "头像修改成功")
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()


@user_blu.route('/avatar/<string:filename>', methods=['GET'])
def avatar(filename):
    """
    头像请求接口  path: /user/avatar/{parameter}.jpg/png   methods: GET
    携带头像名称请求
    :return: 显示头像
    """
    if request.method == 'GET':
        print(filename)
        if filename is None:
            pass
        else:
            # 加载头像
            image_data = open("./static/images/user_avatar/" + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass


@user_blu.route('/info/getclass', methods=['POST'])
def get_class():
    """
    获取组织信息接口    path: /user/info/getclass?id={parameter}&keyword={parameter}   methods: POST
    携带参数id为必选项，keyword为非必选项，id指代组织编码，keyword指代内部成员模糊查找关键字。未携带keyword则返回全部成员姓名及电话数据
    :return: 操作结果JSON
    """
    # 用户信息
    try:
        # 获取requests参数
        id = request.values.get("id")
        keyword = request.values.get("keyword")
        # 查询请求的用户
        userInfo = Userinfo.query.filter_by(id=session.get('uid')).first()
        # 查询用户角色
        user = User.query.filter_by(id=session.get('uid')).first()
        # 如果用户为普通角色并且查询的不是所在组织，拒绝请求
        if user.role == 3 and id != str(userInfo.class_id):
            return ResultTemplate.CAUSE("无权限查看")
        classTable = Classtable.query.filter_by(id=id).first()
        # 判断是否有关键字查找
        if keyword is not None:
            userInfoList = userInfo.query.filter_by(class_id=id).filter(Userinfo.name.like("%{}%".format(keyword)))
        else:
            userInfoList = userInfo.query.filter_by(class_id=id)
        return ResultTemplate.SUCCESS(ClassUserInfo_2_Json(classTable, userInfoList))
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()


@user_blu.route('/info/edit', methods=['POST'])
def edit_info():
    """
    编辑用户资料接口    path: /user/info/edit   methods: POST
    使用json body传递参数, 参数包括整个UserInfo对象
    :return:
    """
    # 用户信息
    try:
        # 获取request参数
        body = request.json
        # 默认为普通用户申请修改资料
        type = "user"
        # 查询请求修改的用户当前在系统中原有的数据
        userInfo = Userinfo.query.filter_by(id=body['id']).first()
        # 获取用户资料
        user = User.query.filter_by(id=session.get("uid")).first()
        # 判断是否为超管或管理员
        if user.role == 1:
            type = "superadmin"
        elif user.role == 2:
            type = "admin"
        if user.id == userInfo.id:
            # 更新数据
            new_userInfo = Json_2_UserInfo_User(userInfo, body)
            # 更新数据库数据
            return mysql_commit(new_userInfo, "资料更新成功")
        # 当发起请求的用户为管理员，并且非管理该组织的管理员，或请求操作的用户与要修改的用户不为同一用户，拒绝操作
        elif type == "admin" and userInfo.class_ForeignKey.administrator != user.id or user.id != userInfo.id:
            return ResultTemplate.CAUSE("无权限操作")
    except Exception as e:
        print(e)
        return ResultTemplate.SYSTEM_ERROR()
