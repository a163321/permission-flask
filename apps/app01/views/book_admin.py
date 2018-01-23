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


# 菜单的内容,
def menu_html(request):
    current_url = request.path
    menu_list = session.get('menu_list')

    # 思路：直接拿到当前url，拿到他的组内菜单，然后在menu_list中，修改他的item['active'] = True,用于在前端页面展示
    all_url = session_conn.query(Permission).all()
    for url_reg in all_url:
        reg = '^{0}$'.format(url_reg.url)
        if re.match(reg, current_url):  # 匹配上那么url_reg就是当前访问的url,只需要找到他的组内菜单url即可，
            if not url_reg.menu_gp:  # 访问url就是组内做菜单的url
                for item in menu_list:
                    url = item['permission_url']
                    new_reg = '^{0}$'.format(url)
                    if re.match(new_reg, url_reg.url):
                        item['active'] = True
            else:
                for item in menu_list:
                    url = item['permission_url']
                    new_reg = '^{0}$'.format(url)
                    if re.match(new_reg, url_reg.per_menu_gp.url):   # url_reg是跟当前访问的url匹配的数据库permission表中的一个对象
                        item['active'] = True


    menu_show_dic = {}  # 这个字典中储存格式化的菜单，在前端直接两层for循环出来展示就可以了，
    for item in menu_list:
        if item['menu_id'] in menu_show_dic:
            menu_show_dic[item['menu_id']]['children'].append(
                {'permission__title': item['permission__title'], 'permission_url': item['permission_url'],
                 'active': item['active']})
            if item['active']:
                menu_show_dic[item['menu_id']]['active'] = True
        else:
            menu_show_dic[item['menu_id']] = {'menu_id': item['menu_id'],
                                              'menu_title': item['menu_title'],
                                              'active': False,
                                              'children': [{'permission__title': item['permission__title'],
                                                            'permission_url': item['permission_url'],
                                                            'active': item['active']}, ]
                                              }
            if item['active']:
                menu_show_dic[item['menu_id']]['active'] = True

    return menu_show_dic


class Page_permission(object):
    '''用于在页面显示按钮，便签是否显示'''
    def __init__(self, code_list):
        self.code_list = code_list

    def has_add(self):
        if 'add' in self.code_list:
            return True

    def has_list(self):
        if 'list' in self.code_list:
            return True

    def has_edit(self):
        if 'edit' in self.code_list:
            return True

    def has_del(self):
        if 'del' in self.code_list:
            return True


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
                init_permission(user, request, session)
                return redirect(url_for('app01_blue.userinfo'))
            else:
                form.password.errors = '账号.密码不匹配，重新登录！'
                return render_template('app01/login.html', form=form)
        else:
            return render_template('app01/login.html', form=form)

# User用户 内容相关的视图函数

@app01_blue.route('/userinfo/', endpoint='userinfo')
def userinfo():
    code_list = request.permission_code_list  # 在当前页面用于显示的code_list
    page_permission = Page_permission(code_list)

    # 模拟数据
    ret = session_conn.query(User).all()
    menu_dic = menu_html(request)
    return render_template('/app01/user/userinfo.html', page_permission=page_permission, data=ret, menu_dic=menu_dic)


@app01_blue.route('/userinfo/add/', endpoint='user_add')
def userinfo_add():
    menu_dic = menu_html(request)

    return render_template('/app01/user/user_add.html', menu_dic=menu_dic)


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

# ===========================================
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



