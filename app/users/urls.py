# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : urls.py
# @Time    : 2017/12/7 12:24
from app.users.views import *

user.add_url_rule('/setadmin', view_func=SetAdminView.as_view('setadmin'))
user.add_url_rule('/canceladmin/<int:id>', view_func=CancelAdminView.as_view('canceladmin'))
user.add_url_rule('/freezeuser/<int:id>', view_func=FreezeUserView.as_view('freezeuser'))
user.add_url_rule('/unfreezeuser/<int:id>', view_func=UnFreezeUserView.as_view('unfreezeuser'))
user.add_url_rule('/resetpassword/<int:id>', view_func=ResetPasswordView.as_view('resetpassword'))
user.add_url_rule('/changepassword', view_func=ChangePassword.as_view('changepassword'))
user.add_url_rule("/activationuser", view_func=ActivationUserview.as_view('activationuser'))
