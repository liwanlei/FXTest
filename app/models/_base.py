# encoding: utf-8
"""模型基础：辅助表与权限常量。"""
from app import db

# 多对多辅助表
registrations = db.Table('registrations', db.Column('task_id', db.Integer(),
                                                    db.ForeignKey('tasks.id')),
                         db.Column('interfacetests_id', db.Integer()
                                   , db.ForeignKey('interfacetests.id')))
quanxianuser = db.Table('quanxianusers', db.Column('user_id', db.Integer(),
                                                   db.ForeignKey('users.id')),
                        db.Column('quanxians_id', db.Integer(),
                                  db.ForeignKey('quanxians.id')))
rely_case = db.Table('yilai',
                     db.Column('case_id', db.Integer(),
                               db.ForeignKey('interfacetests.id')),
                     db.Column('cases_id', db.Integer(),
                               db.ForeignKey('interfacetests.id')),
                     db.Column('attred', db.String()))


class Permisson:
    ADD = 0x01
    EDIT = 0x02
    DELETE = 0x04
    ONEADMIN = 0x08
    ADMIN = 0xff
