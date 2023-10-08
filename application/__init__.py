# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: SAMS
# @FileName: __init__.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 5/1/2023 下午3:52
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.dev import DevelopementConfig
from config.prop import ProductionConfig

db = SQLAlchemy()

config = {
    "dev": DevelopementConfig,
    "prop": ProductionConfig,
}


# 把日志相关的配置封装成一个日志初始化函数
def setup_log(Config):
    # 设置日志的记录等级
    logging.basicConfig(level=Config.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 300, backupCount=100)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaskapp使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def regist_blueprints(app):
    # 导入蓝图对象
    # 注册api蓝图,url_prefix为所有路由默认加上的前缀
    from application.api.authority import authority_blu
    app.register_blueprint(authority_blu, url_prefix='/authority')
    from application.api.user import user_blu
    app.register_blueprint(user_blu, url_prefix='/user')
    from application.api.activity import activity_blu
    app.register_blueprint(activity_blu, url_prefix='/activity')
    from application.api.file import file_blu
    app.register_blueprint(file_blu, url_prefix='/file')


def init_app(config_name):
    """项目的初始化函数"""
    app = Flask(__name__)

    # 设置配置类
    Config = config[config_name]

    # 加载配置
    app.config.from_object(Config)

    print(app.config)

    # 数据库初始化
    db.init_app(app)

    # 日志
    setup_log(Config)

    # 注册蓝图
    regist_blueprints(app)

    return app
