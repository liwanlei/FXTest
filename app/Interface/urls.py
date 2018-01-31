""" 
@author: lileilei
@file: urls.py 
@time: 2018/1/31 13:31 
"""
from app.Interface.views import *
from app.Interface import interfac
interfac.add_url_rule('/ser_inter',view_func=SerinterView.as_view('ser_inter'))
interfac.add_url_rule('/daoru_inter',view_func=DaoruinterView.as_view('daoru_inter'))
interfac.add_url_rule('/interface_add',view_func=InterfaceaddView.as_view('interface_add'))
interfac.add_url_rule('/interfac_edit/<int:id>',view_func=EditInterfaceView.as_view('interfac_edit'))
interfac.add_url_rule('/dele_inter/<int:id>',view_func=DeleinterView.as_view('dele_inter'))