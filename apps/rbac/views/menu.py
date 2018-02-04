import re
from flask import request, session

from apps.db.db import session_conn  # 用于sqlalchemy连接
from apps.rbac.models import Permission


# 菜单的内容,在需要的地方调用，就可以生成菜单需要的数据
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

# 菜单页面的显示相关
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