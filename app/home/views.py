# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import  Blueprint
from  flask import  redirect,request,render_template,url_for,flash,session
home = Blueprint('home', __name__)
from app.models import *
from app.form import  *
from flask.views import MethodView,View
from flask_login import login_required,login_user,logout_user,current_user
from app import loginManager
from config import PageShow
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
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
                if user.status==0:
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
    def get(self):
        if current_user.is_sper==True:
            resylt=Interface.query.filter_by(status=False).order_by('-id').all()
        else:
            resylt=[]
            for pros in current_user.quanxians:
                pagination=Interface.query.filter_by(projects_id=pros.projects.id,status=False).all()
                resylt.append(pagination)
        return  render_template('home/interface.html', inte=resylt)
class YongliView(MethodView):#用例
    @login_required
    def get(self):
        project = Project.query.all()
        models = Model.query.all()
        if current_user.is_sper==True:
            resylt=InterfaceTest.query.filter_by(status=False).order_by('-id').all()
        else:
            resylt = []
            for projec in current_user.quanxians:
                resylt.append(InterfaceTest.query.filter_by(projects_id=projec.projects.id,status=False).all())
        return  render_template('home/interface_yongli.html', yonglis=resylt, projects=project, models=models)
class AdminuserView(MethodView):
    @login_required
    def get(self):
        if current_user.is_sper == True:
            pagination=User.query.filter_by(status=False).order_by('-id').all()
        else:
            pagination=[]
            for projec in current_user.quanxians:
                pagination.append(User.query.filter_by(projects_id=projec.projects.id, status=False).all())
        return render_template('home/useradmin.html', users=pagination)
class TestrepView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper == True:
            pagination = TestResult.query.filter_by(status=False).all()
        else:
            pagination=[]
            for projec in current_user.quanxians:
                pagination.append(TestResult.query.filter_by(projects_id=projec.projects.id, status=False).all())
        return render_template('home/test_result.html', inte=pagination)
class ProjectView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=current_user.quanxians
        return  render_template('home/project.html', projects=projects)
class ModelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper==True:
            models=Model.query.filter_by(status=False).order_by('-id').all()
        else:
            models=[]
            for project in current_user.quanxians:
                models.append(Model.query.filter_by(projects_id=project.projects.id,status=False).all())
        return  render_template('home/model.html', projects=models)
class TesteventVies(MethodView):#测试环境首页
    @login_required
    def get(self):
        if current_user.is_sper==True:
            events = Interfacehuan.query.filter_by(status=False).order_by('-id').all()
        else:
            events=[]
            for project in current_user.quanxians:
                events.append(Interfacehuan.query.filter_by(projects_id=project.projects.id,status=False).order_by('-id').all())
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
            task = Task.query.filter_by(status=False).order_by('-id').all()
        else:
            task=[]
            for project in current_user.quanxians:
                task.append(Task.query.filter_by(projects_id=project.projects.id,status=False).all())
        return render_template('home/timingtask.html', inte=task)