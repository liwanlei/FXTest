# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import  Blueprint,jsonify
from app.common.hebinglist import hebinglist
from  flask import  redirect,request,render_template,url_for,flash,session
home = Blueprint('home', __name__)
import json
from app.models import *
from app.form import  *
from flask.views import MethodView,View
from flask_login import login_required,login_user,logout_user,current_user
from app import loginManager
from config import PageShow
from app.common.fenye import Pagination
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Indexview(MethodView):#首页
    @login_required
    def get(self):
        interface_cont=Interface.query.count()
        interfaceTest_cunt=InterfaceTest.query.count()
        resu_cout=TestResult.query.count()
        project_cout=Project.query.count()
        model_cout=Model.query.count()
        return  render_template('home/index.html', yongli=interfaceTest_cunt, jiekou=interface_cont, report=resu_cout, project_cout=project_cout, model_cout=model_cout)
class LoginView(MethodView):#登录
    def get(self):
        form=LoginFrom()
        return render_template('home/login.html', form=form)
    def post(self):
        form=LoginFrom()
        username=request.form.get('username')
        password=request.form.get('password')
        if username =='':
            flash(u'用户名不能为空')
            return render_template('home/login.html', form=form)
        if password =='':
            flash(u'密码不能时空！')
            return render_template('home/login.html', form=form)
        user=User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password=password) is True:
                if user.status ==0:
                    login_user(user)
                    session['username']=username
                    next =request.args.get('next')
                    return  redirect(next or url_for('home.index'))
                flash(u'用户冻结，请联系管理员')
                return render_template('home/login.html', form=form)
            flash(u'用户名密码错误')
            return render_template('home/login.html', form=form)
        flash(u'用户名不存在')
        return  render_template('home/login.html', form=form)
class LogtView(MethodView):#退出
    def get(self):
        session.clear()
        logout_user()
        return redirect(url_for('home.login'))
class InterfaceView(MethodView):#接口
    @login_required
    def get(self,page=1):
        if current_user.is_sper==True:
            resylt=(Interface.query.filter_by(status=False).order_by('-id').all())
        else:
            resylt=[]
            id =[]
            for pros in current_user.quanxians:
                if not (pros.projects.id in id):
                    pagination=Interface.query.filter(Interface.projects_id==pros.projects.id,Interface.status==False).all()
                    id.append(pros.projects.id)
                    resylt.append(pagination)
            resylt = hebinglist(resylt)
        pager_obj = Pagination(request.args.get("page", 1), len(resylt), request.path, request.args,
                               per_page_count=PageShow)
        index_list = resylt[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return  render_template('home/interface.html', inte=index_list,html = html)
class YongliView(MethodView):
    @login_required
    def get(self,page=1):
        projecs,models=get_pro_mo()
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    projects.append(i.projects)
                    id.append(i.projects)
        if current_user.is_sper==True:
            resylt=InterfaceTest.query.filter_by(status=False).order_by('-id').all()
        else:
            resylt =[]
            id=[]
            for projec in current_user.quanxians:
                if not (projec.projects.id in id):
                    resylt.append(InterfaceTest.query.filter(InterfaceTest.projects_id==projec.projects.id,InterfaceTest.status==0).all())
                    id.append(projec.projects.id)
            resylt=hebinglist(resylt)
        pager_obj = Pagination(request.args.get("page", 1), len(resylt), request.path, request.args, per_page_count=PageShow)
        index_list = resylt[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return  render_template('home/interface_yongli.html',index_list=index_list, html = html,models=models,projects=projects)
class AdminuserView(MethodView):
    @login_required
    def get(self):
        if current_user.is_sper == True:
            pagination=(User.query.order_by('-id').all())
        else:
            pagination=[]
            id=[]
            for projec in current_user.quanxians:
                if (projec.user.all() in id) is False:
                    pagination.append(projec.user.all())
                    id.append(projec.user.all())
            pagination=(hebinglist(pagination))
        pager_obj = Pagination(request.args.get("page", 1), len(pagination), request.path, request.args,
                               per_page_count=PageShow)
        index_list = pagination[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('home/useradmin.html', users=index_list,html=html)
class TestrepView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper == True:
            project=Project.query.filter_by(status=False).all()
        else:
            project=[]
            for projec in current_user.quanxians:
                project.append(projec.projects)
        return render_template('home/test_result.html', projects=(project))
class ProjectView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  i.projects in id==False:
                    if i.projects.status ==False:
                        projects.append(i.projects)
                        id.append(i.projects)
        return  render_template('home/project.html', projects=projects)
class ModelView(View):
    methods=['GET']
    @login_required
    def dispatch_request(self):
        models=Model.query.filter_by(status=False).order_by('-id').all()
        return  render_template('home/model.html', projects=models)
class TesteventVies(MethodView):#测试环境首页
    @login_required
    def get(self):
        if current_user.is_sper==True:
            events=[]
            events.append(Interfacehuan.query.filter_by(status=False).order_by('-id').all())
        else:
            events=[]
            id=[]
            for project in current_user.quanxians:
                if (project.projects.id in id)==False:
                    events.append(Interfacehuan.query.filter_by(project=project.projects.id,status=False).order_by('-id').all())
                    id.append(project.projects.id)
        return render_template('home/events.html', events=events)
class MockViews(MethodView):#mock服务首页
    @login_required
    def get(self,page=1):
        mock=Mockserver.query.filter_by(delete=False).order_by('-id').paginate(page, per_page=int(PageShow),error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)
class TimingtasksView(MethodView):#定时任务
    @login_required
    def get(self):
        if current_user.is_sper==True:
            task=[]
            task.append(Task.query.filter_by(status=False).order_by('-id').all())
        else:
            task=[]
            id=[]
            for project in current_user.quanxians:
                if (project.projects.id in id)==False:
                    task.append(Task.query.filter_by(prject=project.projects.id,status=False).all())
                    id.append(project.projects.id)
        return render_template('home/timingtask.html', inte=task)
class GettProtestreport(MethodView):
    def get(self):
        pass
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not  project:
            return jsonify({'msg': '没有发送数据', 'code': 108})
        project_is=Project.query.filter_by(project_name=project).first()
        testreport=TestResult.query.filter_by(projects_id=project_is.id, status=False).all()
        testreportlist=[]
        for test in testreport:
            testreportlist.append({'test_num':test.test_num,'pass_num':test.pass_num,'fail_num':test.fail_num,'hour_time':str(test.hour_time),'test_rep':test.test_rep,'test_log':test.test_log,
                                   'Exception_num':test.Exception_num,'can_num':test.can_num,'wei_num':test.wei_num,'test_time':str(test.test_time),'Test_user_id':test.users.username,'id':test.id,'fenshu':test.pass_num/test.test_num})
        return jsonify(({'msg': '成功', 'code': 200,'data':(testreportlist)}))