""" 
@author: lileilei
@file: urls.py 
@time: 2018/1/31 13:20 
"""
from app.case.views import *
from app.case import case
case.add_url_rule('/addtestcase',view_func=AddtestcaseView.as_view('addtestcase'))
case.add_url_rule('/delete_case/<int:id>',view_func=Deletecase.as_view('delete_case'))
case.add_url_rule('/edit_case/<int:id>',view_func=EditcaseView.as_view('edit_case'))
case.add_url_rule('/daoru_case',view_func=DaorucaseView.as_view('daoru_case'))
case.add_url_rule('/ser_yongli',view_func=SeryongliView.as_view('ser_yongli'))
case.add_url_rule('/makeonlyonecase',view_func=MakeonlyoneCase.as_view('makeonlyonecase'))#这里是加测试环境的需求的单个接口测试的url
case.add_url_rule('/make_one_case/<int:id>',view_func=MakeonecaseView.as_view('make_one_case'))
case.add_url_rule('/duoyongli',view_func=DuoyongliView.as_view('duoyongli'))
case.add_url_rule('/daochucase',view_func=DaochuCase.as_view('daochucase'))