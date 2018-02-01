from flask import Flask,request,redirect,render_template,session
from apps.db.db import session_conn   #　链接数据库的session
# from flask_admin import Admin,BaseView,expose  # 用于做后台管理的组件
#
# class CustomView(BaseView):
#     """View function of Flask-Admin for Custom page."""
#
#     @expose('/')
#     def index(self):
#         return self.render('admin/custom.html')
#
#     @expose('/second_page')
#     def second_page(self):
#         return self.render('admin/second_page.html')
