# !/usr/bin/env python
# coding:utf-8
# author bai


class BaseConfig(object):
    from apps.rbac.models import Menu,Group,User2Role,Role2Permission,User,Role,Permission
    VALID_URL = ['/app01/login','/static/.*?']
    TOTAL_TABLES = [Menu,Group,User2Role,Role2Permission,User,Role,Permission]


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass