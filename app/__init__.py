# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: __init__.py.py
@time: 2017/7/13 16:38
"""
from  flask import  Flask
from flask_admin import  Admin,AdminIndexView
from  flask_sqlalchemy import  SQLAlchemy
from flask_login import  LoginManager
from flask_moment import  Moment
from flask_bootstrap import  Bootstrap
app=Flask(__name__)
db=SQLAlchemy(app)
moment=Moment(app)
bootstrap=Bootstrap(app)
from  app import  views ,models