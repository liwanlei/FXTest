# encoding: utf-8
"""
@author: lileilei
@file: config.py
@time: 2017/7/13 16:39
"""
import  os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import  ProcessPoolExecutor
class beijing:
	SECRET_KEY = 'BaSeQuie'
	basedir=os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	CSRF_ENABLED = True
	UPLOAD_FOLDER='/upload'
	DEBUG = True
	@staticmethod
	def init_app(app):
		pass
def lod():
	return beijing
class Config(object):
    JOBS = [ ]
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///shebei.db')
    }
    SCHEDULER_EXECUTORS = {
        'processpool': ProcessPoolExecutor(4)
    }
    SCHEDULER_API_ENABLED = True
