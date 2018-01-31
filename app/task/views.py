# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:19
from flask import  Blueprint
from  flask import  redirect,request,render_template,url_for,flash
from app.models import *
from flask.views import MethodView
from flask_login import current_user,login_required
from app import loginManager
import  time,os
from app.common.py_Html import createHtml
from app.test_case.Test_case import ApiTestCase
from app import  scheduler
from app.common.Dingtalk import send_ding
task = Blueprint('task', __name__)
def addtask(id):#定时任务执行的时候所用的函数
    in_id=int(id)
    task=Task.query.filter_by(id=in_id).first()
    starttime = datetime.datetime.now()
    star = time.time()
    day = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, 'upload')
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
    id_list = []
    for task_yongli in task.interface.all():
        id_list.append(task_yongli.id)
        projecct_list.append(task_yongli.projects)
        model_list.append(task_yongli.models)
        Interface_url_list.append(task_yongli.Interface_url)
        Interface_name_list.append(task_yongli.Interface_name)
        Interface_meth_list.append(task_yongli.Interface_meth)
        Interface_pase_list.append(task_yongli.Interface_pase)
        Interface_assert_list.append(task_yongli.Interface_assert)
        Interface_headers_list.append(task_yongli.Interface_headers)
    apitest = ApiTestCase(Interface_url_list, Interface_meth_list, Interface_pase_list, Interface_assert_list, file,
                          Interface_headers_list)
    result_toal, result_pass, result_fail, relusts, bask_list = apitest.testapi()
    endtime = datetime.datetime.now()
    end = time.time()
    createHtml(titles=u'接口测试报告', filepath=filepath, starttime=starttime, endtime=endtime, passge=result_pass,
               fail=result_fail, id=id_list, name=projecct_list, headers=Interface_headers_list,
               coneent=Interface_url_list, url=Interface_meth_list, meth=Interface_pase_list,
               yuqi=Interface_assert_list, json=bask_list, relusts=relusts)
    hour = end - star
    user_id = User.query.filter_by(role_id=2).first().id
    new_reust = TestResult(Test_user_id=user_id, test_num=result_toal, pass_num=result_pass, fail_num=result_fail,
                           test_time=starttime, hour_time=hour, test_rep=(day + '.html'), test_log=(day + '.log'))
    db.session.add(new_reust)
    db.session.commit()
    send_ding(content="%s定时任务执行完毕，测试时间：%s，\\n 通过用例：%s，失败用例：%s，\\n,详情见测试平台测试报告！" % (
        task.taskname, starttime, result_pass, result_fail))
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class TestforTaskView(MethodView):#为测试任务添加测试用例
    @login_required
    def get(self,id):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        task_one=Task.query.filter_by(id=id).first()
        return  render_template('add/addtestyongfortask.html', task_one=task_one, procjets=projects)
    @login_required
    def post(self,id):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        task_one = Task.query.filter_by(id=id).first()
        proc_test=request.form.get('project')
        if proc_test =='':
            flash(u'不能不添加测试项目！')
            return render_template('add/addtestyongfortask.html', task_one=task_one, procjets=projects)
        test_yongli=request.form.getlist('testyongli')
        if test_yongli=='':
            flash(u'亲你见过只有测试项目没有测试用例的测试任务吗！')
            return render_template('add/addtestyongfortask.html', task_one=task_one, procjets=projects)
        for oldtask in task_one.interface.all():
            task_one.interface.remove(oldtask)
        task_one.prject=Project.query.filter_by(project_name=proc_test).first().id
        for yongli in test_yongli:
            task_one.interface.append(InterfaceTest.query.filter_by(id=yongli).first())
            db.session.add(task_one)
        try:
            db.session.commit()
            flash(u'任务更新用例成功')
            return  redirect(url_for('home.timingtask'))
        except:
            flash(u'任务更新用例失败')
            return redirect(url_for('home.timingtask'))
class StartTaskView(MethodView):#开始定时任务
    @login_required
    def get(self,id):
        task=Task.query.filter_by(id=id).first()
        next = request.headers.get('Referer')
        if len(task.interface.all())<=1:
            flash(u'定时任务执行过程的测试用例为多用例，请你谅解')
            return  redirect(next or url_for('home.timingtask'))
        try:
            scheduler.add_job(func=addtask, id=str(id), args=str(id),trigger=eval(task.taskstart),replace_existing=True)
            task.yunxing_status=u'启动'
            db.session.commit()
            flash(u'定时任务启动成功！')
            return  redirect(next or url_for('home.timingtask'))
        except Exception as e:
            flash(u'定时任务启动失败！请检查任务的各项内容各项内容是否正常')
            return redirect(next or url_for('home.timingtask'))
