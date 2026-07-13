# encoding: utf-8
"""用户、角色、岗位模型。"""
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models._base import Permisson, quanxianuser


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=True, unique=True)
    default = db.Column(db.Boolean(), default=False)
    permissions = db.Column(db.Integer())
    quanxian = db.relationship('Quanxian', backref='roles')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permisson.ADD | Permisson.EDIT |
                     Permisson.DELETE, True),
            'Oneadmin': (Permisson.ADD | Permisson.EDIT |
                         Permisson.DELETE | Permisson.ONEADMIN, False),
            'Administrator': (0xff, False)}
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Work(db.Model):  # 岗位表
    __tablename__ = 'works'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    user = db.relationship('User', backref='works', lazy='dynamic')

    def __repr__(self):
        return self.name


class User(db.Model):  # 用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(63), unique=True)
    password = db.Column(db.String(512))
    user_email = db.Column(db.String(64), unique=True)
    jobnum = db.Column(db.Integer())
    status = db.Column(db.Boolean(), default=False)
    is_login = db.Column(db.Boolean(), default=False)
    is_sper = db.Column(db.Boolean(), default=False)
    is_free = db.Column(db.Boolean(), default=False)
    freetime = db.Column(db.DateTime(), default=datetime.datetime.now)
    err_num = db.Column(db.Integer(), default=0)
    work_id = db.Column(db.Integer(), db.ForeignKey('works.id'))
    phone = db.relationship('TestResult', backref='users', lazy='dynamic')
    project = db.relationship('Project', backref='users', lazy='dynamic')
    model = db.relationship('Model', backref='users', lazy='dynamic')
    Interface = db.relationship('Interface', backref='users', lazy='dynamic')
    intfacecase = db.relationship('InterfaceTest', backref='users', lazy='dynamic')
    config = db.relationship('GeneralConfiguration', backref='users', lazy='dynamic')
    email = db.relationship('EmailReport', backref='users', lazy='dynamic')
    huanjing = db.relationship('Interfacehuan', backref='users', lazy='dynamic')
    mock = db.relationship('Mockserver', backref='users', lazy='dynamic')
    task = db.relationship('Task', backref='users', lazy='dynamic')
    log = db.relationship('UserLoginlog', backref='users', lazy='dynamic')
    paemase = db.relationship('Parameter', backref='users', lazy='dynamic')

    def __repr__(self):
        return self.username

    def is_administrator(self):
        return self.can(Permisson.ADMIN)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class UserLoginlog(db.Model):
    __tablename__ = 'userloginlog'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))
    ip = db.Column(db.String(252))
    datatime = db.Column(db.DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return str(self.id)


class Quanxian(db.Model):  # 权限表
    __tablename__ = 'quanxians'
    id = db.Column(db.Integer, primary_key=True)
    rose = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    user = db.relationship('User', secondary=quanxianuser, backref=db.backref('quanxians'),
                           lazy='dynamic')

    def __repr__(self):
        return str(self.id)
