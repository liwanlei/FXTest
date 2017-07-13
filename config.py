# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: config.py
@time: 2017/7/13 16:39
"""
import  os
class Bease:
    basedir=os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "api.db")
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    SECRET_KEY='leizi'  #hard
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME ='leileili@163.com'
    MAIL_PASSWORD= 'your password'
    POSTS_PER_PAGE=6