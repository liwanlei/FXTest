# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
from  app import  app
from app import scheduler
from config import Config
if __name__ == '__main__':
    app.config.from_object('config')
    scheduler.init_app(app=app)
    scheduler.start()
    app.run()
