# encoding: utf-8
"""定时任务、测试结果模型。"""
import datetime
from app import db
from app.models._base import registrations


class Task(db.Model):  # 定时任务的
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    makeuser = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者
    taskname = db.Column(db.String(52))  # 任务名称
    taskstart = db.Column(db.String(252))  # 任务执行时间
    taskmakedate = db.Column(db.DateTime(), default=datetime.datetime.now)  # 任务的创建时间
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
    test_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    hour_time = db.Column(db.Integer())
    test_rep = db.Column(db.String(252))
    test_log = db.Column(db.String(252))
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return str(self.id)


class TestcaseResult(db.Model):  # 测试用例结果
    __tablename__ = 'testcaseresults'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('interfacetests.id'), nullable=True)
    result = db.Column(db.String(252))
    by = db.Column(db.Boolean(), default=False)
    spend = db.Column(db.String(52))
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    testevir = db.Column(db.Integer, db.ForeignKey('ceshihuanjing.id'), nullable=True)

    def __repr__(self):
        return str(self.id)
