# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
'''主运行文件，
使用gevent异步请求，'''
from  app import  app
from flask import Blueprint
from flask_restplus import Api
from app import sched
from app.home import home
from app.mock import mock
from app.task import task
from app.users import user
from app.case import case
from app.Interface import interfac
from gevent.pywsgi import WSGIServer
from gevent import  monkey
monkey.patch_all()
app.register_blueprint(home)
app.register_blueprint(mock)
app.register_blueprint(task)
app.register_blueprint(user)
app.register_blueprint(case)
app.register_blueprint(interfac)
from config import Config
app.config.from_object('config')
def app_start():
	sched.start()
	http_server = WSGIServer(('127.0.0.1', 5000), app)
	http_server.serve_forever()
if __name__ == '__main__':
	#app_start()
	app.run(debug=True,port=5002)