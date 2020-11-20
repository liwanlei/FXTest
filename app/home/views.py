# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import Blueprint, jsonify, flash
import json
from common.mergelist import hebinglist
from flask import redirect, request, render_template, url_for, session

home = Blueprint('home', __name__)
from app.models import *
from app.form import *
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user, current_user
from app import loginManager, sched
from common.Pagination import fenye_list
from common.pageination import Pagination
from error_message import *
from common.CollectionJenkins import Conlenct_jenkins
from common.packageredis import ConRedisOper
from config import *


def get_pro_mo():
    projects = Project.query.filter_by(status=False).all()
    model = Model.query.filter_by(status=False).all()
    return projects, model


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class index(MethodView):
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
                if interface_cont[interface].projects.status == False:
                    interface_list.append(interface_cont[interface])
                else:
                    interface += 1
            except:
                interface += 1
        interfaceTest_cunt = InterfaceTest.query.filter_by(status=False).all()
        case_list = []
        for case in range(len(interfaceTest_cunt)):
            try:
                if interfaceTest_cunt[case].projects.status == False:
                    case_list.append(interfaceTest_cunt[case])
                else:
                    case += 1
            except:
                case += 1
        resu_cout = TestResult.query.filter_by(status=False).all()
        reslut_list = []
        for result in range(len(resu_cout)):
            try:
                if resu_cout[result].projects.status == False:
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
                                'run_status': job_task.yunxing_status, 'id': job_task.id
                                })
        project_cout = Project.query.filter_by(status=False).count()
        model_cout = Model.query.filter_by(status=False).count()
        return render_template('home/index.html', yongli=len(case_list),
                               jiekou=len(interface_list),
                               report=len(reslut_list), project_cout=project_cout,
                               model_cout=model_cout, my_tasl=My_task, all_run_case_count=all_run_case_count)


class LoginView(MethodView):
    def get(self):
        form = LoginFrom()
        return render_template('home/login.html', form=form)

    def post(self):
        data = request.get_json()
        ip = request.remote_addr
        username = data['username']
        password = data['password']
        if username is None:
            return jsonify({'msg': login_username_not_message, 'code': 33, 'data': ''})
        if password is None:
            return jsonify({'msg': login_password_not_message, 'code': 34, 'data': ''})
        user = User.query.filter_by(username=username).first()
        user_err_num = user.err_num
        if (user.jobnum == "None" or user.jobnum is None):
            return jsonify({'msg': login_user_inactivatesd, 'code': 34, 'data': ''})
        if user:
            if user.status is True:
                return jsonify({'msg': login_user_free_message, 'code': 35, 'data': ''})
            if user.check_password(password):
                if (user.is_free == True and user.freetime != None and user.err_num > 6 and (
                        datetime.datetime.now() - user.freetime).minute > 10):
                    return jsonify({'msg': login_user_fremm, 'code': 200, 'data': ''})
                user.is_login = True
                userlog = UserLoginlog(user=user.id, ip=ip, datatime=datetime.datetime.now())
                db.session.add_all([user, userlog])
                db.session.commit()
                login_user(user)
                session['username'] = username
                return jsonify({'msg': login_user_sucess_message, 'code': 200, 'data': ''})
            else:
                if (user.err_num != None and user.err_num >= 5):
                    if (user.freetime != 'None'):
                        if (datetime.datetime.now() - user.freetime).minute > 10:
                            user.err_num = user_err_num + 1
                            db.session.add(user)
                            db.session.commit()
                            return jsonify({'msg': login_password_error_message, 'code': 36, 'data': ''})
                        else:
                            user.err_num = 5
                            user.freetime = datetime.datetime.now()
                            user.is_free = True
                            db.session.add(user)
                            db.session.commit()
                            return jsonify({'msg': login_user_fremm, 'code': 36, 'data': ''})
                    else:
                        if user.err_num == None:
                            user.err_num = 0
                        else:
                            user.err_num = user_err_num + 1
                        db.session.add(user)
                        db.session.commit()
                        return jsonify({'msg': login_password_error_message, 'code': 36, 'data': ''})
                else:
                    if user.err_num == None:
                        user.err_num = 0
                    else:
                        user.err_num = user_err_num + 1
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'msg': login_password_error_message, 'code': 36, 'data': ''})
        return jsonify({'msg': login_user_not_exict_message, 'code': 37, 'data': ''})


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
            return jsonify({'msg': login_username_not_message, 'code': 33, 'data': ''})
        if password is None:
            return jsonify({'msg': login_password_not_message, 'code': 34, 'data': ''})
        user = User.query.filter_by(username=username).first()
        if user:
            if user.status is True:
                return jsonify({'msg': login_user_free_message, 'code': 35, 'data': ''})
            if user.check_password(password):
                user.is_login = True
                userlog = UserLoginlog(user=user.id, ip=ip, datatime=datetime.datetime.now())
                db.session.add_all([user, userlog])
                db.session.commit()
                login_user(user)
                session['username'] = username
                return jsonify({'msg': login_user_sucess_message, 'code': 200, 'data': ''})
            else:
                try:
                    num = int(self.conris.getset(user.username))
                    if (user.is_free == True and num > 5):
                        return jsonify({'msg': login_user_fremm, 'code': 200, 'data': ''})
                    else:
                        self.conris.sethase(username, num + 1, 1000 * 60 * 10)
                        return jsonify({'msg': login_password_error_message, 'code': 36, 'data': ''})
                except Exception as  e:
                    self.conris.sethase(username, 1, 1000 * 60 * 10)
                    return jsonify({'msg': login_password_error_message, 'code': 36, 'data': ''})
        return jsonify({'msg': login_user_not_exict_message, 'code': 37, 'data': ''})


