# !/usr/bin/env python
# coding:utf-8
# author bai


class BaseConfig(object):
    from apps.rbac.models import Menu,Group,User2Role,Role2Permission,User,Role,Permission
    VALID_URL = ['/app01/login','/static/.*?','/admin/.*?']
    TOTAL_TABLES = [Menu,Group,User2Role,Role2Permission,User,Role,Permission]
    # 配置每张表在页面的显示字段
    CRUD = {
        'User':['title',],
        'Role':['title',],
        'Permission':['title','url','menu_gp','code','group'],
        'User2Role':['user_id','role_id'],
        'Role2Permission':['role_id','permission_id'],
        'Menu':['title',],
        'Group':['caption','menu']
    }



class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass