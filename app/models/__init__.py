# encoding: utf-8
"""
@author: lileilei
@file: __init__.py
@time: 2017/7/13 16:43
@description: 数据库模型包，统一导出所有模型以保持 from app.models import * 兼容。
"""
from app.models._base import Permisson, registrations, quanxianuser, rely_case
from app.models.user import Role, Work, User, UserLoginlog, Quanxian
from app.models.project import Project, Model
from app.models.interface import (
    Interface, InterfaceTest, Parameter, Interfacehuan, Mockserver,
)
from app.models.task import Task, TestResult, TestcaseResult
from app.models.config import (
    Action, GeneralConfiguration, EmailReport, CaseGeneral, CaseAction,
)
from app.models.test import (
    Scenes, TestGroup, GroupInterface, TestJmx, Testerver,
)

__all__ = [
    'Permisson', 'registrations', 'quanxianuser', 'rely_case',
    'Role', 'Work', 'User', 'UserLoginlog', 'Quanxian',
    'Project', 'Model',
    'Interface', 'InterfaceTest', 'Parameter', 'Interfacehuan', 'Mockserver',
    'Task', 'TestResult', 'TestcaseResult',
    'Action', 'GeneralConfiguration', 'EmailReport', 'CaseGeneral', 'CaseAction',
    'Scenes', 'TestGroup', 'GroupInterface', 'TestJmx', 'Testerver',
]
