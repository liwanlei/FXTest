# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:24
from app.users.views import *

user.add_url_rule('/set_ad', view_func=SetadView.as_view('set_ad'))
user.add_url_rule('/del_ad/<int:id>', view_func=DeladView.as_view('del_ad'))
user.add_url_rule('/fre_ad/<int:id>', view_func=FreadView.as_view('fre_ad'))
user.add_url_rule('/fre_re/<int:id>', view_func=FrereView.as_view('fre_re'))
user.add_url_rule('/red_pass/<int:id>', view_func=RedpassView.as_view('red_pass'))
user.add_url_rule('/changepassword', view_func=ChangePassword.as_view('changepassword'))
user.add_url_rule("/activi", view_func=Acivauserview.as_view('activi'))
