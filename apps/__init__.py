# !/usr/bin/env python
# coding:utf-8
# author bai

from flask import Flask,session,request
from .app01 import app01_blue
from .rbac import rbac_blue

def create_app():
    app = Flask(__name__)
    app.secret_key = 'fddfa'

    # 设置配置文件
    app.config.from_object('settings.BaseConfig')

    # 注册蓝图
    app.register_blueprint(app01_blue,url_prefix='/app01')
    app.register_blueprint(rbac_blue,url_prefix='/rbac')

    # 注册组件


    return app