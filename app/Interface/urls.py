""" 
@author: lileilei
@file: urls.py 
@time: 2018/1/31 13:31 
"""
from app.Interface.views import *
from app.Interface import interfac

interfac.add_url_rule('/ser_inter', view_func=SerinterView.as_view('ser_inter'))
interfac.add_url_rule('/daoru_inter', view_func=DaoruinterView.as_view('daoru_inter'))
interfac.add_url_rule('/interfac_edit/<int:id>', view_func=EditInterfaceView.as_view('interfac_edit'))
interfac.add_url_rule('/daochuinterface', view_func=DaochuInterfa.as_view('daochuinterface'))
interfac.add_url_rule('/interface_one/<int:id>', view_func=XiangqingView.as_view('interface_one'))
interfac.add_url_rule('/addprame/<int:id>', view_func=ADdparmsView.as_view('addprame'))
interfac.add_url_rule('/deleteprame/<int:id>', view_func=DeleteParmsView.as_view('deleteprame'))
interfac.add_url_rule('/editeprame/<int:id>&<int:inte_id>', view_func=EditParmsView.as_view('editeprame'))
