# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
from  app import  app
from app import scheduler
from app.home import home
from app.mock import  mock
from app.task import  task
from app.users import  user
from app.case import case
from gevent import monkey
from gevent.pywsgi import WSGIServer
import logging
from app.Interface import interfac
app.register_blueprint(home)
app.register_blueprint(mock)
app.register_blueprint(task)
app.register_blueprint(user)
app.register_blueprint(case)
app.register_blueprint(interfac)
from config import Config
if __name__ == '__main__':
    handler = logging.FileHandler('.\log\\flask.log', encoding='UTF-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.config.from_object('config')
    scheduler.init_app(app=app)
    scheduler.start()
    app.logger.addHandler(handler)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
