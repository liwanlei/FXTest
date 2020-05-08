# encoding: utf-8
"""
@author: lileilei
@file: models.py
@time: 2017/7/13 16:43
"""
'''数据库'''
from app import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

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
    password = db.Column(db.String(252))
    user_email = db.Column(db.String(64), unique=True)
    jobnum = db.Column(db.Integer())
    status = db.Column(db.Boolean(), default=False)
    is_login = db.Column(db.Boolean(), default=False)
    is_sper = db.Column(db.Boolean(), default=False)
    is_free = db.Column(db.Boolean(), default=False)
    freetime = db.Column(db.DateTime(), default=datetime.datetime.now())
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
    datatime = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __repr__(self):
        return str(self.id)


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
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.Interface_name


class Action(db.Model):
    '''动作'''
    __tablename__ = 'actions'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))
    name = db.Column(db.String(252), unique=True, index=True, nullable=False)
    category = db.Column(db.Integer(), default=0)  # 0前置，1后置
    style = db.Column(db.Integer(), default=0)  # 动作的类型，0是睡眠，1是sql，2.执行测试用例。3执行请求
    sleepnum = db.Column(db.Integer())
    sql = db.Column(db.String(252))
    sqlfiled = db.Column(db.String(252))
    testevent = db.Column(db.Integer(), db.ForeignKey("ceshihuanjing.id"), nullable=True)
    caseid = db.Column(db.Integer())
    requestsurl = db.Column(db.String(252))
    requestsparame = db.Column(db.String(252))
    requestmethod = db.Column(db.String(8))
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return str(self.id)


class GeneralConfiguration(db.Model):
    '''通用配置'''
    __tablename__ = "generalconfigurations"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))
    addtime = db.Column(db.DateTime(), default=datetime.datetime.now())
    name = db.Column(db.String(252), unique=True, index=True, nullable=False)
    style = db.Column(db.Integer(), default=0)  # 通用配置，0 key-value  1，token 2.sql，3.http请求
    key = db.Column(db.String(252))
    token_parame = db.Column(db.String(252))
    token_url = db.Column(db.String(252))
    token_method = db.Column(db.String(16), default="POST")
    sqlurl = db.Column(db.String(252))
    request_url = db.Column(db.String(252))
    request_parame = db.Column(db.String(252))
    request_method = db.Column(db.String(252), default="GET")
    status = db.Column(db.Boolean(), default=False)
    testevent = db.Column(db.Integer(), db.ForeignKey("ceshihuanjing.id"), nullable=True)

    def __repr__(self):
        return str(self.id)


class TestResult(db.Model):  # 测试结果表
    __tablename__ = 'tstresults'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Test_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    test_num = db.Column(db.Integer())
    pass_num = db.Column(db.Integer())
    fail_num = db.Column(db.Integer())
    Exception_num = db.Column(db.Integer())
    can_num = db.Column(db.Integer())
    wei_num = db.Column(db.Integer())
    projects_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    test_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    hour_time = db.Column(db.Integer())
    test_rep = db.Column(db.String(252))
    test_log = db.Column(db.String(252))
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return str(self.id)


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

    def __repr__(self):
        return self.model_name


class EmailReport(db.Model):
    __tablename__ = 'emailReports'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email_re_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    send_email = db.Column(db.String(64))  # 发送邮箱的邮件
    send_email_password = db.Column(db.String(64))  # 发送邮件的密码
    stmp_email = db.Column(db.String(64))  # stmp服务器
    port = db.Column(db.Integer())  # 端口号
    to_email = db.Column(db.String())  # 收件人
    default_set = db.Column(db.Boolean(), default=False)  # 默认
    status = db.Column(db.Boolean(), default=False)  # 状态

    def __repr__(self):
        return self.send_email


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
    databasepassword = db.Column(db.String(32))
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
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 更新时间
    status = db.Column(db.Boolean(), default=False)  # 状态，是否开启
    delete = db.Column(db.Boolean(), default=False)  # 是否删除
    ischeck = db.Column(db.Boolean(), default=False)  # 是否校验参数
    is_headers = db.Column(db.Boolean(), default=False)  # 是否对headers进行校验

    def __repr__(self):
        return self.name


