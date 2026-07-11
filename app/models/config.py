# encoding: utf-8
"""通用配置、邮件、动作模型。"""
import datetime
from app import db


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
    addtime = db.Column(db.DateTime(), default=datetime.datetime.now)
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


class EmailReport(db.Model):
    __tablename__ = 'emailReports'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email_re_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    send_email = db.Column(db.String(64))  # 发送邮箱的邮件
    send_email_password = db.Column(db.String(512))  # 发送邮件的密码
    stmp_email = db.Column(db.String(64))  # stmp服务器
    port = db.Column(db.Integer())  # 端口号
    to_email = db.Column(db.String())  # 收件人
    default_set = db.Column(db.Boolean(), default=False)  # 默认
    status = db.Column(db.Boolean(), default=False)  # 状态

    def __repr__(self):
        return self.send_email


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
