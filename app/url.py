# -*- coding: utf-8 -*-
# @Date    : 2017-08-09 20:05:32
# @Author  : lileilei
from app.views import *
from app import app
app.add_url_rule('/interface_add',view_func=InterfaceaddView.as_view('interface_add'))
app.add_url_rule('/interfac_edit/<int:id>',view_func=EditInterfaceView.as_view('interfac_edit'))
app.add_url_rule('/dele_inter/<int:id>',view_func=DeleinterView.as_view('dele_inter'))
app.add_url_rule('/addtestcase',view_func=AddtestcaseView.as_view('addtestcase'))
app.add_url_rule('/delete_case/<int:id>',view_func=Deletecase.as_view('delete_case'))
app.add_url_rule('/edit_case/<int:id>',view_func=EditcaseView.as_view('edit_case'))
app.add_url_rule('/daoru_inter',view_func=DaoruinterView.as_view('daoru_inter'))
app.add_url_rule('/daoru_case',view_func=DaorucaseView.as_view('daoru_case'))
app.add_url_rule('/ser_yongli',view_func=SeryongliView.as_view('ser_yongli'))
app.add_url_rule('/ser_inter',view_func=SerinterView.as_view('ser_inter'))
app.add_url_rule('/load/<string:filename>',view_func=LoadView.as_view('load'))
app.add_url_rule('/make_one_case/<int:id>',view_func=MakeonecaseView.as_view('make_one_case'))
app.add_url_rule('/duoyongli',view_func=DuoyongliView.as_view('duoyongli'))
app.add_url_rule('/add_moel',view_func=AddmodelView.as_view('add_moel'))
app.add_url_rule('/add_pro',view_func=AddproView.as_view('add_pro'))
app.add_url_rule('/dele_moel/<int:id>',view_func=DelemodelView.as_view('dele_moel'))
app.add_url_rule('/dele_pro/<int:id>',view_func=DeleproView.as_view('dele_pro'))
app.add_url_rule('/edit_moel/<int:id>',view_func=EditmoelView.as_view('edit_moel'))
app.add_url_rule('/edit_pro/<int:id>',view_func=EditproView.as_view('edit_pro'))
app.add_url_rule('/deletre/<int:id>',view_func=DeleteResultView.as_view('deletre'))
app.add_url_rule('/addevent',view_func=ADDTesteventView.as_view('addevent'))
app.add_url_rule('/deleteevent/<int:id>',view_func=DeleteEventViews.as_view('delete'))
app.add_url_rule('/editevent/<int:id>',view_func=EditEventViews.as_view('editevents'))
app.add_url_rule('/makeonlyonecase',view_func=MakeonlyoneCase.as_view('makeonlyonecase'))#这里是加测试环境的需求的单个接口测试的url