class ZantingtaskView(MethodView):#暂停定时任务
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        task = Task.query.filter_by(id=id).first()
        try:
            scheduler.pause_job(str(id))
            task.yunxing_status = u'暂停'
            db.session.commit()
            flash(u'定时任务暂停成功！')
            return redirect(next or url_for('home.timingtask'))
        except:
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(u'定时任务暂停失败！已经为您初始化')
            return redirect(next or url_for('home.timingtask'))
class HuifutaskView(MethodView):#回复定时任务
    @login_required
    def get(self,id):
        task = Task.query.filter_by(id=id).first()
        next = request.headers.get('Referer')
        try:
            scheduler.resume_job(str(id))
            task.yunxing_status=u'启动'
            db.session.commit()
            flash(u'定时任务恢复成功！')
            return redirect(next or url_for('home.timingtask'))
        except:
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(u'定时任务恢复失败！已经为您初始化')
            return redirect(next or url_for('home.timingtask'))
class YichuTaskView(MethodView):#移除定时任务
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        task = Task.query.filter_by(id=id).first()
        try:
            scheduler.delete_job(str(id))
            task.yunxing_status=u'关闭'
            db.session.commit()
            flash(u'定时任务移除成功！')
            return redirect(next or url_for('home.timingtask'))
        except:
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(u'定时任务移除失败！已经为您初始化')
            return redirect(next or url_for('home.timingtask'))
class AddtimingtaskView(MethodView):
    @login_required
    def get(self):
        return  render_template('add/addtimingtasks.html')
    @login_required
    def post(self):
        taskname=request.form['taskname']
        tinmingtime=request.form['time']
        to_email_data=request.form['to_email']
        cao_email=request.form['cao_email']
        weihu=request.form['weihu']
        if taskname =='':
            flash(u'任务名不能为空！')
            return render_template('add/addtimingtasks.html')
        if tinmingtime =='':
            flash(u'任务执行时间不能为空！')
            return render_template('add/addtimingtasks.html')
        if to_email_data=='':
            flash(u'发送给谁邮件不能为空！')
            return render_template('add/addtimingtasks.html')
        if weihu=='':
            flash(u'维护人邮件不能为空！')
            return render_template('add/addtimingtasks.html')
        taskname_is = Task.query.filter_by(taskname=taskname).first()
        if taskname_is:
            flash(u'任务已经存在请重新填写！')
            return render_template('add/addtimingtasks.html')
        new_task=Task(taskname=taskname,taskstart=tinmingtime,taskrepor_to=to_email_data,taskrepor_cao=cao_email,task_make_email=weihu,
                      makeuser=current_user.id)
        db.session.add(new_task)
        try:
            db.session.commit()
            flash(u'添加定时任务成功')
            return  redirect(url_for('home.timingtask'))
        except Exception as e:
            db.session.rollback()
            flash(u'添加过程貌似异常艰难！')
            return redirect(url_for('home.addtimingtasks'))
class Editmingtaskview(MethodView):
    @login_required
    def get(self,id):
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) == False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        task_one=Task.query.filter_by(id=id).first()
        if not task_one:
            flash(u'你编辑的不存在')
            return  redirect(url_for('home.timingtask'))
        return  render_template('edit/Edittimingtasks.html', task_one=task_one, porjects=projects)
    def post(self,id):
        task_one = Task.query.filter_by(id=id).first()
        taskname = request.form['taskname']
        tinmingtime = request.form['time']
        to_email_data = request.form['to_email']
        cao_email = request.form['cao_email']
        weihu = request.form['weihu']
        if taskname =='':
            flash(u'任务名不能为空！')
            return render_template('add/addtimingtasks.html')
        if tinmingtime =='':
            flash(u'任务执行时间不能为空！')
            return render_template('add/addtimingtasks.html')
        if to_email_data=='':
            flash(u'发送给谁邮件不能为空！')
            return render_template('add/addtimingtasks.html')
        if weihu=='':
            flash(u'维护人邮件不能为空！')
            return render_template('add/addtimingtasks.html')
        task_one.taskname=taskname
        task_one.taskrepor_to=to_email_data
        task_one.taskrepor_cao=cao_email
        task_one.task_make_email=weihu
        task_one.makeuser=current_user.id
        try:
            db.session.commit()
            flash(u'编辑成功')
            return  redirect(url_for('home.timingtask'))
        except:
            db.session.rollback()
            flash(u'编辑出现问题！')
            return redirect(url_for('home.timingtask'))
class DeteleTaskViee(MethodView):
    def get(self,id):
        next = request.headers.get('Referer')
        task_one = Task.query.filter_by(id=id).first()
        if not task_one:
            flash(u'你删除的不存在')
            return redirect(next or url_for('home.timingtask'))
        if task_one.status is True:
            flash(u'已经删除')
            return redirect(next or url_for('home.timingtask'))
        task_one.status=True
        try:
            db.session.commit()
            flash(u'删除任务成功')
            return redirect(next or url_for('home.timingtask'))
        except:
            db.session.rollback()
            flash(u'删除任务休息了')
            return redirect(next or url_for('home.timingtask'))