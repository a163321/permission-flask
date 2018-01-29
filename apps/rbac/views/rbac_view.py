# !/usr/bin/env python
# coding:utf-8
# author bai
import re
from flask import Blueprint,request,session,current_app,redirect,url_for,render_template
from .menu import Page_permission,menu_html
from apps.db.db import session_conn  # 用于sqlalchemy连接

rbac_blue = Blueprint('rbac_blue',__name__)

# 伪中间件
@rbac_blue.before_app_request
def process_request():
    current_url = request.path
    VALID_URL = current_app.config['VALID_URL']

    # 1.白名单验证
    valid_url = VALID_URL
    for each in valid_url:
        if re.match(each, current_url):
            return None

    # 2.验证是否已经登录
    permission_dic = session.get('show_per_dic')
    if not permission_dic:
        return redirect(url_for('app01_blue.login'))

    # 3.当前访问的url与权限url进行匹配验证,并在request中写入code信息，
    flag = False
    for group_id, code_urls in permission_dic.items():
        for url in code_urls['per_url']:
            regax = '^{0}$'.format(url)
            if re.match(regax, current_url):
                flag = True
                request.permission_code_list = code_urls['code']  # 在session中增加code的信息，用于在页面判断在当前页面的权限，
                break
        if flag:
            break

    if not flag:
        return '无权访问'

@rbac_blue.after_app_request
def process_response(response):
    return response

 
# 关于crud视图函数
# 表的显示

@rbac_blue.route('/<query_name>/')
def query_show(query_name):
    print('现在操作的表是%s'%query_name)
    code_list = request.permission_code_list  # 在当前页面用于显示的code_list
    page_permission = Page_permission(code_list)
    menu_dic = menu_html(request)  # 生成用户在页面渲染菜单的数据，
    # 根据当前query_name，用正则匹配到在数据库的表名称，即忽略大小写就可以了，然后查看到数据库的字段，数据，
    total_tabes = current_app.config['TOTAL_TABLES']  # 当前所有的数据库表对象，
    for tb in total_tabes:
        if tb.__name__.lower() == query_name:
            current_tb = tb

    data = session_conn.query(current_tb).all()

    return render_template('rbac/menu.html',page_permission=page_permission,menu_dic=menu_dic,data=data)

# 表的添加
@rbac_blue.route('/<query_name>/add/')
def query_add(query_name):
    print(query_name)
    return '对%s表进行添加操作'%query_name

# 表的修改
@rbac_blue.route('/<query_name>/edit/<int:nid>/')
def query_edit(query_name,nid):
    print(query_name,nid)
    return '对%s表进行编辑操作'%query_name

# 表的删除
@rbac_blue.route('/<query_name>/del/<int:nid>/')
def query_del(query_name,nid):
    print(query_name,nid)
    return '对%s表进行删除操作'%query_name