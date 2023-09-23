# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:19
from app.task.views import *

task.add_url_rule('/addtimingtasks', view_func=AddTimingTaskView.as_view('addtimingtasks'))
task.add_url_rule('/editmingtask/<int:id>', view_func=EdiTmingTaskView.as_view('editmingtask'))
task.add_url_rule('/deltettask/<int:id>', view_func=DeteleTaskView.as_view('deltettask'))
task.add_url_rule('/testfortask/<int:id>', view_func=TestforTaskView.as_view('testfortask'))
task.add_url_rule('/starttask/<int:id>', view_func=StartTaskView.as_view('starttask'))
task.add_url_rule('/pusedtask/<int:id>', view_func=PausedTaskView.as_view('pusedtask'))
task.add_url_rule('/recivertask/<int:id>', view_func=RecoverTaskView.as_view('recivertask'))
task.add_url_rule('/removetask/<int:id>', view_func=RemoveTaskView.as_view('removetask'))
task.add_url_rule('/getpro', view_func=GetTestView.as_view('getpro'))
task.add_url_rule("/createtaskcaseandrun",view_func=CreateTaskCaseAndRunView.as_view('createtaskcaseandrun'))
