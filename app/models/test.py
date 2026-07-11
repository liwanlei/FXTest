# encoding: utf-8
"""测试场景、测试组、JMX、测试服务器模型。"""
import datetime
from app import db


class Scenes(db.Model):
    '''测试场景'''
    __tablename__ = 'sceness'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(252), unique=True)
    order = db.Column(db.Integer(), default=0)
    parame = db.Column(db.String(252))
    assertparame = db.Column(db.String(252))
    center = db.Column(db.String(128))
    createtime = db.Column(db.DateTime(), default=datetime.datetime.now)
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
    updatetime = db.Column(db.Date(), default=datetime.datetime.now)

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
    creatdate = db.Column(db.Date(), default=datetime.datetime.now)
    updateuser = db.Column(db.Integer(), default=createuser)
    updatetime = db.Column(db.Date(), default=datetime.datetime.now)
    is_run = db.Column(db.Integer(), default=0)  # 默认是没有执行

    def __repr__(self):
        return self.name
