# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: __init__.py.py
@time: 2017/7/13 16:38
"""
from  flask import  Flask
from  flask_sqlalchemy import  SQLAlchemy
from flask_bootstrap import  Bootstrap
from flask_login import LoginManager
from config import lod
from flask_apscheduler import  APScheduler
from flask_admin import  Admin
app=Flask(__name__)
conf=lod()
loginManager = LoginManager(app)
app.config.from_object(conf)
bootstrap=Bootstrap(app)
loginManager.session_protection = "strong"
loginManager.login_view='home.login'
loginManager.login_message=u'FXTest测试平台必须登录，请登录您的FXTest平台账号！'
db=SQLAlchemy(app)
scheduler=APScheduler()
admin=Admin(app,name=u'FXTest系统管理后台')
from  app import  views ,models,url,apiadmin