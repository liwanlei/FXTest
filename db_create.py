# -*- coding: utf-8 -*-
# @Time    : 2017/7/13 20:53
# @Author  : lileilei
# @File    : db_create.py
'''创建数据库'''
from app import  db
from  app.models import Permisson,Role
def create_roles():#创建角色
    '''创建三个角色，分别是用户，普通管理员，超级管理员'''
    roles={'User':Permisson.DELETE|Permisson.EDIT|Permisson.ADD,
            'Oneadmin':Permisson.DELETE|Permisson.EDIT|Permisson.ADD|Permisson.ONEADMIN,
            'Administrator':Permisson.DELETE|Permisson.EDIT|Permisson.ADD|Permisson.ONEADMIN|Permisson.ADMIN
            }
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role=Role(name=r)
        role.permissions=roles[r]
        db.session.add(role)
    db.session.commit()
if __name__=='__main__':
    # create_roles()
    db.create_all()