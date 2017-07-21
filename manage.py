# encoding: utf-8
"""
@author: lileilei
@file: manage.py
@time: 2017/7/13 16:39g
"""
from  app import  app
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import User,Interface,InterfaceTest,TestResult,db
admin=Admin(app,name=u'api管理后台')
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Interface,db.session))
admin.add_view(ModelView(InterfaceTest,db.session))
admin.add_view(ModelView(TestResult,db.session))
if __name__ == '__main__':
    app.run()
