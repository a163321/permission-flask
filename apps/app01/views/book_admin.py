# !/usr/bin/env python
# coding:utf-8
# author bai
import re

from flask import Blueprint
from flask import render_template, request, session, redirect, url_for

app01_blue = Blueprint('app01_blue', __name__)
from .form import LoingForm
from apps.db.db import session_conn  # 用于sqlalchemy
from apps.rbac.models import User, Permission
from apps.rbac.service.init_permission import init_permission
from apps.rbac.views.menu import menu_html,Page_permission





@app01_blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoingForm()
        return render_template('app01/login.html', form=form)
    else:
        form = LoingForm(request.form)
        if form.validate():
            # 用户登录成功
            username = form.username.data
            pwd = form.password.data
            user = session_conn.query(User).filter(User.username == username, User.password == pwd).first()
            if user:
                # 登录成功
                session['current_user'] = {'user_id':user.id,'username':user.username}
                init_permission(user, request, session)
                return redirect(url_for('app01_blue.userinfo'))
            else:
                form.password.errors = '不号密码不匹配，重新登录！'
                return render_template('app01/login.html', form=form)
        else:
            return render_template('app01/login.html', form=form)

# User用户 内容相关的视图函数

@app01_blue.route('/userinfo/', endpoint='userinfo')
def userinfo():
    # code_list = request.permission_code_list  # 在当前页面用于显示的code_list
    # page_permission = Page_permission(code_list)

    # 模拟数据
    ret = session_conn.query(User).all()
    # menu_dic = menu_html(request)   # 生成用户在页面渲染菜单的数据，
    # return render_template('/app01/user/userinfo.html', page_permission=page_permission, data=ret, menu_dic=menu_dic)
    return render_template('/app01/user/userinfo.html', data=ret)


@app01_blue.route('/userinfo/add/', endpoint='user_add')
def userinfo_add():

    return render_template('/app01/user/user_add.html')


@app01_blue.route('/userinfo/edit/<int:nid>/', endpoint='user_edit')
def userinfo_edit(nid):

    menu_dic = menu_html(request)
    return render_template('/app01/user/user_edit.html',menu_dic=menu_dic)


@app01_blue.route('/userinfo/del/<int:nid>/', endpoint='user_del')
def userinfo_del(nid):
    return '用户信息删除成功'


# order订单 内容相关的视图函数
@app01_blue.route('/order/', endpoint='order')
def order():
    code_list = request.permission_code_list  # 在当前页面用于显示的code_list
    page_permission = Page_permission(code_list)

    # 模拟数据
    ret = session_conn.query(User).all()
    menu_dic = menu_html(request)
    return render_template('/app01/order/order.html', page_permission=page_permission, data=ret, menu_dic=menu_dic)


@app01_blue.route('/order/add/', endpoint='order_add')
def order_add():
    menu_dic = menu_html(request)

    return render_template('/app01/order/order_add.html', menu_dic=menu_dic)


@app01_blue.route('/order/edit/<int:nid>/', endpoint='order_edit')
def order_edit(nid):
    menu_dic = menu_html(request)
    return render_template('/app01/order/order_edit.html',menu_dic=menu_dic)


@app01_blue.route('/order/del/<int:nid>/', endpoint='order_del')
def order_del(nid):
    return '订单信息 删除成功'


# =====================================
@app01_blue.route('/test')
def test():
    # ret = session_conn.query(Menu).all()
    # for i in ret:
    #     print(i.title)
    # print(ret)

    # menu_obj = Menu(title='菜单五')
    # session.add(menu_obj)
    # session.commit()

    return '测试'



