# -*- coding: utf-8 -*-
# @Date    : 2017-08-14 20:58:13
# @Author  : lileilei
from functools import wraps
from flask import abort
from flask_login import current_user
def chckuserpermisson():
    for rosse in current_user.quanxians:
        if rosse.rose!=2  or current_user.is_sper !=0 :
            return  False
        else:
            return  True

