# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import Blueprint, flash
import json
from common.mergelist import hebinglist
from flask import redirect, request, render_template, url_for, session

from common.jsontools import reponse
from app.models import *
from app.form import *
from flask.views import MethodView
from flask_login import login_required, login_user, \
    logout_user, current_user
from app import loginManager, sched
from common.Pagination import fenye_list
from common.pageination import Pagination
from error_message import *
from common.packageredis import ConRedisOper
from config import *
from common.systemlog import logger

home = Blueprint('home', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class IndexView(MethodView):
    @login_required
    def get(self):
        interface_cont = Interface.query.filter_by(status=False).all()
        interface_result = TestcaseResult.query.all()
        result_list_case = []
        for result in interface_result:
            result_list_case.append(result.case_id)
        all_run_case_count = len(set(result_list_case))
        interface_list = []
        for interface in range(len(interface_cont) + 1):
            try:
                if interface_cont[interface].projects.status is False:
                    interface_list.append(interface_cont[interface])
                else:
                    interface += 1
            except:
                interface += 1
        interfaceTest_cunt = InterfaceTest.query.filter_by(status=False).all()
        case_list = []
        for case in range(len(interfaceTest_cunt)):
            try:
                if interfaceTest_cunt[case].projects.status is False:
                    case_list.append(interfaceTest_cunt[case])
                else:
                    case += 1
            except:
                case += 1
        resu_cout = TestResult.query.filter_by(status=False).all()
        reslut_list = []
        for result in range(len(resu_cout)):
            try:
                if resu_cout[result].projects.status is False:
                    reslut_list.append(resu_cout[result])
                else:
                    result += 1
            except:
                result += 1
        My_task = []
        for job in sched.get_jobs():
            job_task = Task.query.filter_by(id=job.id, status=False).first()
            if job_task.makeuser == current_user.id:
                My_task.append({'taskname': job_task.taskname,
                                'next_run': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S '),
                                'run_status': job_task.yunxing_status,
                                'id': job_task.id
                                })
        project_cout = Project.query.filter_by(status=False).count()
        model_cout = Model.query.filter_by(status=False).count()
        return render_template('home/index.html', yongli=len(case_list),
                               jiekou=len(interface_list),
                               report=len(reslut_list),
                               project_cout=project_cout,
                               model_cout=model_cout, my_tasl=My_task,
                               all_run_case_count=all_run_case_count)


class LoginView(MethodView):
    def get(self):
        form = LoginFrom()
        return render_template('home/login.html', form=form)

    def post(self):
        data = request.get_json()
        if data is None:
            return reponse(message=MessageEnum.login_username_not_message.value[1],
                           code=MessageEnum.login_username_not_message.value[0],
                           data='')
        ip = request.remote_addr
        username = data['username']
        password = data['password']
        if username is None:
            return reponse(message=MessageEnum.login_username_not_message.value[1],
                           code=MessageEnum.login_username_not_message.value[0],
                           data="")
        if password is None:
            return reponse(message=MessageEnum.login_password_not_message.value[1],
                           code=MessageEnum.login_password_not_message.value[0],
                           data='')
        user = User.query.filter_by(username=username).first()
        user_err_num = user.err_num
        if (user.jobnum == "None" or user.jobnum is None):
            return reponse(message=MessageEnum.login_user_inactivatesd.value[1],
                           code=MessageEnum.login_user_inactivatesd.value[0],
                           data='')
        if user:
            if user.status is True:
                return reponse(message=MessageEnum.login_user_free_message.value[1],
                               code=MessageEnum.login_user_free_message.value[0],
                               data='')
            if user.check_password(password):
                if (user.is_free == True and user.freetime != None and user.err_num > 6 and (
                        datetime.datetime.now() - user.freetime).min > 10):
                    return reponse(
                        message=MessageEnum.login_user_fremm.value[1],
                        code=MessageEnum.login_user_fremm.value[0],
                        data='')
                user.is_login = True
                userlog = UserLoginlog(user=user.id,
                                       ip=ip,
                                       datatime=datetime.datetime.now())
                db.session.add_all([user, userlog])
                db.session.commit()
                login_user(user)
                session['username'] = username
                return reponse(message=MessageEnum.login_user_sucess_message.value[1],
                               code=MessageEnum.login_user_sucess_message.value[0],
                               data='')
            else:
                if (user.err_num != None and user.err_num >= 5):
                    print(user.freetime is None)
                    if (user.freetime != 'None' and user.freetime is not None ):
                        if (datetime.datetime.now() - user.freetime).min > 10:
                            user.err_num = user_err_num + 1
                            db.session.add(user)
                            db.session.commit()
                            return reponse(message=MessageEnum.login_password_error_message.value[1],
                                           code=MessageEnum.login_password_error_message.value[0],
                                           data='')
                        else:
                            user.err_num = 5
                            user.freetime = datetime.datetime.now()
                            user.is_free = True
                            db.session.add(user)
                            db.session.commit()
                            return reponse(message=MessageEnum.login_user_fremm.value[1],
                                           code=MessageEnum.login_user_fremm.value[0], data='')
                    else:
                        if user.err_num == None:
                            user.err_num = 0
                        else:
                            user.err_num = user_err_num + 1
                        db.session.add(user)
                        db.session.commit()
                        return reponse(message=MessageEnum.login_password_error_message.value[1],
                                       code=MessageEnum.login_password_error_message.value[0], data='')
                else:
                    if user.err_num == None:
                        user.err_num = 0
                    else:
                        user.err_num = user_err_num + 1
                    db.session.add(user)
                    db.session.commit()
                    return reponse(message=MessageEnum.login_password_error_message.value[1],
                                   code=MessageEnum.login_password_error_message.value[0], data='')
        return reponse(message=MessageEnum.login_user_not_exict_message.value[1],
                       code=MessageEnum.login_user_not_exict_message.value[0],
                       data='')


class LoginViewRedis(MethodView):
    '''redis'''

    def __init__(self):
        self.conris = ConRedisOper(redis_host, redis_port, 3)

    def get(self):
        form = LoginFrom()
        return render_template('home/login.html', form=form)

    def post(self):
        data = request.get_json()
        ip = request.remote_addr
        username = data['username']
        password = data['password']
        if username is None:
            return reponse(message=MessageEnum.login_username_not_message.value[1],
                           code=MessageEnum.login_username_not_message.value[0], data='')
        if password is None:
            return reponse(message=MessageEnum.login_password_not_message.value[1],
                           code=MessageEnum.login_password_not_message.value[0], data='')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.status is True:
                return reponse(message=MessageEnum.login_user_free_message.value[1],
                               code=MessageEnum.login_user_free_message.value[0], data='')
            if user.check_password(password):
                user.is_login = True
                userlog = UserLoginlog(user=user.id, ip=ip, datatime=datetime.datetime.now())
                db.session.add_all([user, userlog])
                db.session.commit()
                login_user(user)
                session['username'] = username
                return reponse(message=MessageEnum.login_user_sucess_message.value[1],
                               code=MessageEnum.login_user_sucess_message.value[0], data='')
            else:
                try:
                    num = int(self.conris.getset(user.username))
                    if (user.is_free == True and num > 5):
                        return reponse(message=MessageEnum.login_user_fremm.value[1],
                                       code=MessageEnum.login_user_fremm.value[0], data='')
                    else:
                        self.conris.sethash(username, num + 1, 1000 * 60 * 10)
                        return reponse(message=MessageEnum.login_password_error_message.value[1],
                                       code=MessageEnum.login_password_error_message.value[0], data='')
                except Exception as  e:
                    self.conris.sethash(username, 1, 1000 * 60 * 10)
                    return reponse(message=MessageEnum.login_password_error_message.value[1],
                                   code=MessageEnum.login_password_error_message.value[0], data='')
        return reponse(message=MessageEnum.login_user_not_exict_message.value[1],
                       code=MessageEnum.login_user_not_exict_message.value[0], data='')


class LogoutView(MethodView):
    @login_required
    def get(self):
        username = session.get("username")
        session.clear()
        logout_user()
        user = User.query.filter_by(username=username).first()
        user.is_login = False
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.login', next=request.url))


class InterfaceView(MethodView):
    @login_required
    def get(self):
        models = Model.query.filter_by(status=False).all()
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for pros in current_user.quanxians:
                projects.append(pros.projects)
        return render_template('home/interface.html', projects=projects,
                               models=models)

    @login_required
    def post(self):
        data = request.get_json()
        project = data['project']
        model = data['model']
        name = data['name']
        url = data['url']
        headers = data['headers']
        xieyi = data['xieyi']
        meth = data['meth']
        project_id = Project.query.filter_by(project_name=project).first().id
        models_id = Model.query.filter_by(model_name=model).first().id
        try:
            new_interface = Interface(model_id=models_id,
                                      projects_id=project_id,
                                      Interface_name=name,
                                      Interface_url=url,
                                      Interface_meth=meth,
                                      Interface_user_id=current_user.id,
                                      Interface_headers=headers,
                                      interfacetype=xieyi)
            db.session.add(new_interface)
            db.session.commit()
            return reponse(message=MessageEnum.interface_add_success.value[1],
                           code=MessageEnum.interface_add_success.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(
                message=MessageEnum.interface_add_erroe.value[1], code=MessageEnum.interface_add_erroe.value[0],
                data='')

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        interface = Interface.query.filter_by(id=data, status=False).first()
        if not interface:
            return reponse(
                message=MessageEnum.interface_add_not.value[1],
                code=MessageEnum.interface_add_not.value[0])

        interface.status = True
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.info(e)
            db.session.rollback()
            return reponse(message=MessageEnum.delete_inteface_error.value[1],
                           code=MessageEnum.delete_inteface_error.value[0])


class CaseView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for i in current_user.quanxians:
                projects.append(i.projects)
        return render_template('home/interface_case.html', projects=projects)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        testcase = InterfaceTest.query.filter_by(id=data).first()
        if not testcase:
            return reponse(data=MessageEnum.case_not_exict.value[1],
                           code=MessageEnum.case_not_exict.value[0])
        try:
            testcase.status = True
            db.session.commit()
            return reponse(data=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(
                data=MessageEnum.delete_case_error.value[1],
                code=MessageEnum.delete_case_error.value[0])


class AdminUserView(MethodView):
    @login_required
    def get(self):
        wrok = Work.query.all()
        projects = Project.query.filter_by(status=False).all()
        if current_user.is_sper is True:
            pagination = (User.query.order_by(User.id.desc()).all())
        else:
            pagination = []
            id = []
            for projec in current_user.quanxians:
                if (projec.user.all() in id) is False:
                    pagination.append(projec.user.all())
                    id.append(projec.user.all())
            pagination = (hebinglist(pagination))
        pager_obj = Pagination(request.args.get("page", 1),
                               len(pagination), request.path, request.args,
                               per_page_count=PageShow)
        index_list = pagination[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('home/useradmin.html', users=index_list,
                               html=html, wroks=wrok, projects=projects)

    @login_required
    def post(self):
        data = request.get_json()
        name = data['name']
        password = data['password']
        work = data['work']
        project = data['project']
        email = data['email']
        use = User.query.filter_by(username=name).first()
        if use:
            return reponse(message=MessageEnum.user_is_exict.value[1],
                           code=MessageEnum.user_is_exict.value[0])
        emai = User.query.filter_by(user_email=str(email)).first()
        if emai:
            return reponse(message=MessageEnum.email_only_one.value[1],
                           code=MessageEnum.email_only_one.value[0])
        wrok = Work.query.filter_by(name=work).first()
        new_user = User(username=name, user_email=email)
        new_user.set_password(password)
        new_user.work_id = wrok.id
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(message=MessageEnum.model_edit_fial.value[1],
                           code=MessageEnum.model_edit_fial.value[0])
        if len(project) <= 0:
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        else:
            try:
                user_id = User.query.filter_by(username=name).first()
                for proj in project:
                    project_one = Project.query.filter_by(project_name=proj).first()
                    quanxian = Quanxian(project=project_one.id, rose=1)
                    quanxian.user.append(user_id)
                    db.session.add(quanxian)
                db.session.commit()
                return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                return reponse(message=MessageEnum.model_edit_fial.value[1], code=MessageEnum.model_edit_fial.value[0])


class TestResultView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            project = Project.query.filter_by(status=False).all()
        else:
            project = []
            for projec in current_user.quanxians:
                project.append(projec.projects)
        projects_lsit = fenye_list(Ob_list=project, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/test_result.html', projects=pyth_post1, pages=pages)
        except Exception as e:
            logger.exception(e)
            return redirect(url_for('home.test_result'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        delTest = TestResult.query.filter_by(id=data, status=False).first()
        if not delTest:
            return reponse(message=MessageEnum.delete_report_not_exict.value[1], code=MessageEnum.delete_report_not_exict.value[0])
        delTest.status = True
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(message=MessageEnum.delete_report_fail.value[1], code=MessageEnum.delete_report_fail.value[0])


class ProjectView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if i.projects in id == False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        projects_lsit = fenye_list(Ob_list=projects, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/project.html', projects=pyth_post1, pages=pages)
        except:
            return redirect(url_for('home.project'))

    @login_required
    def post(self):
        name = request.data.decode('utf-8')
        if current_user.is_sper == False:
            return reponse(message=MessageEnum.user_not_permision.value[1],
                           code=MessageEnum.user_not_permision.value[0])
        if name == '':
            return reponse(code=MessageEnum.project_cannot_empty.value[0], message=MessageEnum.project_cannot_empty.value[1])

        projec = Project.query.filter_by(project_name=name, status=False).first()
        if projec:
            return reponse(code=MessageEnum.project_only_one.value[0], message=MessageEnum.project_only_one.value[1])
        new_moel = Project(project_name=name, project_user_id=current_user.id)
        try:
            db.session.add(new_moel)
            db.session.commit()
            # testgroup = TestGroup(adduser=current_user.id,
            #                       addtime=datetime.datetime.now(),
            #                       updatetime=datetime.datetime.now(),
            #                       updateuser=current_user.id,
            #                       name='黑名单', projectid=new_moel.id)
            # db.session.add(testgroup)
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0], message=MessageEnum.successs.value[1])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(code=MessageEnum.project_add_error.value[0], message=MessageEnum.project_add_error.value[1] )

    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        prohect = Project.query.filter_by(id=id).first()
        if not prohect:
            new = Project(project_name=name, project_user_id=current_user.id)
            db.session.add(new)
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
        prohect.project_name = name
        try:
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(code=MessageEnum.eidt_excption.value[0], message=MessageEnum.eidt_excption.value[1])

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        proje = Project.query.filter_by(id=data, status=False).first()
        if not proje:
            return reponse(message=MessageEnum.project_not_exict.value[1], code=MessageEnum.project_not_exict.value[0])
        proje.status = True
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(message=MessageEnum.delete_fail.value[1], code=MessageEnum.delete_fail.value[0])


class ModelView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            project_list = Project.query.filter_by(status=False).all()
        else:
            project_list = []
            for projec in current_user.quanxians:
                project_list.append(projec.projects)
        models = Model.query.filter_by(status=False).all()
        projects_lsit = fenye_list(Ob_list=models, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        pyth_post1 = projects_lsit[int(page) - 1]
        return render_template('home/model.html', projects=pyth_post1, pages=pages,
                               project_list=project_list)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        model = Model.query.filter_by(id=data, status=False).first()
        if not model:
            return reponse(message=MessageEnum.model_not_exict.value[1], code=MessageEnum.model_not_exict.value[0])
        model.status = True
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(message=MessageEnum.delete_fail.value[1], code=MessageEnum.delete_fail.value[0])

    @login_required
    def post(self):
        data = request.get_json()
        models = Model.query.filter_by(model_name=data['name']).first()
        if data['project'] == '请选择':
            # common = True
            project_one = None
        else:
            project_one = Project.query.filter_by(project_name=data['project']).first().id
            # common = False
        if models:
            return reponse(code=MessageEnum.model_only_one.value[0], message=MessageEnum.model_only_one.value[1])

        new_moel = Model(model_name=data['name'], model_user_id=current_user.id,
                         project=project_one)
        db.session.add(new_moel)

        try:
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(code=MessageEnum.model_edit_fial.value[0], message=MessageEnum.model_edit_fial.value[1])

    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        projec = json_data['project']
        edit_mode = Model.query.filter_by(id=id, status=False).first()
        if projec == '请选择':
            project_one = None
        else:
            project_one = Project.query.filter_by(status=False, project_name=projec).first().id
        if not edit_mode:
            mew = Model(model_name=name, model_user_id=current_user.id)
            db.session.add(mew)
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
        edit_mode.model_name = name
        edit_mode.project = project_one
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(message=MessageEnum.edit_model_error.value[1], code=MessageEnum.edit_model_error.value[0])


class TestenvironmentView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            events = []
            events.append(Interfacehuan.query.filter_by(status=False).order_by(
                Interfacehuan.id.desc()).all())
        else:
            events = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) is False:
                    events.append(
                        Interfacehuan.query.filter_by(project=project.projects.id,
                                                      status=False).order_by(
                            Interfacehuan.id.desc()).all())
                    id.append(project.projects.id)
        projects_lsit = fenye_list(Ob_list=events, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).order_by(
                Project.id.desc()).all()
        else:
            projects = []
            for i in current_user.quanxians:
                if (i.projects in i) is False:
                    projects.append(i.projects)
        try:
            teststcentpage = projects_lsit[int(page) - 1]
            return render_template('home/events.html', events=teststcentpage,
                                   pages=pages,
                                   projects=projects)
        except Exception as e:
            print(e)
            return redirect(url_for('home.testenvironment'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        event = Interfacehuan.query.filter_by(id=data).first()
        event.status = True
        try:
            db.session.commit()
            return reponse(
                code=MessageEnum.successs.value[0]
                , message=MessageEnum.successs.value[1]
            )
        except Exception as e:
            logger.error(e)
            return reponse(message=MessageEnum.delete_fail.value[1],
                           code=MessageEnum.delete_fail.value[0])

    @login_required
    def post(self):
        data = request.get_json()
        json_data = data
        project = json_data['project']
        url = json_data['url']
        desc = json_data['desc']
        name = json_data['name']
        host = json_data['host']
        port = json_data['port']
        usernmae = json_data['username']
        password = json_data['password']
        url_old = Interfacehuan.query.filter_by(url=str(url)).first()
        if url_old:
            return reponse(message=MessageEnum.testeveirment_use_one_nam.value[1],
                           code=MessageEnum.testeveirment_use_one_nam.value[0], data='')
        prkcyt = Project.query.filter_by(project_name=project).first()
        testevent = Interfacehuan(url=url, desc=desc, project=prkcyt.id,
                                  database=name,
                                  databaseuser=usernmae, databasepassword=password,
                                  dbhost=host,
                                  dbport=port, make_user=current_user.id)
        db.session.add(testevent)
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(message=MessageEnum.add_case_erro, code=211)

    @login_required
    def put(self):
        data = request.get_json()
        json_data = data
        project = json_data['project']
        id = json_data['id']
        url = json_data['url']
        desc = json_data['desc']
        name = json_data['name']
        host = json_data['host']
        port = json_data['port']
        usernmae = json_data['username']
        password = json_data['password']
        project = Project.query.filter_by(project_name=project).first()
        event = Interfacehuan.query.filter_by(id=id).first()
        if not event:
            newevent = Interfacehuan(url=url, desc=desc, project=project.id,
                                     database=name,
                                     databaseuser=usernmae,
                                     databasepassword=password, dbhost=host,

                                     dbport=port, make_user=current_user.id)
            db.session.add(newevent)
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        event.url = url
        event.desc = desc
        event.database = name
        event.databaseuser = usernmae
        event.datebasepassword = password
        event.dbhost = host
        event.dbport = port
        event.project = project.id
        event.make_user = current_user.id
        try:
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(message=MessageEnum.edit_mock_error.value[1],
                           code=MessageEnum.edit_mock_error.value[0])


class MockViews(MethodView):
    @login_required
    def get(self, page=1):
        mock = Mockserver.query.filter_by(delete=False).order_by(
            Mockserver.id.desc()).paginate(page,
                                           per_page=int(PageShow),
                                           error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)

    @login_required
    def post(self):
        data_post = request.get_json()
        name_exict = Mockserver.query.filter_by(name=data_post['name']).first()
        if name_exict:
            return reponse(code=MessageEnum.mock_name_only_one.value[0],
                           message=MessageEnum.mock_name_only_one.value[1])
        if data_post['checkout'] == u'是':
            is_check = True
        else:
            is_check = False
        if data_post['checkouheaders'] == u'是':
            is_headers = True
        else:
            is_headers = False
        if data_post['kaiqi'] == u'是':
            is_kaiqi = True
        else:
            is_kaiqi = False
        new_mock = Mockserver(name=data_post['name'])
        new_mock.make_uers = current_user.id
        new_mock.path = data_post['path']
        new_mock.methods = data_post['meth']
        new_mock.headers = data_post['headers']
        new_mock.description = data_post['desc']
        new_mock.fanhui = data_post['back']
        new_mock.params = data_post['parm']
        new_mock.rebacktype = data_post['type']
        new_mock.status = is_kaiqi
        new_mock.ischeck = is_check
        new_mock.is_headers = is_headers
        new_mock.update_time = datetime.datetime.now()
        db.session.add(new_mock)
        try:
            db.session.commit()
            return reponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return reponse(code=MessageEnum.create_mock_error.value[0],
                           message=MessageEnum.create_mock_error.value[1])

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        ded = Mockserver.query.filter_by(id=data, status=False).first()
        if ded:
            ded.delete = True
            db.session.commit()
            return reponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0])
        return reponse(message=MessageEnum.delete_mock_error.value[1],
                       code=MessageEnum.delete_mock_error.value[0])


class TimingtasksView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            task = []
            task.append(Task.query.filter_by(status=False).order_by(Task.id.desc()).all())
        else:
            task = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) is False:
                    task.append(Task.query.filter_by(prject=project.projects.id,
                                                     status=False).all())
                    id.append(project.projects.id)
        old_yask = hebinglist(task)
        projects_lsit = fenye_list(Ob_list=old_yask, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/timingtask.html', inte=pyth_post1, pages=pages)
        except Exception as e:
            logger.error(e)
            return redirect(url_for('home.timingtask'))


class GetProtestReportView(MethodView):
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not project:
            return reponse(message=MessageEnum.error_send_message.value[1],
                           code=MessageEnum.error_send_message.value[0], data='')
        project_is = Project.query.filter_by(project_name=project).first()
        if not project_is:
            return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0], data=[])
        testreport = TestResult.query.filter_by(projects_id=project_is.id,
                                                status=False).order_by(
            TestResult.id.desc()).all()
        testreportlist = []
        for test in testreport:
            testreportlist.append({'test_num': test.test_num, 'pass_num': test.pass_num,
                                   'fail_num': test.fail_num,
                                   'hour_time': str(test.hour_time),
                                   'test_rep': test.test_rep, 'test_log': test.test_log,
                                   'Exception_num': test.Exception_num,
                                   'can_num': test.can_num,
                                   'wei_num': test.wei_num,
                                   'test_time': str(test.test_time),
                                   'Test_user_id': test.users.username, 'id': test.id,
                                   'fenshu': test.pass_num / test.test_num})
        return reponse(message=MessageEnum.successs.value[1], code=MessageEnum.successs.value[0], data=(testreportlist))

    # class JenkinsFirst(MethodView):
    #     @login_required
    #     def get(self):
    #         try:
    #             # tasks=Task.query.filter_by(makeuser=current_user.id,status=False).all()
    #             jobs = Conlenct_jenkins().get_all_job()
    #             jenkis_task = []
    #             for job in jobs:
    #                 # for task in tasks:
    #                 #   if job['name']==task.taskname:
    #                 jenkis_task.append({'name': job['name'], 'url': job['url'],
    #                                     'color': job['color']})
    #             return render_template('home/jenkins.html', jobs=jenkis_task)
    #         except Exception as e:
    #             flash("无法连接jenkins服务器", category="error")
    #             return redirect(url_for('home.index'))

    # class JenkinsGou(MethodView):
    #     @login_required
    #     def get(self, jobname=''):
    #         goujian = Conlenct_jenkins().build_job(jobname)
    #         if goujian == True:
    #             flash('构建成功！', category="message")
    #             return redirect(url_for('home.jenkinsfirst'))
    #         else:
    #             flash('构建失败', category="message")
    #             return redirect(url_for('home.jenkinsfirst'))

    # class GetJenLogview(MethodView):
    #     @login_required
    #     def post(self):
    #         url = (request.get_data().decode('utf-8'))
    #         url_base = (url.split('&')[0])
    #         jobname = url.split('&')[1]
    #         try:
    #             log = Conlenct_jenkins().job_bulid_log(url_base, jobname)
    #             return reponse(code= 200, data= str(log)})
    #         except Exception as e:
    #             return reponse(code= 701, data= str(e)})
    #
    #
    # class DeleteJenkinstask(MethodView):
    #     @login_required
    #     def post(self, id):
    #         pass


class GenconfigView(MethodView):
    @login_required
    def get(self, page=1):
        genconfiglist = GeneralConfiguration.query.filter_by(status=False).order_by(
            GeneralConfiguration.id.desc()).all()
        projects_lsit = fenye_list(Ob_list=genconfiglist, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/genconfig.html', inte=pyth_post1, pages=pages)
        except Exception as e:
            logger.error(e)
            return redirect(url_for('home.genconfig'))


class DeleteGenconfigView(MethodView):
    @login_required
    def get(self, id):
        gencofigilist = GeneralConfiguration.query.filter_by(id=id, status=False).first()
        if not gencofigilist:
            flash(MessageEnum.config_not_exict.value[1])
        gencofigilist.status = True
        try:
            db.session.commit()
            flash(MessageEnum.successs.value[1])
            return redirect(url_for('home.genconfig'))
        except Exception as e:
            logger.error('删除配置失败！原因：%s' % e)
            db.session.rollback()
            flash(MessageEnum.cobfig_delete_error.value[1])
            return redirect(url_for('home.genconfig'))
