# !/usr/bin/env python
# coding:utf-8
# author bai

class BaseConfig(object):
    VALID_URL = ['/app01/login','/static/.*?']


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass