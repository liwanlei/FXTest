"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import app
from flask import request, render_template, \
    make_response, send_from_directory, \
    flash, redirect, url_for
from flask_mail import Mail, Message
from app.models import *
from common.jsontools import reponse
import os
from flask.views import MethodView
from app.form import RegFrom
from flask_login import login_required, current_user
from config import email_type
from error_message import *
from common.systemlog import logger


def get_common_data():
    projects = Project.query.filter_by(status=False).all()
    model = Model.query.filter_by(status=False).all()
    return projects, model


@app.route('/down_jiekou', methods=['GET'])
@login_required
def down_jiekou():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, 'upload')
    response = make_response(send_from_directory(file_dir, 'interface.xlsx', as_attachment=True))
    return response


@app.route('/down_case', methods=['GET'])
@login_required
def down_case():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, 'upload')
    response = make_response(send_from_directory(file_dir, 'interface_case.xlsx', as_attachment=True))
    return response


class LoadView(MethodView):
    @login_required
    def get(self, filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir, 'upload')
        response = make_response(send_from_directory(file_dir, filename, as_attachment=True))
        return response


@app.route('/gettest', methods=['POST'])
# @login_required
def gettest():  # ajax获取项目的测试用例
    projec = (request.get_data('project')).decode('utf-8')
    if not projec:
        return reponse(code=MessageEnum.successs.value[0], data='', message=MessageEnum.successs.value[1])
    proje = Project.query.filter_by(project_name=str(projec)).first()
    if not proje:
        return reponse(code=MessageEnum.successs.value[0], data='', message=MessageEnum.successs.value[1])
    all_case = InterfaceTest.query.filter_by(projects_id=proje.id).all()
    case_list = []
    for item in all_case:
        if item.status == True:
            continue
        else:
            case_list.append({'name': item.Interface_name, 'id': item.id})
    return reponse(code=MessageEnum.successs.value[0],
                   data=case_list, message=MessageEnum.successs.value[1])


@app.route('/getprojects', methods=['GET', 'POST'])
@login_required
def getprojects():  # 获取项目
    id = request.get_data('id')
    if not id:
        return reponse(message=MessageEnum.request_null_message.value[1],
                       code=MessageEnum.request_null_message.value[0],
                       data={})
    interface = InterfaceTest.query.filter_by(id=int(id)).first()
    result = interface.projects
    projetc = Project.query.filter_by(project_name=str(result.project_name)).first()
    testhuanjing = Interfacehuan.query.filter_by(projects=projetc, status=False).all()

    if len(testhuanjing) <= 0:
        return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                       message=MessageEnum.testeveirment_not_exict.value[1],
                       data={})
    url_list = []
    for testevent in testhuanjing:
        url_list.append(testevent.url)
    if not interface:
        return reponse(code=MessageEnum.project_not_exict.value[0],
                       message=MessageEnum.project_not_exict.value[1],
                       data="")

    data = {}
    data['project'] = result.project_name
    data['url'] = url_list

    return reponse(data=data, code=MessageEnum.successs.value[0],
                   message=MessageEnum.successs.value[1])


class GetCaseView(MethodView):  # 获取用例
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not project:
            return reponse(
                message=MessageEnum.request_null_message.value[1],
                code=MessageEnum.request_null_message.value[0],
                data='')
        projectdata = Project.query.filter_by(project_name=project, status=False).first()
        if not projectdata:
            return reponse(
                message=MessageEnum.project_not_exict.value[1], code=MessageEnum.project_not_exict.value[0],
                data='')
        tesatcaelist = InterfaceTest.query.filter_by(projects_id=projectdata.id, status=False).all()
        caselit = []
        for i in tesatcaelist:
            caselit.append(i.id)
        return reponse(code=MessageEnum.request_success.value[0],
                       message=MessageEnum.request_success.value[1],
                       data=(caselit))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')


