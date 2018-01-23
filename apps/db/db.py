# !/usr/bin/env python
# coding:utf-8
# author bai
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/flask_rbac?charset=utf8", max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)

session_conn = Session()