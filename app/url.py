# -*- coding: utf-8 -*-
# @Date    : 2017-08-09 20:05:32
# @Author  : lileilei
from app.views import *
from app import app
app.add_url_rule('/load/<string:filename>',view_func=LoadView.as_view('load'))
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