class IndexFirstview(MethodView):
    def get(self):
        return redirect(url_for("home.index"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegFrom()
    if request.method == 'POST':
        usernmae = request.form.get('username')
        pasword = request.form.get('password')
        setpasswod = request.form.get('se_password')
        email = request.form.get('email')
        jobnum = request.form.get("jobnum")
        if email == "" or email is None:
            flash(MessageEnum.user_email_not_none.value[1])
            return render_template('home/register.html', form=form)
        try:
            if (str(email.split("@")[1]) != email_type):
                flash(MessageEnum.email_geshi_error.value[1])
                return render_template('home/register.html', form=form)
        except Exception as e:
            logger.exception(e)
            flash(MessageEnum.user_email_error.value[1])
            return render_template('home/register.html', form=form)
        job_num = User.query.filter_by(jobnum=jobnum).first()
        if job_num:
            flash(MessageEnum.jobnum_oblg_reg_one.value[1])
            return render_template('home/register.html', form=form)
        if pasword != setpasswod:
            flash(MessageEnum.password_not_same.value[1])
            return render_template('home/register.html', form=form)
        user = User.query.filter_by(username=usernmae).first()
        if user:
            flash(MessageEnum.user_exict.value[1])
            return render_template('home/register.html', form=form)
        emai = User.query.filter_by(user_email=email).first()
        if emai:
            flash(MessageEnum.email_exict.value[1])
            return render_template('home/register.html', form=form)
        new_user = User(username=usernmae, user_email=email, jobnum=job_num)
        new_user.set_password(pasword)
        db.session.add(new_user)
        try:
            db.session.commit()
            # 需要邮箱发送的方法
            msg = Message(u"你好", sender=email, recipients=email)
            msg.body = u"欢迎你注册, 你的用户名：%s，你的密码是：%s" % (usernmae, pasword)
            msg.html = '<a href="http://127.0.0.1:5000/login">去登录</a>'
            mail = Mail()
            mail.send(msg)
            return redirect(url_for('home.login'))
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.user_register_error.value[1])
            return render_template('home/register.html', form=form)
    return render_template('home/register.html', form=form)


class GeneraConfig(MethodView):
    def get(self):
        return render_template("add/addconfg.html")

    '''通用配置添加编辑'''

    def post(self):
        try:
            data = request.get_json()
            config = GeneralConfiguration.query.filter_by(name=data['name']).first()
            if config:
                return reponse(code=MessageEnum.common_is_same.value[0],
                               message=MessageEnum.common_is_same.value[1],
                               data='')
            if data['type'] == "key-value":
                newconfig = GeneralConfiguration(user=current_user, style=0,
                                                 key=data["key"],
                                                 name=data['name'])
                db.session.add(newconfig)
                db.session.commit()
                return reponse(code=MessageEnum.successs.value[0],
                               message=MessageEnum.successs.value[1])
            elif data['type'] == 'token':
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], token_method=data['method'],
                                                 token_parame=data['parame'], token_url=data['url'])
                db.session.add(newconfig)
                db.session.commit()
                return reponse(code=MessageEnum.successs.value[0],
                               message=MessageEnum.successs.value[1])
            elif data['type'] == 'sql':
                testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
                if not testevnet:
                    return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                                   message=MessageEnum.testeveirment_not_exict.value[1])
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], testevent=testevnet,
                                                 sqlurl=data['sql'])
                db.session.add(newconfig)
                db.session.commit()
                return reponse(code=MessageEnum.successs.value[0],
                               message=MessageEnum.successs.value[1])
            elif data['type'] == 'http请求':
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], request_method=data['method'],
                                                 request_parame=data['parame'], request_url=data['url'])
                db.session.add(newconfig)
                db.session.commit()
                return reponse(code=MessageEnum.successs.value[0],
                               message=MessageEnum.successs.value[1])
            else:
                return reponse(code=MessageEnum.common_gene_not_support.value[0],
                               message=MessageEnum.common_gene_not_support.value[1], data='')

        except Exception as e:
            logger.exception(e)
            return reponse(
                code=MessageEnum.parames_not_null.value[0],
                message=MessageEnum.parames_not_null.value[1])

    @login_required
    def put(self):
        data = request.get_json()
        config_is = GeneralConfiguration.query.filter_by(id=int(data['id'])).first()
        if not config_is:
            return reponse(
                code=MessageEnum.common_is_not_exict.value[0],
                message=MessageEnum.common_is_not_exict.value[1],
                data='')
        if data['type'] == "key-value":
            config_is.user = current_user
            config_is.style = 0
            config_is.key = data["key"]
            db.session.commit()
            return reponse(code=MessageEnum.common_edit_is_success.value[0],
                           message=MessageEnum.common_edit_is_success.value[1])
        elif data['type'] == 'token':
            config_is.user = current_user
            config_is.style = 1,
            config_is.name = data['name']
            config_is.token_method = data['method'],
            config_is.token_parame = data['parame'],
            config_is.token_url = data['url']
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.common_gene_not_support.value[1])
        elif data['type'] == 'sql':
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
            config_is.user = current_user
            config_is.style = 1
            config_is.name = data['name']
            config_is.testevent = testevnet
            config_is.sqlurl = data['sql']
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        elif data['type'] == 'http请求':
            config_is.user = current_user
            config_is.style = 1
            config_is.name = data['name']
            config_is.request_method = data['method']
            config_is.request_parame = data['parame']
            config_is.request_url = data['url']
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.common_gene_not_support.value[1])
        else:
            return reponse(code=MessageEnum.common_gene_not_support.value[0],
                           message=MessageEnum.common_gene_not_support.value[1], data='')


