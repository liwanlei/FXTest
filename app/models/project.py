# encoding: utf-8
"""项目、模块模型。"""
from app import db


class Project(db.Model):  # 项目
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_name = db.Column(db.String(252), unique=True)
    TestResult = db.relationship('TestResult', backref='projects', lazy='dynamic')
    Interfacetest = db.relationship('InterfaceTest', backref='projects', lazy='dynamic')
    Interface = db.relationship('Interface', backref='projects', lazy='dynamic')
    Interfacehuan = db.relationship('Interfacehuan', backref='projects', lazy='dynamic')
    task = db.relationship('Task', backref='projects', lazy='dynamic')
    quanxian = db.relationship('Quanxian', backref='projects', lazy='dynamic')
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.project_name


class Model(db.Model):  # 模块，有的接口是根据模块来划分的
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(256))
    model_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    Interfacetest = db.relationship('InterfaceTest', backref='models', lazy='dynamic')
    Interface = db.relationship('Interface', backref='models', lazy='dynamic')
    status = db.Column(db.Boolean(), default=False)
    project = db.Column(db.Integer(), db.ForeignKey('projects.id'))

    def __repr__(self):
        return self.model_name
