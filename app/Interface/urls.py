""" 
@author: lileilei
@file: urls.py 
@time: 2018/1/31 13:31 
"""
from app.Interface.views import *
from app.Interface import interfaceview

interfaceview.add_url_rule('/ser_inter', view_func=SerinterView.as_view('ser_inter'))
interfaceview.add_url_rule('/import_interface', view_func=ImportInterfaceView.as_view('import_inter'))
interfaceview.add_url_rule('/interfac_edit/<int:id>', view_func=EditInterfaceView.as_view('interfac_edit'))
interfaceview.add_url_rule('/exportinterface', view_func=ExportinterfaceInterfceView.as_view('import_interface'))
interfaceview.add_url_rule('/interface_detail/<int:id>', view_func=DetailView.as_view('interface_detail'))
interfaceview.add_url_rule('/addprame/<int:id>', view_func=AddParameterView.as_view('addprame'))
interfaceview.add_url_rule('/deleteprame/<int:id>', view_func=DeleteParameterView.as_view('deleteprame'))
interfaceview.add_url_rule('/editeprame/<int:id>&<int:inte_id>', view_func=EditPParameterView.as_view('editeprame'))
