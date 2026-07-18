# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
import datetime

from flask import Blueprint, flash
import json
from common.list_utils import flatten_list
from flask import redirect, request, render_template, url_for, session
from sqlalchemy.orm import joinedload

from common.json_tools import response
from app.models import *
from app.forms import *
from flask.views import MethodView
from flask_login import login_required, login_user, \
    logout_user, current_user
from app import loginManager, sched, db
from common.list_paging import Pagination, fenye_list
from error_message import *
from common.redis_client import ConRedisOper  # noqa: F401 (保留以兼容其他模块导入)
from config import *
from common.system_log import logger

home = Blueprint('home', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class IndexView(MethodView):
    @login_required
    def get(self):
        interface_cont = Interface.query.filter_by(status=False).options(
            joinedload(Interface.projects)).all()
        interface_result = TestcaseResult.query.all()
        result_list_case = []
        for result in interface_result:
            result_list_case.append(result.case_id)
        all_run_case_count = len(set(result_list_case))
        interface_list = []
        for interface in interface_cont:
            try:
                if interface.projects.status is False:
                    interface_list.append(interface)
            except Exception as e:
                logger.exception(e)
        interfaceTest_cunt = InterfaceTest.query.filter_by(status=False).all()
        case_list = []
        for case in interfaceTest_cunt:
            try:
                if case.projects.status is False:
                    case_list.append(case)
            except Exception as e:
                logger.exception(e)
        resu_cout = TestResult.query.filter_by(status=False).all()
        reslut_list = []
        for result in resu_cout:
            try:
                if result.projects.status is False:
                    reslut_list.append(result)
            except Exception as e:
                logger.exception(e)
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
        form = LoginForm()
        return render_template('home/login.html', form=form)

    def post(self):
        data = request.get_json()
        if data is None:
            return response(message=MessageEnum.login_username_not_message.value[1],
                           code=MessageEnum.login_username_not_message.value[0],
                           data='')
        ip = request.remote_addr
        username = data['username']
        password = data['password']
        if username is None:
            return response(message=MessageEnum.login_username_not_message.value[1],
                           code=MessageEnum.login_username_not_message.value[0],
                           data="")
        if password is None:
            return response(message=MessageEnum.login_password_not_message.value[1],
                           code=MessageEnum.login_password_not_message.value[0],
                           data='')
        user = User.query.filter_by(username=username).first()
        if not user:
            return response(message=MessageEnum.login_user_not_exist_message.value[1],
                           code=MessageEnum.login_user_not_exist_message.value[0],
                           data='')
        user_err_num = user.err_num
        if (user.jobnum == "None" or user.jobnum is None):
            return response(message=MessageEnum.login_user_inactive.value[1],
                           code=MessageEnum.login_user_inactive.value[0],
                           data='')
        if user:
            if user.status is True:
                return response(message=MessageEnum.login_user_freeze_message.value[1],
                               code=MessageEnum.login_user_freeze_message.value[0],
                               data='')
            if password and user.check_password(password):
                if (user.is_free == True and user.freetime != None and user.err_num > 6 and (
                        datetime.datetime.now() - user.freetime).min > 10):
                    return response(
                        message=MessageEnum.login_password_error_exceed_limit.value[1],
                        code=MessageEnum.login_password_error_exceed_limit.value[0],
                        data='')
                user.is_login = True
                userlog = UserLoginlog(user=user.id,
                                       ip=ip,
                                       datatime=datetime.datetime.now())
                db.session.add_all([user, userlog])
                db.session.commit()
                login_user(user)
                session['username'] = username
                return response(message=MessageEnum.login_user_success_message.value[1],
                               code=MessageEnum.login_user_success_message.value[0],
                               data='')
            else:
                num = user.err_num != None and user.err_num >= 5
                if num:
                    if (user.freetime != 'None' and user.freetime is not None ):
                        if (datetime.datetime.now() - user.freetime).min > 10:
                            user.err_num = user_err_num + 1
                            db.session.add(user)
                            db.session.commit()
                            return response(message=MessageEnum.login_password_error_message.value[1],
                                           code=MessageEnum.login_password_error_message.value[0],
                                           data='')
                        else:
                            user.err_num = 5
                            user.freetime = datetime.datetime.now()
                            user.is_free = True
                            db.session.add(user)
                            db.session.commit()
                            return response(message=MessageEnum.login_password_error_exceed_limit.value[1],
                                           code=MessageEnum.login_password_error_exceed_limit.value[0], data='')
                    else:
                        if user.err_num == None:
                            user.err_num = 0
                        else:
                            user.err_num = user_err_num + 1
                        db.session.add(user)
                        db.session.commit()
                        return response(message=MessageEnum.login_password_error_message.value[1],
                                       code=MessageEnum.login_password_error_message.value[0], data='')
                else:
                    if user.err_num == None:
                        user.err_num = 0
                    else:
                        user.err_num = user_err_num + 1
                    db.session.add(user)
                    db.session.commit()
                    return response(message=MessageEnum.login_password_error_message.value[1],
                                   code=MessageEnum.login_password_error_message.value[0], data='')
        return response(message=MessageEnum.login_user_not_exist_message.value[1],
                       code=MessageEnum.login_user_not_exist_message.value[0],
                       data='')


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



