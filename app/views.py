"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import app
from flask import request, render_template, \
    make_response, send_from_directory, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
from app.models import *
import os
from flask.views import MethodView
from error_message import *
from app.form import RegFrom
from flask_login import login_required, current_user
from config import email_type


def get_pro_mo():
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
@login_required
def gettest():  # ajax获取项目的测试用例
    projec = (request.get_data('project')).decode('utf-8')
    if not projec:
        return []
    proje = Project.query.filter_by(project_name=str(projec)).first()
    if not proje:
        return []
    testyong = InterfaceTest.query.filter_by(projects_id=proje.id).all()
    testyong_list = []
    for i in testyong:
        if i.status == True:
            continue
        else:
            testyong_list.append({'name': i.Interface_name, 'id': i.id})
    return jsonify({'data': testyong_list})


@app.route('/getprojects', methods=['GET', 'POST'])
@login_required
def getprojects():  # 获取项目
    id = request.get_data('id')
    if not id:
        return jsonify({'msg': request_null_message, 'code': 108})
    peoject = InterfaceTest.query.filter_by(id=int(id)).first()
    result = peoject.projects
    projetc = Project.query.filter_by(project_name=str(result.project_name)).first()
    testhuanjing = Interfacehuan.query.filter_by(projects=projetc, status=False).all()
    if len(testhuanjing) <= 0:
        return jsonify({'msg': testeveirment_not_exict, 'code': 107, 'data': str(result)})
    url_list = []
    for huanjing in testhuanjing:
        url_list.append(huanjing.url)
    if not peoject:
        return jsonify({'msg': project_not_exict, 'code': 109, 'data': ''})
    return jsonify({'data': str(result), 'huanjing': url_list, 'code': 200, 'msg': request_success})


class Getyongli(MethodView):  # 获取用例
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not project:
            return jsonify({'msg': request_null_message, 'code': 8, 'data': ''})
        peoject = Project.query.filter_by(id=project, status=False).first()
        if not peoject:
            return jsonify({'msg': project_not_exict, 'code': 9, 'data': ''})
        tesatcaelist = InterfaceTest.query.filter_by(projects_id=peoject.id, status=False).all()
        caselit = []
        for i in tesatcaelist:
            caselit.append(i.id)
        return jsonify({'code': 200, 'msg': request_success, 'data': (caselit)})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')


class IndexFirstview(MethodView):
    def get(self):
        return redirect(url_for("home.index"))


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegFrom()
    if request.method == 'POST':
        usernmae = request.form.get('username')
        pasword = request.form.get('password')
        setpasswod = request.form.get('se_password')
        email = request.form.get('email')
        jobnum = request.form.get("jobnum")
        if email == "" or email is None:
            flash('邮箱不能为空')
            return render_template('home/reg.html', form=form)
        try:
            if (str(email.split("@")[1]) != email_type):
                flash(email_geshi_error)
                return render_template('home/reg.html', form=form)
        except Exception as e:
            flash("邮箱格式错误")
            return render_template('home/reg.html', form=form)
        job_num = User.query.filter_by(jobnum=jobnum).first()
        if job_num:
            flash(jobnum_oblg_reg_one)
            return render_template('home/reg.html', form=form)
        if pasword != setpasswod:
            flash(password_not_same)
            return render_template('home/reg.html', form=form)
        user = User.query.filter_by(username=usernmae).first()
        if user:
            flash(user_exict)
            return render_template('home/reg.html', form=form)
        emai = User.query.filter_by(user_email=email).first()
        if emai:
            flash(email_exict)
            return render_template('home/reg.html', form=form)
        new_user = User(username=usernmae, user_email=email, jobnum=job_num)
        new_user.set_password(pasword)
        db.session.add(new_user)
        try:
            db.session.commit()
            # 需要邮箱发送的方法
            msg = Message(u"你好", sender=email, recipients=email)
            msg.body = u"欢迎你注册, 你的用户名：%s，你的密码是：%s" % (usernmae, pasword)
            msg.html = '<a href="http://127.0.0.1:5000/login">去登录</a>'
            Mail.send(msg)
            return redirect(url_for('home.login'))
        except Exception as e:
            db.session.rollback()
            flash("注册失败")
            return render_template('home/reg.html', form=form)
    return render_template('home/reg.html', form=form)


