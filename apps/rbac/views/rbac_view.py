# !/usr/bin/env python
# coding:utf-8
# author bai
import re
from flask import Blueprint, request, session, current_app, redirect, url_for, render_template
from .menu import Page_permission, menu_html
from apps.db.db import session_conn  # 用于sqlalchemy连接
from flask_admin import BaseView, expose
from flask import g


rbac_blue = Blueprint('rbac_blue', __name__)


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

                code_list = request.permission_code_list  # 在当前页面用于显示的code_list
                page_permission = Page_permission(code_list)
                g.page_permission = page_permission  # 用于在当前页显示编辑、添加、删除的权限

                break
        if flag:
            break
    # g 在全局中设置菜单的信息，以及
    g.menu_dic = menu_html(request)  # 菜单的数据



    # if not flag:
    #     return '无权访问'


@rbac_blue.after_app_request
def process_response(response):
    return response


# 关于crud视图函数
# 表的显示

def get_current_tb(query_name):
    # 根据当前query_name，用正则匹配到在数据库的表名称，即忽略大小写就可以了，然后查看到数据库的字段，数据，
    total_tabes = current_app.config['TOTAL_TABLES']  # 当前所有的数据库表对象，
    for tb in total_tabes:
        if tb.__name__.lower() == query_name:
            current_tb = tb
    return current_tb


@rbac_blue.route('/<query_name>/')
def query_show(query_name):
    code_list = request.permission_code_list  # 在当前页面用于显示的code_list
    page_permission = Page_permission(code_list)
    menu_dic = menu_html(request)  # 生成用户在页面渲染菜单的数据，
    print(request.args.get('page'))
    current_tb = get_current_tb(query_name)

    data = session_conn.query(current_tb).all()
    show_fields = current_app.config['CRUD'].get(current_tb.__name__)  # 拿到配置的当前表要显示的字段

    return render_template('rbac/crud_layout.html', page_permission=page_permission, menu_dic=menu_dic, data=data,
                           show_fields=show_fields,current_tb=current_tb)


# 表的添加
@rbac_blue.route('/<query_name>/add/')
def query_add(query_name):
    from sqlalchemy.sql.schema import Column
    current_tb = get_current_tb(query_name)
    # dic = current_tb.__dict__
    # for k,v in dic.items():
    #     if isinstance(v,Column):
    #         print('77')
    # for name in current_tb.__dict__:
    return '对%s表进行添加操作' % query_name


# 表的修改
@rbac_blue.route('/<query_name>/edit/<int:nid>/')
def query_edit(query_name, nid):
    print(query_name, nid)
    return '对%s表进行编辑操作' % query_name


# 表的删除
@rbac_blue.route('/<query_name>/del/<int:nid>/')
def query_del(query_name, nid):
    print(query_name, nid)
    return '对%s表进行删除操作' % query_name


# ============admin组件的代码========================
class CustomView(BaseView):  # CustomView相当于是一个蓝图，名字是根据CustomView类取
    """View function of Flask-Admin for Custom page."""

    @expose('/')  # expose用法与blueprint.route一致，当前蓝图下边必须有一个route('/')的路径
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')

from flask_admin.contrib.sqla import ModelView

class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    pass
class MenuModelView(ModelView):
    ''' 处理 Menu 表的类'''
    can_delete = True
 # 是否可以编辑
    page_size = 9                 #
    can_view_details = True       # 是否开启详细视图
    # column_excludes_list = ['']   # 设置不要显示的字段


class PermissionModelView(ModelView):
    can_edit = True
    page_size = 9
    column_list = ['title','url','menu_gp','code','group'] #　要显示的字段
    column_labels = {'title':'url名称','url':'地址','menu_gp':'组内id','code':'code代码','group':'所属分组'}  # 在页面每个字段显示的名字
    column_editable_list = ('title','url','code',)  # 可以直接在视图中编辑的字段
    can_export = True   # 数据导出功能

# ============练习====================


