# -*- coding: utf-8 -*-
# @Date    : 2017-08-14 20:58:13
# @Author  : lileilei
'''
判断是否是管理员
'''
from flask_login import current_user
def chckuserpermisson():
    for rosse in current_user.quanxians:
        if int(rosse.rose)==2  or current_user.is_sper ==1:
            return  True
        else:
            return  False