class GeneraConfig(MethodView):
    def get(self):
        return render_template("add/addconfg.html")

    '''通用配置添加编辑'''

    def post(self):
        try:
            data = request.get_json()
            config = GeneralConfiguration.query.filter_by(name=data['name']).first()
            if config:
                return jsonify({'code': 11, 'msg': common_is_same, 'data': ''})
            if data['type'] == "key-value":
                newconfig = GeneralConfiguration(user=current_user, style=0,
                                                 key=data["key"], name=data['name'])
                db.session.add(newconfig)
                db.session.commit()
                return jsonify({'code': 200, 'msg': request_success})
            elif data['type'] == 'token':
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], token_method=data['method'],
                                                 token_parame=data['parame'], token_url=data['url'])
                db.session.add(newconfig)
                db.session.commit()
                return jsonify({'code': 200, 'msg': request_success})
            elif data['type'] == 'sql':
                testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
                if not testevnet:
                    return jsonify({'code': 11, 'msg': testeveirment_not_exict})
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], testevent=testevnet,
                                                 sqlurl=data['sql'])
                db.session.add(newconfig)
                db.session.commit()
                return jsonify({'code': 200, 'msg': request_success})
            elif data['type'] == 'http请求':
                newconfig = GeneralConfiguration(user=current_user, style=1,
                                                 name=data['name'], request_method=data['method'],
                                                 request_parame=data['parame'], request_url=data['url'])
                db.session.add(newconfig)
                db.session.commit()
                return jsonify({'code': 200, 'msg': request_success})
            else:
                return jsonify({'code': 11, 'msg': common_gene_not_support, 'data': ''})

        except Exception as e:
            return jsonify({'code': 12, 'data': "参数缺少"})

    @login_required
    def put(self):
        data = request.get_json()
        config_is = GeneralConfiguration.query.filter_by(id=int(data['id'])).first()
        if not config_is:
            return jsonify({'code': 11, 'msg': common_is_not_exict, 'data': ''})
        if data['type'] == "key-value":
            config_is.user = current_user
            config_is.style = 0
            config_is.key = data["key"]
            db.session.commit()
            return jsonify({'code': 200, 'msg': common_edit_is_success})
        elif data['type'] == 'token':
            config_is.user = current_user
            config_is.style = 1,
            config_is.name = data['name']
            config_is.token_method = data['method'],
            config_is.token_parame = data['parame'],
            config_is.token_url = data['url']
            db.session.commit()
            return jsonify({'code': 200, 'msg': common_edit_is_success})
        elif data['type'] == 'sql':
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': testeveirment_not_exict})
            config_is.user = current_user
            config_is.style = 1
            config_is.name = data['name']
            config_is.testevent = testevnet
            config_is.sqlurl = data['sql']
            db.session.commit()
            return jsonify({'code': 200, 'msg': common_edit_is_success})
        elif data['type'] == 'http请求':
            config_is.user = current_user
            config_is.style = 1
            config_is.name = data['name']
            config_is.request_method = data['method']
            config_is.request_parame = data['parame']
            config_is.request_url = data['url']
            db.session.commit()
            return jsonify({'code': 200, 'msg': common_edit_is_success})
        else:
            return jsonify({'code': 11, 'msg': common_gene_not_support, 'data': ''})


class ActionViews(MethodView):
    '''操作添加编辑'''

    @login_required
    def post(self):
        data = request.get_json()
        name_is = Action.query.filter_by(name=data['name']).first()
        if name_is:
            return jsonify({'code': 2, 'msg': re_is_same})
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
            return jsonify({'code': 200, 'msg': request_success})
        elif data['type'] == "1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': testeveirment_not_exict})
            action.testevent = testevnet
            action.style = 1
            action.sql = data['sql']
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success})
        elif data['type'] == "2":
            action.style = 2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': testeveirment_not_exict})
            case_is = InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not case_is:
                return jsonify({'code': 11, 'msg': case_not_exict})
            action.testevent = testevnet
            action.caseid = int(data['caseid'])
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success})
        elif data['type'] == "3":
            action.style = 3
            action.requestsurl = data['url']
            action.requestmethod = data['method']
            action.requestsparame = data['parame']
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success})
        else:
            return jsonify({'code': 11, 'msg': re_is_not_exitc, 'data': ''})

    @login_required
    def put(self):
        data = request.get_json()
        id = Action.query.filter_by(id=data['id']).first()
        if not id:
            return jsonify({'code': 2, 'msg': re_editisnot})

        if data['type'] == "0":
            id.sleepnum = int(data['num'])
            id.style = 0
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success})
        elif data['type'] == "1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': testeveirment_not_exict})
            id.testevent = testevnet
            id.style = 1
            id.sql = data['sql']
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success % id.name})
        elif data['type'] == "2":
            id.style = 2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': testeveirment_not_exict})
            case_is = InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not case_is:
                return jsonify({'code': 11, 'msg': case_not_exict})
            id.testevent = testevnet
            id.caseid = case_is.id
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success % id.name})
        elif data['type'] == "3":
            id.style = 3
            id.requestsurl = data['url']
            id.requestmethod = data['method']
            id.requestsparame = data['parame']
            db.session.commit()
            return jsonify({'code': 200, 'msg': request_success % id.name})
        else:
            return jsonify({'code': 11, 'msg': re_is_not_exitc, 'data': ''})
