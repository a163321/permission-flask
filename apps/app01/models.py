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


class Book(Base):
    __tablename__='book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), )


if __name__ == '__main__':
    Base.metadata.create_all(engine)