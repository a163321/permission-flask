# from .rbac_view import rbac_blue
# from flask import request,session,current_app,redirect,url_for
# import re
# # 伪中间件，用于判断每次请求的
#
# @rbac_blue.before_app_request
# def process_request():
#     print('======================================')
#     current_url = request.path
#     VALID_URL = current_app.config['VALID_URL']
#
#     # 1.白名单验证
#     valid_url = VALID_URL
#     for each in valid_url:
#         if re.match(each, current_url):
#             return None
#
#     # 2.验证是否已经登录
#     permission_dic = session.get('show_per_dic')
#     if not permission_dic:
#         return redirect(url_for('app01_blue.login'))
#
#     # 3.当前访问的url与权限url进行匹配验证,并在request中写入code信息，
#     flag = False
#     for group_id, code_urls in permission_dic.items():
#         for url in code_urls['per_url']:
#             regax = '^{0}$'.format(url)
#             if re.match(regax, current_url):
#                 flag = True
#                 request.permission_code_list = code_urls['code']  # 在session中增加code的信息，用于在页面判断在当前页面的权限，
#                 break
#         if flag:
#             break
#
#     if not flag:
#         return '无权访问'
#
# @rbac_blue.after_app_request
# def process_response(response):
#     return response