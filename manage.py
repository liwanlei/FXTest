"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39
"""
"""主运行文件 使用gevent异步请求"""
from dotenv import load_dotenv
load_dotenv()

from app import app
from app import sched
from app import init_work_choices
from app.home import home
from app.mock import mock
from app.task import task
from app.users import user
from app.case import case
from app.interface import interfaceview
from gevent.pywsgi import WSGIServer
from gevent import monkey


monkey.patch_all()
def register_blueprints():
    app.register_blueprint(home)
    app.register_blueprint(mock)
    app.register_blueprint(task)
    app.register_blueprint(user)
    app.register_blueprint(case)
    app.register_blueprint(interfaceview)



def app_start():
    register_blueprints()
    init_work_choices()
    sched.start()
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    app_start()
    # app.run(debug=True, port=5002)
