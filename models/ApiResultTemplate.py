# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: ApiResultTemplate.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/1/2023 上午5:02

class ApiResultCode:
    # 操作成功
    SUCCESS = 200
    # 操作失败
    FAIL = -1
    # 数据不存在
    NO_DATA = -2
    # 系统异常
    SYSTEM_ERROR = 503
    # 用户未登录
    NO_AUTH = -200
    # 文件路径为空
    FILE_PATH_ISNULL = -11


class ApiResultMsg:
    FAIL = "fail"
    SUCCESS = "success"
    TOKEN_INVALID = "token.invalid"
    FILE_PATH_ISNULL = "error.fastdfs.file_path_isnull"
    FILE_ISNULL = "error.fastdfs.file_isnull"
    FILE_UPLOAD_FAILED = "error.fastdfs.file_upload_failed"
    FILE_NOT_EXIST = "error.fastdfs.file_not_exist"
    FILE_DOWNLOAD_FAILED = "error.fastdfs.file_download_failed"
    FILE_DELETE_FAILED = "error.fastdfs.file_delete_failed"
    FILE_SERVER_CONNECTION_FAILED = "error.fastdfs.file_server_connection_failed"
    FILE_OUT_SIZE = "error.fastdfs.file_server_connection_failed"
    FILE_TYPE_ERROR_IMAGE = "error.file.type.image"
    FILE_TYPE_ERROR_DOC = "error.file.type.doc"
    FILE_TYPE_ERROR_VIDEO = "error.file.type.video"
    FILE_TYPE_ERROR_COMPRESS = "error.file.type.compress"
    SYSTEM_ERROR = "error.system"