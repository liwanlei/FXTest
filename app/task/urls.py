# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:19
from app.task.views import *

task.add_url_rule('/addtimingtasks', view_func=AddtimingtaskView.as_view('addtimingtasks'))
task.add_url_rule('/editmingtask/<int:id>', view_func=Editmingtaskview.as_view('editmingtask'))
task.add_url_rule('/deltettask/<int:id>', view_func=DeteleTaskViee.as_view('deltettask'))
task.add_url_rule('/testfortask/<int:id>', view_func=TestforTaskView.as_view('testfortask'))
task.add_url_rule('/starttask/<int:id>', view_func=StartTaskView.as_view('starttask'))
task.add_url_rule('/zantingtask/<int:id>', view_func=ZantingtaskView.as_view('zantingtask'))
task.add_url_rule('/huifutask/<int:id>', view_func=HuifutaskView.as_view('huifutask'))
task.add_url_rule('/yichutask/<int:id>', view_func=YichuTaskView.as_view('yichutask'))
task.add_url_rule('/getpro', view_func=GettesView.as_view('getpro'))
