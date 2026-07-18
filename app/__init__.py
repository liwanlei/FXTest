# encoding: utf-8
"""
@author: lileilei
@site: 
@file: __init__.py
@time: 2017/7/13 16:38
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import lod
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from config import jobstores, executors
from flask_admin import Admin
from common.system_log import logger

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

app = Flask(__name__)
conf = lod()
app.config.from_object(conf)
loginManager = LoginManager(app)
bootstrap = Bootstrap(app)
loginManager.session_protection = None
loginManager.login_view = 'home.login'
loginManager.login_message = u'FXTest测试平台必须登录，请登录您的FXTest平台账号！'
db = SQLAlchemy(app)
admin = Admin(app, name=u'FXTest系统管理后台')
from app.models import Work
from app import views, models, urls, admin_views


def listerner(event):
    if event.exception:
        logger.error('任务出错了！')
    else:
        logger.info('任务正常运行中...')


sched = BackgroundScheduler(jobstores=jobstores, executors=executors)
sched.add_listener(listerner, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
choice_l = [(1, '否'), (2, '是')]
work_choices = []


def init_work_choices():
    global work_choices
    work_list = Work.query.all()
    work_choices = [(w.id, w.name) for w in work_list]
