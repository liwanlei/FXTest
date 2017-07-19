# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: form.py
@time: 2017/7/13 16:42
"""
from flask_wtf import  Form
from wtforms import  StringField,SubmitField,DateTimeField,validators,IntegerField,FileField,PasswordField
class LoginFrom(Form):
    username=StringField('用户名',[validators.Length(min=4, max=16,message='用户名长度在4-16位'),validators.DataRequired()],render_kw={'placeholder':'请输入用户名'})
    password=PasswordField('密码',[validators.length(min=8,max=16,message='密码长度8-16位'),validators.DataRequired()],render_kw={'placeholder':'请输入密码'})
class RegFrom(Form):
    username = StringField('注册用户名', [validators.Length(min=4, max=16, message='用户名长度在4-16位'), validators.DataRequired()],render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('注册密码', [validators.length(min=8, max=16, message='密码长度8-16位'), validators.DataRequired()],render_kw={'placeholder': '请输入密码'})
    se_password = PasswordField('再次输入密码', [validators.length(min=8, max=16, message='密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': '请输入密码'})
    email=StringField('输入注册邮箱', [validators.Length(min=4, max=16, message='邮箱输入错误'), validators.DataRequired()],
                           render_kw={'placeholder': '请输入邮箱'})
class XugaiFrom(Form):
    password = PasswordField('密码', [validators.length(min=8, max=16, message='密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': '请输入原密码'})
    xiu_password = PasswordField('密码',
                                [validators.length(min=8, max=16, message='密码长度8-16位'), validators.DataRequired()],
                                render_kw={'placeholder': '请输入新密码'})
    xiu_password_se = PasswordField('密码',
                                 [validators.length(min=8, max=16, message='密码长度8-16位'), validators.DataRequired()],
                                 render_kw={'placeholder': '请再次输入密码'})
class InterForm(Form):
    project_name=StringField('项目名字', [validators.DataRequired()],render_kw={'placeholder': '请输入接口所属项目名称'})
    model_name=StringField('模块名字', [validators.DataRequired()],render_kw={'placeholder': '请输入接口所属模块名称'})
    interface_name=StringField('接口名字', [validators.DataRequired()],render_kw={'placeholder': '请输入接口名称'})
    interface_url=StringField('接口url', [validators.DataRequired()],render_kw={'placeholder': '请输入接口url'})
    interface_meth=StringField('请求方式', [validators.DataRequired()],render_kw={'placeholder': '请输入接口请求方式'})
    interface_par = StringField('请求示例', [validators.DataRequired()], render_kw={'placeholder': '请输入接口参数示例'})
    interface_bas= StringField('请求返回示例', [validators.DataRequired()], render_kw={'placeholder': '请输入接口返回示例'})
class Interface_yong_Form(Form):
    yongli_name=StringField('项目', [validators.DataRequired()],render_kw={'placeholder': '请输入接口项目名称'})
    model_name=StringField('模块', [validators.DataRequired()],render_kw={'placeholder': '请输入接口模块名称'})
    interface_name = StringField('接口名字', [validators.DataRequired()], render_kw={'placeholder': '请输入接口名称'})
    interface_url = StringField('接口url', [validators.DataRequired()], render_kw={'placeholder': '请输入接口url'})
    interface_meth = StringField('请求方式', [validators.DataRequired()], render_kw={'placeholder': '请输入接口请求方式'})
    interface_can=StringField('请求参数', [validators.DataRequired()], render_kw={'placeholder': '请输入接口请求参数'})
    interface_rest = StringField('请求预期', [validators.DataRequired()], render_kw={'placeholder': '请输入接口预期'})
