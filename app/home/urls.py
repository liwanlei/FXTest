# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 9:27
from .views import *
from .views import home

home.add_url_rule('/index', view_func=index.as_view('index'))
home.add_url_rule('/login', view_func=LoginView.as_view('login'))
home.add_url_rule('/logout', view_func=Logout.as_view('logout'))
home.add_url_rule('/interface', view_func=InterfaceView.as_view('interface'))
home.add_url_rule('/interface/<int:page>', view_func=InterfaceView.as_view('interfaspa'))
home.add_url_rule('/yongli', view_func=YongliView.as_view('yongli'))
home.add_url_rule('/yongli/<int:page>', view_func=YongliView.as_view('yonglipage'))
home.add_url_rule('/adminuser', view_func=AdminuserView.as_view('adminuser'))
home.add_url_rule('/adminuser/<int:page>', view_func=AdminuserView.as_view('adminuserpage'))
home.add_url_rule('/project', view_func=ProjectView.as_view('project'))
home.add_url_rule('/project/<int:page>', view_func=ProjectView.as_view('projectpage'))
home.add_url_rule('/model', view_func=ModelView.as_view('model'))
home.add_url_rule('/model/<int:page>', view_func=ModelView.as_view('models'))
home.add_url_rule('/test_rep', view_func=TestrepView.as_view('test_rep'))
home.add_url_rule('/test_rep/<int:page>', view_func=TestrepView.as_view('test_repppage'))
home.add_url_rule('/ceshihuanjing', view_func=TesteventVies.as_view('ceshihuanjing'))
home.add_url_rule('/ceshihuanjing/<int:page>', view_func=TesteventVies.as_view('ceshihuanjings'))
home.add_url_rule('/mock', view_func=MockViews.as_view('mockserver'))
home.add_url_rule('/mock/<int:page>', view_func=MockViews.as_view('mockservers'))
home.add_url_rule('/timingtask', view_func=TimingtasksView.as_view('timingtask'))
home.add_url_rule('/timingtask/<int:page>', view_func=TimingtasksView.as_view('timingtasks'))
home.add_url_rule('/get_pro_test_report', view_func=GettProtestreport.as_view('get_pro_test_report'))
home.add_url_rule('/jenkinsfirst', view_func=JenkinsFirst.as_view('jenkinsfirst'))
home.add_url_rule('/buildjob/<jobname>', view_func=JenkinsGou.as_view('buildjob'))
home.add_url_rule('/getjenlog', view_func=GetJenLogview.as_view('get_jen_log'))
home.add_url_rule('/deletejentask/<int:id>', view_func=DeleteJenkinstask.as_view('deletejentask'))
home.add_url_rule('/deletegenconfig/<int:id>', view_func=DeleteGenconfi.as_view('deletegenconfig'))
home.add_url_rule('/genconfig', view_func=GenconfigView.as_view('genconfig'))
home.add_url_rule('/genconfig/<int:page>', view_func=GenconfigView.as_view('genconfigs'))
