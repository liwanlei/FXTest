# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:11
from app.mock.views import *
mock.add_url_rule('/addmock',view_func=AddmockViews.as_view('addmock'))
mock.add_url_rule('/deletemock/<int:id>',view_func=DeletemockViews.as_view('deletemock'))
mock.add_url_rule('/editmockserver/<int:id>',view_func=EditmockserView.as_view('editmockserver'))
mock.add_url_rule('/mackserver/<string:path>',view_func=MakemockserverView.as_view('mackserver'))
mock.add_url_rule('/closemock/<int:id>',view_func=ClosemockView.as_view('closemock'))
mock.add_url_rule('/startmock/<int:id>',view_func=StartmockView.as_view('startmock'))
mock.add_url_rule('/sermock',view_func=SermockView.as_view('sermock'))