class Task(db.Model):  # 定时任务的
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    makeuser = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者
    taskname = db.Column(db.String(52))  # 任务名称
    taskstart = db.Column(db.String(252))  # 任务执行时间
    taskmakedate = db.Column(db.DateTime(), default=datetime.datetime.now())  # 任务的创建时间
    taskrepor_to = db.Column(db.String(252))  # 收件人邮箱
    taskrepor_cao = db.Column(db.String(252), nullable=True)  # 抄送人邮箱
    task_make_email = db.Column(db.String(252))  # 维护本计划的人的邮箱
    status = db.Column(db.Boolean(), default=False)  # 任务状态，默认正常状态
    yunxing_status = db.Column(db.String(), default=u'创建')  # 任务的运行状态，默认是创建
    prject = db.Column(db.Integer(), db.ForeignKey('projects.id'))  # 任务所属的项目
    testevent = db.Column(db.Integer(), db.ForeignKey('ceshihuanjing.id'))
    interface = db.relationship('InterfaceTest', secondary=registrations,
                                backref=db.backref('tasks'), lazy='dynamic')  # 多对多到测试用例

    def __repr__(self):
        return self.taskname


class Quanxian(db.Model):  # 权限表
    __tablename__ = 'quanxians'
    id = db.Column(db.Integer, primary_key=True)
    rose = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    user = db.relationship('User', secondary=quanxianuser, backref=db.backref('quanxians'),
                           lazy='dynamic')

    def __repr__(self):
        return str(self.id)


class TestcaseResult(db.Model):  # 测试用例结果
    __tablename__ = 'testcaseresults'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('interfacetests.id'), nullable=True)
    result = db.Column(db.String(252))
    date = db.Column(db.DateTime(), default=datetime.datetime.now())
    testevir = db.Column(db.Integer, db.ForeignKey('ceshihuanjing.id'), nullable=True)

    def __repr__(self):
        return str(self.id)


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


class CaseGeneral(db.Model):
    '''测试用例和通用参数关系'''
    __tablename__ = 'casegenerals'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    case = db.Column(db.Integer(), db.ForeignKey("interfacetests.id"))
    general = db.Column(db.Integer(), db.ForeignKey("generalconfigurations.id"))
    filed = db.Column(db.String(252))

    def __repr__(self):
        return str(self.id)


class CaseAction(db.Model):
    '''测试用例和前后动作关系表'''
    __tablename__ = 'caseactions'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    case = db.Column(db.Integer(), db.ForeignKey("interfacetests.id"))
    action = db.Column(db.Integer(), db.ForeignKey("actions.id"))
    actiontype = db.Column(db.Integer(), default=0)
    filed = db.Column(db.String(252))

    def __repr__(self):
        return str(self.id)


class Scenes(db.Model):
    '''测试场景'''
    __tablename__ = 'sceness'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(252), unique=True)
    order = db.Column(db.Integer(), default=0)
    parame = db.Column(db.String(252))
    assertparame = db.Column(db.String(252))
    center = db.Column(db.String(128))
    createtime = db.Column(db.DateTime(), default=datetime.datetime.now())
    desc = db.Column(db.String(128))

    def __repr__(self):
        return self.name


class TestGroup(db.Model):
    '''测试组'''
    __tablename__ = 'testgroup'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(252), unique=True)
    projectid = db.Column(db.Integer())
    status = db.Column(db.Integer(), default=0)  # 状态，0正常，1删除
    adduser = db.Column(db.Integer(), default=0)
    addtime = db.Column(db.Date())
    updateuser = db.Column(db.Integer(), default=adduser)
    updatetime = db.Column(db.Date(), default=datetime.datetime.now())

    def __repr__(self):
        return self.name


class GroupInterface(db.Model):
    '''名单接口'''
    __tablename__ = 'groupinterface'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    testgroupid = db.Column(db.Integer())
    testinterface = db.Column(db.Integer())
    addtime = db.Column(db.Date())
    adduser = db.Column(db.Integer())

    def __repr__(self):
        return str(self.id)


class TestJmx(db.Model):
    "存储测试用例转化的脚本"
    __tablename__ = 'testjmx'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    intefaceid = db.Column(db.Integer())
    runcounttest = db.Column(db.String(252))
    loopcount = db.Column(db.String(252))
    jmxpath = db.Column(db.String(252))
    serverid = db.Column(db.Integer())
    name = db.Column(db.String(252))
    status = db.Column(db.Integer(), default=0)  # 0是创建，1执行中

    def __repr__(self):
        return str(self.id)


class Testerver(db.Model):
    '''测试服务器'''
    __tablename__ = 'testservers'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    ip = db.Column(db.String(252))
    port = db.Column(db.Integer(), default=22)
    loginuser = db.Column(db.String(64), default="root")
    loginpassword = db.Column(db.String(64), default="123456")
    name = db.Column(db.String(64))
    status = db.Column(db.Integer(), default=0)  # 0正常，1删除
    createuser = db.Column(db.Integer(), default=0)
    creatdate = db.Column(db.Date(), default=datetime.datetime.now())
    updateuser = db.Column(db.Integer(), default=createuser)
    updatetime = db.Column(db.Date(), default=datetime.datetime.now())

    def __repr__(self):
        return str(self.name)
