# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 9:27
from .views import *
from .views import home
home.add_url_rule('/',view_func=Indexview.as_view('index'))
home.add_url_rule('/login',view_func=LoginView.as_view('login'))
home.add_url_rule('/logt',view_func=LogtView.as_view('logt'))
home.add_url_rule('/interface',view_func=InterfaceView.as_view('interface'))
home.add_url_rule('/interface/<int:page>',view_func=InterfaceView.as_view('interfaspa'))
home.add_url_rule('/yongli',view_func=YongliView.as_view('yongli'))
home.add_url_rule('/yongli/<int:page>',view_func=YongliView.as_view('yonglipage'))
home.add_url_rule('/adminuser',view_func=AdminuserView.as_view('adminuser'))
home.add_url_rule('/adminuser/<int:page>',view_func=AdminuserView.as_view('adminuserpage'))
home.add_url_rule('/project',view_func=ProjectView.as_view('project'))
home.add_url_rule('/model',view_func=ModelView.as_view('model'))
home.add_url_rule('/test_rep',view_func=TestrepView.as_view('test_rep'))
home.add_url_rule('/test_rep/<int:page>',view_func=TestrepView.as_view('test_repppage'))
home.add_url_rule('/ceshihuanjing',view_func=TesteventVies.as_view('ceshihuanjing'))
home.add_url_rule('/mock',view_func=MockViews.as_view('mockserver'))
home.add_url_rule('/timingtask',view_func=TimingtasksView.as_view('timingtask'))
home.add_url_rule('/get_pro_test_report',view_func=GettProtestreport.as_view('get_pro_test_report'))