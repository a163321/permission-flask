# !/usr/bin/env python
# coding:utf-8
# author bai
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship

engine = create_engine(
    "mysql+pymysql://root:123@127.0.0.1:3306/flask_rbac?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）

)


Base = declarative_base()


class Menu(Base):
    '''页面中的菜单名'''
    __tablename__ = 'menu'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(32),)

    def __str__(self):
        return self.title

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


class Group(Base):
    '''url分组'''
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True,autoincrement=True)
    caption = Column(String(32),)
    menu = Column(Integer,ForeignKey('menu.id',ondelete='CASCADE', onupdate='CASCADE'))

    gp_menu = relationship('Menu',backref='menu_gp')

    def __str__(self):
        return self.caption

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


class User2Role(Base):
    '''用户、角色关系表'''
    __tablename__ = 'user2role'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.id',ondelete='CASCADE', onupdate='CASCADE'))
    role_id = Column(Integer,ForeignKey('role.id',ondelete='CASCADE', onupdate='CASCADE'))

    def __str__(self):
        return 'user_id:%s role_id:%s',(str(self.user_id),str(self.role_id))

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    # 联合唯一，以及索引
    # __table_args = UniqueConstraint(
    #     UniqueConstraint('user_id','role_id',name='user_role'),
    #     Index('user_role','user_id','role_id')
    # )


class Role2Permission(Base):
    '''角色\权限关系表'''
    __tablename__ = 'role2permission'
    id = Column(Integer, primary_key=True,autoincrement=True)
    role_id = Column(Integer,ForeignKey('role.id',ondelete='CASCADE', onupdate='CASCADE'))
    # role_id = Column(Integer,ForeignKey('role.id'))
    permission_id = Column(Integer,ForeignKey('permission.id',ondelete='CASCADE', onupdate='CASCADE'))


    def __str__(self):
        return 'role_id:%s permission_id:%s'%(str(self.role_id),str(self.permission_id))

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

class User(Base):
    '''用户表'''
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(32),)
    password = Column(String(32),)
    email = Column(String(32),)
    # roles与生成表结构无关，仅用于查询方便
    roles = relationship('Role',secondary='user2role',backref='role_users',passive_deletes=True)


    def __str__(self):
        return self.username

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


class Role(Base):
    '''角色表'''
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(32))
    # roles与生成表结构无关，仅用于查询方便
    users = relationship('User',secondary='user2role',backref='user_roles',passive_deletes=True)
    permission = relationship('Permission',secondary='role2permission',backref='per_roles',passive_deletes=True)

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    def __str__(self):
        return self.title

class Permission(Base):
    '''权限表'''
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(32), )
    url = Column(String(32), )
    menu_gp = Column(Integer,ForeignKey('permission.id'),nullable=True,)  # 自关联，当前url在菜单显示的时候的url
    code = Column(String(32), )
    group = Column(Integer,ForeignKey('group.id'))

    # roles与生成表结构无关，仅用于查询方便
    roles = relationship('Role',secondary='role2permission',backref='role_pers',passive_deletes=True)
    per_group = relationship('Group',backref='group_per')     # permission.per_group能拿到当前权限url坐在的group对象
    per_menu_gp = relationship('Permission',remote_side=[id])      # 自关联，记得加remote_side=[id]

    __mapper_args__ = {
        'confirm_deleted_rows': True
    }
    # single_parent=True   # 让级联支持多对多，设置为True
    # passive_deletes = True


    def __str__(self):
        return self.url


if __name__ == '__main__':
    Base.metadata.create_all(engine)




