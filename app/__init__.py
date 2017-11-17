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
#from flask_cache import Cache
from flask_bootstrap import  Bootstrap
from flask_login import LoginManager
from config import lod
app=Flask(__name__)
moment=Moment(app)
conf=lod()
loginManager = LoginManager(app)
app.config.from_object(conf)
bootstrap=Bootstrap(app)
loginManager.session_protection = "strong"
loginManager.login_view='login'
db=SQLAlchemy(app)
from  app import  views ,models,url
