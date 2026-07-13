# encoding: utf-8
"""接口、测试用例、参数、环境、Mock 模型。"""
import datetime
from app import db
from app.models._base import rely_case


class Interface(db.Model):  # 接口表
    __tablename__ = 'interfaces'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'))
    projects_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    Interface_name = db.Column(db.String(252))
    Interface_url = db.Column(db.String(252))
    Interface_meth = db.Column(db.String(252), default='GET')
    Interface_headers = db.Column(db.String(252))
    Interface_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    interfacetype = db.Column(db.String(32), default='http')
    interfacetests = db.relationship('InterfaceTest', backref='interfaces', lazy='dynamic')
    interfapar = db.relationship('Parameter', backref='interfaces', lazy='dynamic')
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.Interface_name


class InterfaceTest(db.Model):  # 测试用例表
    __tablename__ = 'interfacetests'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'))
    projects_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    interface_id = db.Column(db.Integer(), db.ForeignKey('interfaces.id'))
    bian_num = db.Column(db.String(252))
    interface_type = db.Column(db.String(16))
    Interface_name = db.Column(db.String(252))
    Interface_url = db.Column(db.String(252))
    Interface_meth = db.Column(db.String(252))
    Interface_pase = db.Column(db.String(252))
    Interface_assert = db.Column(db.String(252))
    Interface_headers = db.Column(db.String(252))
    pid = db.Column(db.Integer(), db.ForeignKey('interfacetests.id'), nullable=True)
    getattr_p = db.Column(db.String(252), nullable=True)
    rely = db.relationship('InterfaceTest', secondary=rely_case,
                           primaryjoin=(rely_case.c.case_id == id),
                           secondaryjoin=(rely_case.c.cases_id == id),
                           backref=db.backref('interfacetests',
                                              lazy='dynamic'), lazy='dynamic')
    Interface_is_tiaoshi = db.Column(db.Boolean(), default=False)
    Interface_tiaoshi_shifou = db.Column(db.Boolean(), default=True, nullable=True)
    Interface_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    saveresult = db.Column(db.Boolean(), default=False)
    is_database = db.Column(db.Boolean(), default=False)
    chaxunshujuku = db.Column(db.String(252), nullable=True)
    databaseziduan = db.Column(db.String(252), nullable=True)
    testcaseresult = db.relationship('TestcaseResult',
                                     backref='interfacetests', lazy='dynamic')
    is_ci = db.Column(db.Boolean(), default=False)
    is_smoke = db.Column(db.Integer(), default=0)  # 0 否 1是
    is_reback = db.Column(db.Integer(), default=0)  # 0 否 1是
    is_monitor = db.Column(db.Integer(), default=0)  # 1 监控用例
    status = db.Column(db.Boolean(), default=False)  # 是否删除

    def __repr__(self):
        return self.Interface_name


class Parameter(db.Model):  # 参数
    __tablename__ = 'parames'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_id = db.Column(db.Integer, db.ForeignKey("interfaces.id"))  # 接口id
    parameter_type = db.Column(db.String(64))  # 参数类型
    parameter_name = db.Column(db.String(64))  # 参数名字
    necessary = db.Column(db.Boolean(), default=False)  # 是否必须
    type = db.Column(db.Integer(), default=0)  # 类型,返回还是传参，入参为0  出参为1
    status = db.Column(db.Boolean(), default=False)  # 状态
    default = db.Column(db.String(63))  # 示例
    desc = db.Column(db.String(252))  # 参数描述
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return str(self.id)


class Interfacehuan(db.Model):  # 测试环境
    __tablename__ = 'ceshihuanjing'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    make_user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    url = db.Column(db.String(252))  # 地址
    desc = db.Column(db.String(252))  # 描述
    database = db.Column(db.String(252))  # 数据库
    dbport = db.Column(db.String(252))  # 数据库服务端口号
    dbhost = db.Column(db.String(252))  # 数据库主机
    databaseuser = db.Column(db.String(32))
    databasepassword = db.Column(db.String(512))
    project = db.Column(db.Integer(), db.ForeignKey('projects.id'))  # 环境对应的项目
    status = db.Column(db.Boolean(), default=False)  # 状态
    testcaseresult = db.relationship('TestcaseResult', backref='ceshihuanjing',
                                     lazy='dynamic')
    task = db.relationship('Task', backref='ceshihuanjing',
                           lazy='dynamic')

    def __repr__(self):
        return str(self.id)


class Mockserver(db.Model):  # mocksever
    __tablename__ = 'mockserver'
    id = db.Column(db.Integer, primary_key=True)
    make_uers = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建人
    name = db.Column(db.String(55))  # 名字
    path = db.Column(db.String(252))  # 路径
    methods = db.Column(db.String(50))  # 方法
    headers = db.Column(db.String(500))  # 请求头
    description = db.Column(db.String(50))  # 描述
    fanhui = db.Column(db.String(500))  # 返回数据
    params = db.Column(db.String(500))  # 参数
    rebacktype = db.Column(db.String(32))  # 类型，
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now)  # 更新时间
    status = db.Column(db.Boolean(), default=False)  # 状态，是否开启
    delete = db.Column(db.Boolean(), default=False)  # 是否删除
    ischeck = db.Column(db.Boolean(), default=False)  # 是否校验参数
    is_headers = db.Column(db.Boolean(), default=False)  # 是否对headers进行校验

    def __repr__(self):
        return self.name
