# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:19
from flask import  Blueprint,jsonify
from  flask import  redirect,request,render_template,url_for,flash
from app.models import *
from flask.views import MethodView
from flask_login import current_user,login_required
from app import loginManager
import  time,os
from common.py_Html import createHtml
from app.test_case.Test_case import ApiTestCase
from app import  scheduler
from common.Dingtalk import send_ding
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
    testevent=task.testevent
    apitest = ApiTestCase(inteface_url=Interface_url_list, inteface_meth=Interface_meth_list,
                          inteface_parm=Interface_pase_list,inteface_assert=Interface_assert_list,
                          file=file, headers=Interface_headers_list,pid=Interface_pid_list,is_database=Interface_is_data_list,
                           data_mysql=Interface_mysql_list,data_ziduan=Interface_msyql_ziduan_list,urltest=testevent,
                          yilaidata=Interface_yilai_list, saveresult=Interface_save_list, id_list=id_list)
    result_toal, result_pass, result_fail, relusts, bask_list, result_cashu, result_wei, result_except = apitest.testapi()
    endtime = datetime.datetime.now()
    end = time.time()
    createHtml(titles=u'定时任务接口测试报告', filepath=filepath, starttime=starttime, endtime=endtime,
               passge=result_pass, fail=result_fail, id=id_list, name=projecct_list,
               headers=Interface_headers_list, coneent=Interface_url_list, url=Interface_meth_list,
               meth=Interface_pase_list, yuqi=Interface_assert_list, json=bask_list, relusts=relusts,
               excepts=result_except, yuqis=result_cashu, weizhi=result_wei)
    hour = end - star
    user_id = User.query.filter_by(role_id=2).first().id
    new_reust = TestResult(Test_user_id=user_id, test_num=result_toal, pass_num=result_pass,
                           fail_num=result_fail, test_time=starttime, hour_time=hour,
                           test_rep=(day + '.html'), test_log=(day + '.log'), Exception_num=result_except,
                           can_num=result_cashu, wei_num=result_wei)
    db.session.add(new_reust)
    db.session.commit()
    try:
        send_ding(content="%s定时任务执行完毕，测试时间：%s，\\n 通过用例：%s，失败用例：%s，\\n,详情见测试平台测试报告！" % (
        task.taskname, starttime, result_pass, result_fail))
    except Exception as e:
        flash('定时任务的钉钉消息发送失败！原因:%s'%e)
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
        for yongli in test_yongli:
            task_yong=InterfaceTest.query.filter_by(id=(yongli)).first()
            task_one.interface.append(task_yong)
        task_one.prject = proc_test
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
        if len(task.interface.all())<=1:
            flash(u'定时任务执行过程的测试用例为多用例，请你谅解')
            return  redirect(url_for('home.timingtask'))
        try:
            scheduler.add_job(func=addtask, id=str(id), args=str(id),trigger=eval(task.taskstart),replace_existing=True)
            task.yunxing_status='启动'
            db.session.commit()
            flash(u'定时任务启动成功！')
            return  redirect(url_for('home.timingtask'))
        except Exception as e:
            flash(u'定时任务启动失败！原因：%e'%e)
            return redirect(url_for('home.timingtask'))
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
        except Exception as e:
            task.yunxing_status = u'创建'
            db.session.commit()
            flash(u'定时任务暂停失败！已经为您初始化，原因：%s'%e)
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
        project=Project.query.filter_by(status=False).all()
        return  render_template('add/addtimingtasks.html',projects=project)
    @login_required
    def post(self):
        data=request.get_json()
        taskname_is = Task.query.filter_by(taskname=data['taskname']).first()
        testevent=Interfacehuan.query.filter_by(url=data['testevent']).first()
        if not testevent:
            return jsonify({'code': 337, 'msg': '任务的测试环境不存在', 'data': ''})
        if taskname_is:
            return jsonify({'code':330,'msg':'任务名不能重复','data':''})
        procjt=Project.query.filter_by(project_name=data['projects'],status=False).first()
        if not  procjt:
            return jsonify({'code': 338, 'msg': '任务的所属项目不存在', 'data': ''})
        new_task=Task(taskname=data['taskname'],taskstart=data['time'],taskrepor_to=data['to_email'],taskrepor_cao=data['cao_email'],task_make_email=data['weihu'],
                      makeuser=current_user.id,prject=procjt.id,testevent=testevent.id)
        db.session.add(new_task)
        try:
            return jsonify({'code': 200, 'msg': '成功', 'data': ''})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 331, 'msg': '任务添加失败，原因：%s'%e, 'data': ''})
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
            flash(u'删除任务出现异常，系统已经为你还原')
            return redirect(next or url_for('home.timingtask'))
class GettesView(MethodView):
    @login_required
    def post(self):
        project=request.get_data('value')
        project=project.decode('utf-8')
        changpr=Project.query.filter_by(project_name=project).first()
        if not changpr :
            return  jsonify({"code":231,'msg':'项目查询不到'})
        if changpr.status==True:
            return  jsonify({"code":232,'msg':'项目已经删除或者冻结'})
        testevent=Interfacehuan.query.filter_by(projects=changpr,status=False).all()
        testeventlist=[]
        for testeven in testevent:
            testeventlist.append({"url":testeven.url})
        return  jsonify({'code':200,'data':testeventlist,'msg':'请求成功'})