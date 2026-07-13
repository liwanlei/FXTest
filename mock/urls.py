# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:11
from app.mock.views import EditMockServerView, MakeMockserverView, CloseMockView, StartMockView,mock

mock.add_url_rule('/editmockserver/<int:id>', view_func=EditMockServerView.as_view('editmockserver'))
mock.add_url_rule('/mackserver/<string:path>', view_func=MakeMockserverView.as_view('mackserver'))
mock.add_url_rule('/closemock/<int:id>', view_func=CloseMockView.as_view('closemock'))
mock.add_url_rule('/startmock/<int:id>', view_func=StartMockView.as_view('startmock'))