class Logout(MethodView):
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
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for pros in current_user.quanxians:
                projects.append(pros.projects)
        return render_template('home/interface.html', projects=projects, models=models)

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
            new_interface = Interface(model_id=models_id, projects_id=project_id,
                                      Interface_name=name,
                                      Interface_url=url,
                                      Interface_meth=meth,
                                      Interface_user_id=current_user.id,
                                      Interface_headers=headers,
                                      interfacetype=xieyi)
            db.session.add(new_interface)
            db.session.commit()
            return jsonify({'data': interface_add_success, 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': interface_add_erroe, 'code': 3})

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        interface = Interface.query.filter_by(id=data, status=False).first()
        if not interface:
            return jsonify({"data": '删除接口不存在', 'code': 4})
        interface.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除接口失败，原因：%s' % e, 'code': 3})


class YongliView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for i in current_user.quanxians:
                projects.append(i.projects)
        return render_template('home/interface_yongli.html', projects=projects)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        testcase = InterfaceTest.query.filter_by(id=data).first()
        if not testcase:
            return jsonify({"data": '删除用例不存在', 'code': 4})
        try:
            testcase.status = True
            db.session.commit()
            return jsonify({"data": '删除用例成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除用例失败，原因：%s' % e, 'code': 3})


class AdminuserView(MethodView):
    @login_required
    def get(self):
        wrok = Work.query.all()
        projects = Project.query.filter_by(status=False).all()
        if current_user.is_sper == True:
            pagination = (User.query.order_by(User.id.desc()).all())
        else:
            pagination = []
            id = []
            for projec in current_user.quanxians:
                if (projec.user.all() in id) is False:
                    pagination.append(projec.user.all())
                    id.append(projec.user.all())
            pagination = (hebinglist(pagination))
        pager_obj = Pagination(request.args.get("page", 1), len(pagination), request.path, request.args,
                               per_page_count=PageShow)
        index_list = pagination[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('home/useradmin.html', users=index_list, html=html, wroks=wrok, projects=projects)

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
            return jsonify({'data': '用户已经存在！不能重复!', 'code': 10})
        emai = User.query.filter_by(user_email=str(email)).first()
        if emai:
            return jsonify({'data': '邮箱已经存在！请选个邮箱!', 'code': 11})
        wrok = Work.query.filter_by(name=work).first()
        new_user = User(username=name, user_email=email)
        new_user.set_password(password)
        new_user.work_id = wrok.id
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': '添加失败，原因：%s' % e, 'code': 3})
        if len(project) <= 0:
            return jsonify({'data': '成功', 'code': 2})
        else:
            try:
                user_id = User.query.filter_by(username=name).first()
                for proj in project:
                    project_one = Project.query.filter_by(project_name=proj).first()
                    quanxian = Quanxian(project=project_one.id, rose=1)
                    quanxian.user.append(user_id)
                    db.session.add(quanxian)
                db.session.commit()
                return jsonify({'data': '成功', 'code': 2})
            except Exception as e:
                db.session.rollback()
                return jsonify({'data': '添加失败，原因：%s' % e, 'code': 1})


class TestrepView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
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
        except:
            return redirect(url_for('home.test_rep'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        delTest = TestResult.query.filter_by(id=data, status=False).first()
        if not delTest:
            return jsonify({"data": '删除的测试报告不存在', 'code': 3})
        delTest.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除测试报告成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除测试报告失败！', 'code': 2})


class ProjectView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
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
            return jsonify({'code': 3, 'data': '权限不足！'})
        if name == '':
            return jsonify({'code': 4, 'data': '不能为空！'})
        projec = Project.query.filter_by(project_name=name, status=False).first()
        if projec:
            return jsonify({'code': 5, 'data': '项目不能重复！'})
        new_moel = Project(project_name=name, project_user_id=current_user.id)
        try:
            db.session.add(new_moel)
            db.session.commit()
            testgroup = TestGroup(adduser=current_user.id, addtime=datetime.datetime.now(),
                                  updatetime=datetime.datetime.now(), updateuser=current_user.id,
                                  name='黑名单', projectid=new_moel.id)
            db.session.add(testgroup)
            db.session.commit()
            return jsonify({'code': 2, 'data': '添加成功！', '': ''})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 7, 'data': '添加失败，原因:%s！' % e, })

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
            return jsonify({"data": '添加项目成功', 'code': 2})
        prohect.project_name = name
        try:
            db.session.commit()
            return jsonify({'code': 2, 'data': '编辑项目成功！'})
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 3, 'data': '编辑出现问题！原因：%s' % e})

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        proje = Project.query.filter_by(id=data, status=False).first()
        if not proje:
            return jsonify({"data": '删除项目不存在', 'code': 4})
        proje.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除失败', 'code': 3})


class ModelView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
            project_list = Project.query.filter_by(status=False).all()
        else:
            project_list = []
            for projec in current_user.quanxians:
                project_list.append(projec.projects)
        models = Model.query.filter_by(status=False).all()
        projects_lsit = fenye_list(Ob_list=models, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        pyth_post1 = projects_lsit[int(page) - 1]
        return render_template('home/model.html', projects=pyth_post1, pages=pages, project_list=project_list)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        model = Model.query.filter_by(id=data, status=False).first()
        if not model:
            return jsonify({"data": '模块不存在', 'code': 3})
        model.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除失败', 'code': 4})

    @login_required
    def post(self):
        data = request.get_json()
        models = Model.query.filter_by(model_name=data['name']).first()
        if data['project'] == '请选择':
            common = True
            project_one = None
        else:
            project_one = Project.query.filter_by(project_name=data['project']).first().id
            common = False
        if models:
            return jsonify({'code': 1, 'data': u'模块不能重复存在'})
        new_moel = Model(model_name=data['name'], model_user_id=current_user.id, common=common, project=project_one)
        db.session.add(new_moel)
        try:
            db.session.commit()
            return jsonify({'code': 2, 'data': u'添加成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 3, 'data': u'添加失败，原因：%s' % e})

    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        projec = json_data['project']
        edit_mode = Model.query.filter_by(id=id, status=False).first()
        if projec == '请选择':
            common = True
            project_one = None
        else:
            common = False
            project_one = Project.query.filter_by(status=False, project_name=projec).first().id
        if not edit_mode:
            mew = Model(model_name=name, model_user_id=current_user.id, common=common, project=project_one)
            db.session.add(mew)
            db.session.commit()
            return jsonify({'data': '编辑成功', 'code': 2})
        edit_mode.model_name = name
        edit_mode.common = common
        edit_mode.project = project_one
        try:
            db.session.commit()
            return jsonify({'data': '编辑模块成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': '编辑模块出现问题！原因：%s' % e, 'code': 308})


class TesteventVies(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
            events = []
            events.append(Interfacehuan.query.filter_by(status=False).order_by(Interfacehuan.id.desc()).all())
        else:
            events = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) == False:
                    events.append(
                        Interfacehuan.query.filter_by(project=project.projects.id, status=False).order_by(Project.id.desc()).all())
                    id.append(project.projects.id)
        projects_lsit = fenye_list(Ob_list=events, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = []
            for i in current_user.quanxians:
                if (i.projects in i) == False:
                    projects.append(i.projects)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/events.html', events=pyth_post1, pages=pages, projects=projects)
        except:
            return redirect(url_for('home.ceshihuanjing'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        event = Interfacehuan.query.filter_by(id=data).first()
        event.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code': 2})
        except Exception as e:
            return jsonify({"data": '删除失败', 'code': 4})

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
            return jsonify({"msg": u'测试环境必须是相互独立的', "code": 209, 'data': ''})
        prkcyt = Project.query.filter_by(project_name=project).first()
        end = Interfacehuan(url=url, desc=desc, project=prkcyt.id, database=name,
                            databaseuser=usernmae, databasepassword=password, dbhost=host,
                            dbport=port, make_user=current_user.id)
        db.session.add(end)
        try:
            db.session.commit()
            return jsonify({"data": u'添加测试环境成功!', "code": 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": u'添加测试用例失败！原因：%s' % e, "code": 211})

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
            end = Interfacehuan(url=url, desc=desc, project=project.id, database=name,
                                databaseuser=usernmae, databasepassword=password, dbhost=host,
                                dbport=port, make_user=current_user.id)
            db.session.add(end)
            db.session.commit()
            return jsonify({'data': '编辑成功', 'code': 2})
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
            return jsonify({'data': '编辑成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': '编辑失败！原因是:%s' % e, 'code': 321})


class MockViews(MethodView):
    @login_required
    def get(self, page=1):
        mock = Mockserver.query.filter_by(delete=False).order_by(Mockserver.id.desc()).paginate(page,
                                                                                 per_page=int(PageShow),
                                                                                 error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)

    @login_required
    def post(self):
        data_post = request.get_json()
        name_is = Mockserver.query.filter_by(name=data_post['name']).first()
        if name_is:
            return jsonify({"code": 28, 'data': 'mockserver的名称不能重复'})
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
            return jsonify({"code": 2, 'data': '添加mock成功'})
        except:
            db.session.rollback()
            return jsonify({"code": 29, 'data': '创建新的mock接口出错,原因：%s' % Exception})

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        ded = Mockserver.query.filter_by(id=data, status=False).first()
        if ded:
            ded.delete = True
            db.session.commit()
            return jsonify({'data': '删除成功', 'code': 2})
        return jsonify({'data': '删除失败，找不到mocksever', 'code': 3})


class TimingtasksView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper == True:
            task = []
            task.append(Task.query.filter_by(status=False).order_by(Task.id.desc()).all())
        else:
            task = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) == False:
                    task.append(Task.query.filter_by(prject=project.projects.id, status=False).all())
                    id.append(project.projects.id)
        old_yask = hebinglist(task)
        projects_lsit = fenye_list(Ob_list=old_yask, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/timingtask.html', inte=pyth_post1, pages=pages)
        except:
            return redirect(url_for('home.timingtask'))


class GettProtestreport(MethodView):
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not project:
            return jsonify({'msg': u'没有发送数据', 'code': 38, 'data': ''})
        project_is = Project.query.filter_by(project_name=project).first()
        if not project_is:
            return jsonify(({'msg': u'成功', 'code': 200, 'data': []}))
        testreport = TestResult.query.filter_by(projects_id=project_is.id, status=False).order_by(TestResult.id.desc()).all()
        testreportlist = []
        for test in testreport:
            testreportlist.append({'test_num': test.test_num, 'pass_num': test.pass_num,
                                   'fail_num': test.fail_num, 'hour_time': str(test.hour_time),
                                   'test_rep': test.test_rep, 'test_log': test.test_log,
                                   'Exception_num': test.Exception_num, 'can_num': test.can_num,
                                   'wei_num': test.wei_num, 'test_time': str(test.test_time),
                                   'Test_user_id': test.users.username, 'id': test.id,
                                   'fenshu': test.pass_num / test.test_num})
        return jsonify(({'msg': u'成功', 'code': 200, 'data': (testreportlist)}))


class JenkinsFirst(MethodView):
    @login_required
    def get(self):
        try:
            # tasks=Task.query.filter_by(makeuser=current_user.id,status=False).all()
            jobs = Conlenct_jenkins().get_all_job()
            jenkis_task = []
            for job in jobs:
                # for task in tasks:
                #   if job['name']==task.taskname:
                jenkis_task.append({'name': job['name'], 'url': job['url'],
                                    'color': job['color']})
            return render_template('home/jenkins.html', jobs=jenkis_task)
        except Exception as e:
            flash("无法连接jenkins服务器", category="error")
            return redirect(url_for('home.index'))


class JenkinsGou(MethodView):
    @login_required
    def get(self, jobname=''):
        goujian = Conlenct_jenkins().build_job(jobname)
        if goujian == True:
            flash('构建成功！', category="message")
            return redirect(url_for('home.jenkinsfirst'))
        else:
            flash('构建失败', category="message")
            return redirect(url_for('home.jenkinsfirst'))


class GetJenLogview(MethodView):
    @login_required
    def post(self):
        url = (request.get_data().decode('utf-8'))
        url_base = (url.split('&')[0])
        jobname = url.split('&')[1]
        try:
            log = Conlenct_jenkins().job_bulid_log(url_base, jobname)
            return jsonify({"code": 200, 'data': str(log)})
        except Exception as e:
            return jsonify({'code': 701, 'data': str(e)})


class DeleteJenkinstask(MethodView):
    @login_required
    def post(self, id):
        pass


class GenconfigView(MethodView):
    @login_required
    def get(self, page=1):
        genconfiglist = GeneralConfiguration.query.filter_by(status=False).order_by(GeneralConfiguration.id.desc()).all()
        projects_lsit = fenye_list(Ob_list=genconfiglist, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/genconfig.html', inte=pyth_post1, pages=pages)
        except:
            return redirect(url_for('home.genconfig'))


class DeleteGenconfi(MethodView):
    @login_required
    def get(self, id):
        gencofigilist = GeneralConfiguration.query.filter_by(id=id, status=False).first()
        if not gencofigilist:
            flash("配置已经删除或者不存在")
        gencofigilist.status = True
        try:
            db.session.commit()
            flash('删除配置成功')
            return redirect(url_for('home.genconfig'))
        except Exception as e:
            db.session.rollback()
            flash('删除配置失败！原因：%s' % e)
            return redirect(url_for('home.genconfig'))
