# encoding: utf-8
"""
@author: lileilei
@file: form.py
@time: 2017/7/13 16:42
"""
'''form表单'''
from flask_wtf import Form
from wtforms import StringField, validators, PasswordField, SelectField
from wtforms.validators import Email
from app.models import Work

choice_list = []
work_list = Work.query.all()
choice_l = [(1, '否'), (2, '是')]
for i in range(len(work_list)):
    choice_list.append((work_list[i].id, work_list[i].name))


class LoginFrom(Form):
    username = StringField(u'用户名',
                           [validators.Length(min=4, max=16, message=u'用户名长度在4-16位'), validators.DataRequired()],
                           render_kw={'placeholder': u'请输入用户名'})
    password = PasswordField(u'密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': u'请输入密码'})


class RegFrom(Form):
    username = StringField(u'注册用户名', [validators.Length(min=4, max=16, message=u'用户名长度在4-16位'),
                                      validators.DataRequired(message=u'请输入用户名')], render_kw={'placeholder': u'请输入用户名'})
    password = PasswordField(u'注册密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'),
                                       validators.DataRequired(message=u'请输入密码')], render_kw={'placeholder': u'请输入密码'})
    se_password = PasswordField(u'再次输入密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'),
                                            validators.DataRequired(message=u'请输入确认密码')],
                                render_kw={'placeholder': u'请输入密码'})
    email = StringField(u'输入注册邮箱', [validators.DataRequired(message=u'请输入邮箱'), Email(message=u'邮箱格式不对')],
                        render_kw={'placeholder': u'请输入邮箱'})
    work = SelectField(u'选择职位', choices=choice_list, coerce=int,
                       validators=[validators.DataRequired(message=u"项目名称不能为空")])


class XugaiFrom(Form):
    password = PasswordField(u'密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': u'请输入原密码'})
    xiu_password = PasswordField(u'密码',
                                 [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                                 render_kw={'placeholder': u'请输入新密码'})
    xiu_password_se = PasswordField(u'密码',
                                    [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                                    render_kw={'placeholder': u'请再次输入密码'})


class InterForm(Form):  # 接口的表单
    project_name = StringField(u'项目名字', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口所属项目名称'})
    model_name = StringField(u'模块名字', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口所属模块名称'})
    interface_name = StringField(u'接口名字', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口名称'})
    interface_url = StringField(u'编号', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口url'})
    interface_headers = StringField(u'接口headers', [validators.DataRequired()],
                                    render_kw={'placeholder': u'请输入接口headers'})
    interface_meth = StringField(u'请求方式', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口请求方式'})
    interface_par = StringField(u'请求示例', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口参数示例'})
    interface_bas = StringField(u'请求返回示例', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口返回示例'})


class Interface_yong_Form(Form):  # 测试用例的表单
    yongli_name = StringField(u'项目', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口项目名称'})
    model_name = StringField(u'模块', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口模块名称'})
    interface_name = StringField(u'接口名字', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口名称'})
    interface_url = StringField(u'接口url', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口url'})
    interface_headers = StringField(u'接口headers', [validators.DataRequired()],
                                    render_kw={'placeholder': u'请输入接口headers'})
    interface_meth = StringField(u'请求方式', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口请求方式'})
    interface_can = StringField(u'请求参数', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口请求参数'})
    interface_rest = StringField(u'请求预期', [validators.DataRequired()], render_kw={'placeholder': u'请输入接口预期'})
    save = SelectField(u'选择是否保存测试结果', choices=choice_l, coerce=int)


class Set_email_Form(Form):  # 设置发送邮箱的
    send_email = StringField(u'请输入邮箱', [validators.DataRequired(message=u'请输入邮箱'), Email(message=u'邮箱格式不对')],
                             render_kw={'placeholder': u'请输入邮箱'})
    password = StringField(u'请输入安全密码：', [validators.DataRequired(message=u'请输入安全密码')],
                           render_kw={'placeholder': u'请输入邮箱安全密码'})
    stmp_email = StringField(u'请输入stmp地址：', [validators.DataRequired(message=u'请输入stmp地址：')],
                             render_kw={'placeholder': u'请输入stmp地址：'})
    port = StringField(u'请输入stmp的端口号：', [validators.DataRequired(message=u'请输入stmp的端口号：')],
                       render_kw={'placeholder': u'请输入stmp的端口号：'})


class Interface_Env(Form):  # 测试环境
    project = StringField(u'项目', [validators.DataRequired(message=u'请填写项目')], render_kw={'placeholder': u'请输入接口项目名称'})
    envtion = StringField(u'测试环境url', [validators.DataRequired(message=u'请输入测试环境url')],
                          render_kw={'placeholder': u'测试环境url'})
    desc = StringField(u'测试环境描述', [validators.DataRequired(message=u'请输入测试环境描述')], render_kw={'placeholder': u'测试环境描述'})