class ActionViews(MethodView):
    '''操作添加编辑'''

    @login_required
    def post(self):
        data = request.get_json()
        name_is = Action.query.filter_by(name=data['name']).first()
        if name_is:
            return reponse(code=MessageEnum.re_is_same.value[0], message=MessageEnum.re_is_same.value[1])
        action = Action(name=data['name'], user=current_user)
        if data['catepy'] == '前置':
            action.category = 0
        else:
            action.category = 1
        if data['type'] == "0":
            action.sleepnum = int(data['num'])
            action.style = 0
            db.session.add(action)
            db.session.commit()
            return reponse(code=MessageEnum.request_success.value[0], message=MessageEnum.request_success.value[1])
        elif data['type'] == "1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
            action.testevent = testevnet
            action.style = 1
            action.sql = data['sql']
            db.session.add(action)
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        elif data['type'] == "2":
            action.style = 2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
            case_is = InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not case_is:
                return reponse(
                    code=MessageEnum.case_not_exict.value[0], message=MessageEnum.case_not_exict.value[1])
            action.testevent = testevnet
            action.caseid = int(data['caseid'])
            db.session.add(action)
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        elif data['type'] == "3":
            action.style = 3
            action.requestsurl = data['url']
            action.requestmethod = data['method']
            action.requestsparame = data['parame']
            db.session.add(action)
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        else:
            return reponse(
                code=MessageEnum.re_is_not_exitc.value[0],
                message=MessageEnum.re_is_not_exitc.value[1], data='')

    @login_required
    def put(self):
        data = request.get_json()
        id = Action.query.filter_by(id=data['id']).first()
        if not id:
            return reponse(code=MessageEnum.re_editisnot.value[0],
                           message=MessageEnum.re_editisnot.value[1])

        if data['type'] == "0":
            id.sleepnum = int(data['num'])
            id.style = 0
            db.session.commit()
            return reponse(code=MessageEnum.re_editisnot.value[0],
                           message=MessageEnum.successs.value[1])
        elif data['type'] == "1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
            id.testevent = testevnet
            id.style = 1
            id.sql = data['sql']
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0], message=MessageEnum.successs.value[1])
        elif data['type'] == "2":
            id.style = 2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return reponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
            case_is = InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not case_is:
                return reponse(
                    code=MessageEnum.case_not_exict.value[0],
                    message=MessageEnum.case_not_exict.value[1])
            id.testevent = testevnet
            id.caseid = case_is.id
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        elif data['type'] == "3":
            id.style = 3
            id.requestsurl = data['url']
            id.requestmethod = data['method']
            id.requestsparame = data['parame']
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        else:
            return reponse(
                code=MessageEnum.re_is_not_exitc.value[0], message=MessageEnum.re_is_not_exitc.value[1], data='')
