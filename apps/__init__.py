# !/usr/bin/env python
# coding:utf-8
# author bai

from flask import Flask,session,request
from .app01 import app01_blue
from .rbac import rbac_blue
from apps.db.db import session_conn
from flask_admin import Admin,BaseView,expose  # 用于做后台管理的组件
from apps.rbac.views.rbac_view import CustomView,CustomModelView,MenuModelView,PermissionModelView
from apps.rbac.models import Menu,Group,User,User2Role,Role,Role2Permission,Permission

def create_app():
    app = Flask(__name__)
    app.debug=True
    app.secret_key = 'fddfa'

    # 设置配置文件
    app.config.from_object('settings.BaseConfig')

    # 注册蓝图
    app.register_blueprint(app01_blue,url_prefix='/app01')
    app.register_blueprint(rbac_blue,url_prefix='/rbac')

    # 注册后台管理的组件
    flask_admin = Admin(base_template='admin/base_menu.html') # 使用自己的模板，覆盖原来的模板
    flask_admin.init_app(app)
    # flask_admin.add_view(CustomView(name='cus_name',endpoint='helloworld'))
    # 上一句，假如设定了name属性，在页面菜单显示name的值,否则显示customView,
    # 设置了endpoint属性，则是会改变url,url就是endpoint的值


    models = [Group,User,Role,]
    for model in models:
        flask_admin.add_view(
            # CustomModelView(model, session_conn,name='权限相关'))  # 如果设置name属性，则这些表都会显示在一组
            CustomModelView(model, session_conn))

    # 类似于注册处理这个model表的类
    flask_admin.add_view(MenuModelView(Menu,session_conn,endpoint='menu'))
    flask_admin.add_view(PermissionModelView(Permission,session_conn,endpoint='permission'))

    return app