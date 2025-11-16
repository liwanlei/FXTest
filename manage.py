"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
"""主运行文件，
使用gevent异步请求
"""
from app import app
from app import sched
from app.home import home
from app.mock import mock
from app.task import task
from app.users import user
from app.case import case
from app.Interface import interfaceview
from gevent.pywsgi import WSGIServer
from gevent import monkey
from config import Config


monkey.patch_all()
def register_blueprints():
    app.register_blueprint(home)
    app.register_blueprint(mock)
    app.register_blueprint(task)
    app.register_blueprint(user)
    app.register_blueprint(case)
    app.register_blueprint(interfaceview)



def app_start():
    app.config.from_object('config')
    sched.start()
    register_blueprints()
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    app_start()
    # app.run(debug=True, port=5002)
