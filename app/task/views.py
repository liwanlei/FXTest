# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
from flask import Blueprint
from flask import redirect, request, render_template, url_for, flash
from app.models import *
from flask.views import MethodView
from flask_login import current_user, login_required
from app import loginManager, sched
import time, os
from common.htmltestreport import createHtml
from app.test_case.Test_case import ApiTestCase
from common.mergelist import listmax
from common.Dingtalk import send_ding
from config import Dingtalk_access_token
from error_message import *
from common.jsontools import reponse
from common.systemlog import logger

task = Blueprint('task', __name__)


def addtask(id):  # 定时任务执行的时候所用的函数
    in_id = int(id)
    task = Task.query.filter_by(id=in_id, status=False).first()
    starttime = datetime.datetime.now()
    star = time.time()
    day = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    pad = os.getcwd()
    file_dir = pad + '/app/upload'
    file = os.path.join(file_dir, (day + '.log'))
    if os.path.exists(file) is False:
        os.system('touch %s' % file)
    filepath = os.path.join(file_dir, (day + '.html'))
    if os.path.exists(filepath) is False:
        os.system(r'touch %s' % filepath)
    projecct_list = []
    model_list = []
    Interface_name_list = []
    Interface_url_list = []
    Interface_meth_list = []
    Interface_pase_list = []
    Interface_assert_list = []
    Interface_headers_list = []
    Interface_pid_list = []
    Interface_yilai_list = []
    Interface_save_list = []
    Interface_is_data_list = []
    Interface_mysql_list = []
    Interface_msyql_ziduan_list = []
    id_list = []
    for task_yongli in task.interface.all():
        id_list.append(task_yongli.id)
        projecct_list.append(task_yongli.projects)
        model_list.append(task_yongli.models)
        Interface_is_data_list.append(task_yongli.is_database)
        Interface_mysql_list.append(task_yongli.chaxunshujuku)
        Interface_msyql_ziduan_list.append(task_yongli.databaseziduan)
        Interface_url_list.append(task_yongli.Interface_url)
        Interface_name_list.append(task_yongli.Interface_name)
        Interface_meth_list.append(task_yongli.Interface_meth)
        Interface_pase_list.append(task_yongli.Interface_pase)
        Interface_assert_list.append(task_yongli.Interface_assert)
        Interface_headers_list.append(task_yongli.Interface_headers)
        Interface_pid_list.append(task_yongli.pid)
        Interface_yilai_list.append(task_yongli.getattr_p)
        Interface_save_list.append(task_yongli.saveresult)
    testevent = task.testevent
    intest = Interfacehuan.query.filter_by(id=testevent, status=False).first()
    apitest = ApiTestCase(inteface_url=Interface_url_list,
                          inteface_method=Interface_meth_list,
                          inteface_parme=Interface_pase_list,
                          inteface_assert=Interface_assert_list,
                          file=file, headers=Interface_headers_list,
                          pid=Interface_pid_list,
                          is_database=Interface_is_data_list,
                          data_mysql=Interface_mysql_list,
                          data_field=Interface_msyql_ziduan_list,
                          urltest=intest.url,
                          replydata=Interface_yilai_list,
                          saveresult=Interface_save_list, id_list=id_list)
    result_toal, result_pass, result_fail, relusts, \
    bask_list, result_cashu, result_wei, result_except, \
    spendlist = apitest.testapi()
    large, small, pingjun = listmax(spendlist)
    endtime = datetime.datetime.now()
    end = time.time()
    createHtml(titles=u'定时任务接口测试报告', filepath=filepath,
               starttime=starttime, endtime=endtime,
               passge=result_pass, fail=result_fail, id=id_list,
               name=projecct_list,
               headers=Interface_headers_list, coneent=Interface_url_list,
               url=Interface_meth_list,
               meth=Interface_pase_list, yuqi=Interface_assert_list,
               json=bask_list, relusts=relusts,
               excepts=result_except, yuqis=result_cashu,
               weizhi=result_wei, maxs=large, mins=small,
               pingluns=pingjun)
    hour = end - star
    new_reust = TestResult(Test_user_id=1, test_num=result_toal,
                           pass_num=result_pass,
                           fail_num=result_fail, test_time=starttime,
                           hour_time=hour,
                           test_rep=(day + '.html'), test_log=(day + '.log'),
                           Exception_num=result_except,
                           can_num=result_cashu, wei_num=result_wei,
                           projects_id=projecct_list[0].id)
    db.session.add(new_reust)
    db.session.commit()
    try:
        send_ding(content="多用例测试已经完成，通过用例：%s，失败用例：%s，详情见测试报告" % (result_pass, result_fail),
                  Dingtalk_access_token=Dingtalk_access_token)
    except Exception as e:

        print(e)
        # flash('定时任务的钉钉消息发送失败！原因:%s' % e)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TestforTaskView(MethodView):  # 为测试任务添加测试用例

    @login_required
    def get(self, id):
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            ids = []
            for i in current_user.quanxians:
                if (i.projects in ids) is False:
                    if i.projects.status is False:
                        projects.append(i.projects)
                        ids.append(i.projects)
        task_one = Task.query.filter_by(id=id).first()
        return render_template('add/addtestcasefortask.html',
                               task_one=task_one, procjets=projects)

    @login_required
    def post(self, id):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) is False:
                    if i.projects.status is False:
                        projects.append(i.projects)
                        id.append(i.projects)
        task_one = Task.query.filter_by(id=id).first()
        procject_test = request.form.get('project')
        if procject_test == '':
            flash(MessageEnum.not_add_project.value[1])
            return render_template('add/addtestcasefortask.html', task_one=task_one, procjets=projects)
        test_yongli = request.form.getlist('testyongli')
        if test_yongli == '':
            flash(MessageEnum.project_not_case.value[1])
            return render_template('add/addtestcasefortask.html', task_one=task_one, procjets=projects)
        for oldtask in task_one.interface.all():
            task_one.interface.remove(oldtask)
        for yongli in test_yongli:
            task_yong = InterfaceTest.query.filter_by(id=yongli).first()
            if task_yong.status is True:
                continue
            else:
                task_one.interface.append(task_yong)
        task_one.prject = procject_test
        db.session.add(task_one)
        try:
            db.session.commit()
            flash(MessageEnum.task_update_case.value[1])
            return redirect(url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            flash(MessageEnum.task_update_case_error.value[1])
            return redirect(url_for('home.timingtask'))


class StartTaskView(MethodView):  # 开始定时任务
    @login_required
    def get(self, id):
        task = Task.query.filter_by(id=id).first()
        if len(task.interface.all()) <= 1:
            flash(MessageEnum.task_must_be_mulite_case.value[1])
            return redirect(url_for('home.timingtask'))
        try:
            time_start = eval(task.taskstart)
            day_week = time_start['day_of_week']
            hour = time_start['hour']
            mindes = time_start['minute']
            sched.add_job(func=addtask, id=str(id), args=[str(id)],
                          trigger='cron',
                          day_of_week=day_week, hour=hour,
                          minute=mindes, jobstore='redis',
                          replace_existing=True)
            task.yunxing_status = '启动'
            db.session.commit()
            flash(MessageEnum.task_start_success.value[1])
            return redirect(url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            flash(MessageEnum.task_start_eeor.value[1])
            return redirect(url_for('home.timingtask'))


class PausedTaskView(MethodView):  # 暂停定时任务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        task = Task.query.filter_by(id=id).first()
        try:
            sched.pause_job(str(id))
            task.yunxing_status = u'暂停'
            db.session.commit()
            flash(u'！')
            return redirect(next or url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(MessageEnum.task_stop_fail.value[1])
            return redirect(next or url_for('home.timingtask'))


class RecoverTaskView(MethodView):  # 回复定时任务
    @login_required
    def get(self, id):
        task = Task.query.filter_by(id=id).first()
        next = request.headers.get('Referer')
        try:
            sched.resume_job(str(id))
            task.yunxing_status = u'启动'
            db.session.commit()
            flash(MessageEnum.task_repuse_success.value[1])
            return redirect(next or url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(MessageEnum.task_repuse_fail.value[1])
            return redirect(next or url_for('home.timingtask'))


class RemoveTaskView(MethodView):  # 移除定时任务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        task = Task.query.filter_by(id=id).first()
        try:
            sched.remove_job(str(id))
            task.yunxing_status = u'关闭'
            db.session.commit()
            flash(MessageEnum.remove_success.value[1])
            return redirect(next or url_for('home.timingtask'))
        except Exception as  e:
            logger.exception(e)
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(MessageEnum.remove_fail.value[1])
            return redirect(next or url_for('home.timingtask'))


class AddTimingTaskView(MethodView):
    @login_required
    def get(self):
        project = Project.query.filter_by(status=False).all()
        return render_template('add/addtimingtasks.html', projects=project)

    @login_required
    def post(self):
        data = request.get_json()
        task_time = {'type': 'cron', 'day_of_week': data['week'],
                     'hour': data['hour'], 'minute': data['minx']}
        taskname_is = Task.query.filter_by(taskname=data['taskname']).first()
        testevent = Interfacehuan.query.filter_by(url=data['testevent']).first()
        if not testevent:
            return reponse(
                code=MessageEnum.task_event_not_exict.value[0],
                message=MessageEnum.task_event_not_exict.value[1],
                data='')
        if taskname_is:
            return reponse(
                code=MessageEnum.task_name_not_same.value[0],
                message=MessageEnum.task_name_not_same.value[1],
                data='')
        procjt = Project.query.filter_by(project_name=data['projects'], status=False).first()
        if not procjt:
            return reponse(code=MessageEnum.task_project_is_not_exict.value[0],
                           message=MessageEnum.task_project_is_not_exict.value[1], data='')
        new_task = Task(taskname=data['taskname'], taskstart=str(task_time),
                        taskrepor_to=data['to_email'], taskrepor_cao=data['cao_email'],
                        task_make_email=data['weihu'], makeuser=current_user.id,
                        prject=procjt.id, testevent=testevent.id)
        db.session.add(new_task)
        try:
            return reponse(code=MessageEnum.successs.value[0], message=MessageEnum.successs.value[1], data='')
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(
                code=MessageEnum.task_add_fail.value[0], message=MessageEnum.task_add_fail.value[1], data='')


class EdiTmingTaskView(MethodView):
    @login_required
    def get(self, id):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) is False:
                    if i.projects.status is False:
                        projects.append(i.projects)
                        id.append(i.projects)
        task_one = Task.query.filter_by(id=id).first()
        if not task_one:
            flash(MessageEnum.task_edit_not_exict.value[1])
            return redirect(url_for('home.timingtask'))
        return render_template('edit/Edittimingtasks.html',
                               task_one=task_one, porjects=projects)

    @login_required
    def post(self, id):
        task_one = Task.query.filter_by(id=id).first()
        taskname = request.form['taskname']
        to_email_data = request.form['to_email']
        cao_email = request.form['cao_email']
        week = request.form['week']
        hour = request.form['hours']
        minute = request.form['minute']
        task_time = {'type': 'cron', 'day_of_week': week, 'hour': hour, 'minute': minute}
        weihu = request.form['weihu']
        if taskname == '':
            flash(MessageEnum.task_name_not_none.value[1])
            return render_template('add/addtimingtasks.html')
        if to_email_data == '':
            flash(MessageEnum.task_recevier.value[1])
            return render_template('add/addtimingtasks.html')
        if weihu == '':
            flash(MessageEnum.task_user.value[1])
            return render_template('add/addtimingtasks.html')
        task_one.taskname = taskname
        task_one.taskrepor_to = to_email_data
        task_one.taskrepor_cao = cao_email
        task_one.task_make_email = weihu
        task_one.makeuser = current_user.id
        task_one.taskstart = str(task_time)
        try:
            db.session.commit()
            flash(MessageEnum.task_edit.value[1])
            return redirect(url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.task_edit_fail.value[1])
            return redirect(url_for('home.timingtask'))


class DeteleTaskView(MethodView):
    def get(self, id):
        next = request.headers.get('Referer')
        task_one = Task.query.filter_by(id=id).first()
        if not task_one:
            flash(MessageEnum.delete_not_exict.value[1])
            return redirect(next or url_for('home.timingtask'))
        if task_one.status is True:
            flash(MessageEnum.task_is_delete.value[1])
            return redirect(next or url_for('home.timingtask'))
        task_one.status = True
        try:
            db.session.commit()
            flash(MessageEnum.task_delete_success.value[1])
            return redirect(next or url_for('home.timingtask'))
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.task_delete_fail.value[1])
            return redirect(next or url_for('home.timingtask'))


class GetTestView(MethodView):
    @login_required
    def post(self):
        project = request.get_data('value')
        project = project.decode('utf-8')
        changpr = Project.query.filter_by(project_name=project).first()
        if not changpr:
            return reponse(
                code=MessageEnum.project_search.value[0], message=MessageEnum.project_search.value[1], data='')
        if changpr.status == True:
            return reponse(
                code=MessageEnum.project_delet_free.value[0], message=MessageEnum.project_delet_free.value[1],
                data='')
        testevent = Interfacehuan.query.filter_by(projects=changpr, status=False).all()
        testeventlist = []
        for testeven in testevent:
            testeventlist.append({"url": testeven.url})
        return reponse(
            code=MessageEnum.successs.value[0], data=testeventlist, message=MessageEnum.successs.value[1])
