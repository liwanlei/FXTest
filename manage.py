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
app.register_blueprint(home)
app.register_blueprint(mock)
app.register_blueprint(task)
app.register_blueprint(user)
from config import Config
if __name__ == '__main__':
    app.config.from_object('config')
    scheduler.init_app(app=app)
    scheduler.start()
    app.run()
