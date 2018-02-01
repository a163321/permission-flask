# !/usr/bin/env python
# coding:utf-8
# author bai

from flask import Flask,session,request
from .app01 import app01_blue
from .rbac import rbac_blue
from apps.db.db import session_conn
from flask_admin import Admin,BaseView,expose  # 用于做后台管理的组件
from apps.rbac.views.rbac_view import CustomView,CustomModelView
from apps.rbac.models import Menu,Group,User,User2Role,Role,Role2Permission,Permission

def create_app():
    app = Flask(__name__)
    app.secret_key = 'fddfa'

    # 设置配置文件
    app.config.from_object('settings.BaseConfig')

    # 注册蓝图
    app.register_blueprint(app01_blue,url_prefix='/app01')
    app.register_blueprint(rbac_blue,url_prefix='/rbac')

    # 注册后台管理的组件
    flask_admin = Admin()
    flask_admin.init_app(app)
    flask_admin.add_view(CustomView(name='first'))
    models = [Menu,Group,User,User2Role,Role,Role2Permission,Permission]
    for model in models:
        flask_admin.add_view(
            CustomModelView(model, session_conn, category='权限表'))

    return app