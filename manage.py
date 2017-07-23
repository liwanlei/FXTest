# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39g
"""
from  app import  app
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import User,Interface,InterfaceTest,TestResult,db
if __name__ == '__main__':
    app.run()
