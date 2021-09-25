# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 9:27
from .views import *
from .views import home

home.add_url_rule('/index', view_func=IndexView.as_view('index'))
home.add_url_rule('/login', view_func=LoginView.as_view('login'))
home.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
home.add_url_rule('/interface', view_func=InterfaceView.as_view('interface'))
home.add_url_rule('/interface/<int:page>', view_func=InterfaceView.as_view('interfaspa'))
home.add_url_rule('/case', view_func=CaseView.as_view('case'))
home.add_url_rule('/case/<int:page>', view_func=CaseView.as_view('casepage'))
home.add_url_rule('/adminuser', view_func=AdminUserView.as_view('adminuser'))
home.add_url_rule('/adminuser/<int:page>', view_func=AdminUserView.as_view('adminuserpage'))
home.add_url_rule('/project', view_func=ProjectView.as_view('project'))
home.add_url_rule('/project/<int:page>', view_func=ProjectView.as_view('projectpage'))
home.add_url_rule('/model', view_func=ModelView.as_view('model'))
home.add_url_rule('/model/<int:page>', view_func=ModelView.as_view('models'))
home.add_url_rule('/test_result', view_func=TestResultView.as_view('test_result'))
home.add_url_rule('/test_result/<int:page>', view_func=TestResultView.as_view('test_repppage'))
home.add_url_rule('/testenvironment', view_func=TestenvironmentView.as_view('testenvironment'))
home.add_url_rule('/testenvironment/<int:page>', view_func=TestenvironmentView.as_view('testenvironmenta'))
home.add_url_rule('/mock', view_func=MockViews.as_view('mockserver'))
home.add_url_rule('/mock/<int:page>', view_func=MockViews.as_view('mockservers'))
home.add_url_rule('/timingtask', view_func=TimingtasksView.as_view('timingtask'))
home.add_url_rule('/timingtask/<int:page>', view_func=TimingtasksView.as_view('timingtasks'))
home.add_url_rule('/get_project_test_report', view_func=GetProtestReportView.as_view('get_project_test_report'))
# home.add_url_rule('/jenkinsfirst', view_func=JenkinsFirst.as_view('jenkinsfirst'))
# home.add_url_rule('/buildjob/<jobname>', view_func=JenkinsGou.as_view('buildjob'))
# home.add_url_rule('/getjenlog', view_func=GetJenLogview.as_view('get_jen_log'))
# home.add_url_rule('/deletejentask/<int:id>', view_func=DeleteJenkinstask.as_view('deletejentask'))
home.add_url_rule('/deletegenconfig/<int:id>', view_func=DeleteGenconfigView.as_view('deletegenconfig'))
home.add_url_rule('/genconfig', view_func=GenconfigView.as_view('genconfig'))
home.add_url_rule('/genconfig/<int:page>', view_func=GenconfigView.as_view('genconfigs'))
