# !/usr/bin/env python
# coding:utf-8
# author bai

def init_permission(user, request,session):
    # 从数据库中拿到每个url的信息，包括url的
    permission_url_list = []  # 用来存放当前用户每个url的信息

    roles = user.roles
    for role in roles:  # 拿到当前用户的所有的角色
        permissions = role.role_pers  # 拿到当前用户的所有角色的权限,用relations
        for permission in permissions:  # ===这里应该要做一个判断，是否拿到了权限，不然控制没有方法。
            if permission and permission.per_group:
                temp = {}
                temp['permission_menu_id'] = permission.per_group.gp_menu.id  # 权限url所属的菜单id
                temp['permission_menu_title'] = permission.per_group.gp_menu.title  # 权限url所属的菜单title
                temp['permission_gp_id'] = permission.per_group.id  # 权限url所属的分组id
                temp['permission_gp_caption'] = permission.per_group.caption  # 权限url所属的分组caption
                temp['url_title'] = permission.title
                temp['per_url'] = permission.url
                temp['url_code'] = permission.code
                temp['menu_gp'] =permission.menu_gp
                permission_url_list.append(temp)

    # 因为一个用户涉及到多个角色，角色之间的权限url可能存在重复，需要去重
    new_permission_url_list = []
    for permission_url_dic in permission_url_list:
        if permission_url_dic not in new_permission_url_list:
            new_permission_url_list.append(permission_url_dic)
    permission_url_list = new_permission_url_list

    li = [{'permission_menu_id': 1, 'permission_menu_title': '菜单一', 'permission_gp_id': 1, 'permission_gp_caption': '用户信息',
       'url_title': '用户列表', 'per_url': '/userinfo/', 'url_code': 'list'},]

    # 1.页面添加、编辑、删除 显示相关
    # dest_permission_dic = {'1': {'code': [], 'per_url': []}, '2': {'code': [], 'per_url': []}}
    show_per_dic = {}
    for each_dic in permission_url_list:
        if each_dic['permission_gp_id'] in show_per_dic:
            show_per_dic[each_dic['permission_gp_id']]['code'].append(each_dic['url_code'])
            show_per_dic[each_dic['permission_gp_id']]['per_url'].append(each_dic['per_url'])
        else:
            show_per_dic[each_dic['permission_gp_id']] = {'code': [each_dic['url_code'], ],
                                                         'per_url': [each_dic['per_url']]}
    session['show_per_dic'] = show_per_dic


    # 2.页面菜单相关
    # menu_list= [{'menu_id': 1, 'menu_title': '菜单一', 'url_title': '用户列表', 'per_url': '/userinfo/', 'menu_gp': None, 'active': False},]
    menu_list = []
    for dic in permission_url_list:
        if not dic['menu_gp']:
            temp = {}
            temp['menu_id'] = dic['permission_menu_id']
            temp['menu_title'] = dic['permission_menu_title']
            temp['permission__title'] = dic['url_title']
            temp['permission_url'] = dic['per_url']
            temp['permissions__menu_gp'] = dic['menu_gp']
            temp['active'] = False
            menu_list.append(temp)
    session['menu_list'] = menu_list







