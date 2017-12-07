# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:24
from app.users.views import *
user.add_url_rule('/seting',view_func=Set_emaiView.as_view('setting'))
user.add_url_rule('/add_emai',view_func=Add_emaiView.as_view('add_emai'))
user.add_url_rule('/delemail/<int:id>',view_func=DeleteView.as_view('delemail'))
user.add_url_rule('/editemail/<int:id>',view_func=EditemailView.as_view('editemail'))
user.add_url_rule('/quzhi/<int:id>',view_func=QuzhiMoView.as_view('quzhi'))
user.add_url_rule('/shezhi/<int:id>',view_func=ShezhiMoView.as_view('shezhi'))
user.add_url_rule('/add_user',view_func=AdduserView.as_view('add_user'))
user.add_url_rule('/set_ad/<int:id>',view_func=SetadView.as_view('set_ad'))
user.add_url_rule('/del_ad/<int:id>',view_func=DeladView.as_view('del_ad'))
user.add_url_rule('/fre_ad/<int:id>',view_func=FreadView.as_view('fre_ad'))
user.add_url_rule('/fre_re/<int:id>',view_func=FrereView.as_view('fre_re'))
user.add_url_rule('/red_pass/<int:id>',view_func=RedpassView.as_view('red_pass'))
user.add_url_rule('/ser_user',view_func=SeruserView.as_view('ser_user'))