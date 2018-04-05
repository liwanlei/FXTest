# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
'''主要运行文件，
使用gevent异步请求，'''
from  app import  app
from app import scheduler
from app.home import home
from app.mock import mock
from app.task import task
from app.users import user
from app.case import case
from app.Interface import interfac
from gevent.pywsgi import WSGIServer
import logging
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
scheduler.init_app(app=app)
scheduler.start()
def app_start():
	handler = logging.FileHandler('./log/flask.log', encoding='UTF-8')
	handler.setLevel(logging.INFO)
	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
	handler.setFormatter(logging_format)
#	app.config.from_object('config')
	#scheduler.init_app(app=app)
	#scheduler.start()
	#app.logger.addHandler(handler)
	http_server = WSGIServer(('127.0.0.1', 5000), app)
	http_server.serve_forever()
if __name__ == '__main__':
	app_start()
    #handler = logging.FileHandler('.\log\\flask.log', encoding='UTF-8')
    #handler.setLevel(logging.INFO)
    #logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    #handler.setFormatter(logging_format)
    #app.config.from_object('config')
    #scheduler.init_app(app=app)
    #scheduler.start()
    #app.logger.addHandler(handler)
    #http_server = WSGIServer(('127.0.0.1', 5000), app)
    #http_server.serve_forever()
