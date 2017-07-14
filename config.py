# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: config.py
@time: 2017/7/13 16:39
"""
import  os
class beijing:
	SECRET_KEY = 'BaSeQuie'
	basedir=os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	CSRF_ENABLED = True
	DEBUG = True
	@staticmethod
	def init_app(app):
		pass
def lod():
	return beijing