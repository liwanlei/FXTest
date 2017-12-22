# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import  Blueprint
from  flask import  redirect,request,render_template,url_for,flash,session
home = Blueprint('home', __name__)
from app import  db
from app.models import *
from app.form import  *
from flask.views import MethodView,View
from flask_login import current_user,login_required,login_user,logout_user
from app.common.decorators import admin_required,permission_required
from app import loginManager
from app.common.dict_com import comp_dict,dict_par
import  json
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
        if request.method=='POST' and form.validate_on_submit():
            username=request.form.get('username')
            password=request.form.get('password')
            user=User.query.filter_by(username=username).first()
            if user:
                if user.status==False:
                    if user.check_password(password=password)==True:
                        if user.status==0:
                            login_user(user)
                            session['username']=username
                            return  redirect(url_for('home.index'))
                        flash(u'用户冻结，请联系管理员')
                        return render_template('home/login.html', form=form)
                    flash(u'用户名密码错误')
                    return render_template('home/login.html', form=form)
                flash(u'用户已经冻结，请联系管理员！')
                return render_template('home/login.html', form=form)
            flash(u'用户名不存在')
            return  render_template('home/login.html', form=form)
        return  render_template('home/login.html', form=form)
class LogtView(MethodView):#退出
    def get(self):
        session.clear()
        logout_user()
        return redirect(url_for('login'))
class InterfaceView(MethodView):#接口
    @login_required
    def get(self,page=1):
        pagination=Interface.query.filter_by(status=False).order_by('-id').paginate(page, per_page=20,error_out=False)
        inter=pagination.items
        return  render_template('home/interface.html', inte=inter, pagination=pagination)
class YongliView(MethodView):#用例
    @login_required
    def get(self,page=1):
        project=Project.query.all()
        models=Model.query.all()
        if not session.get('username'):
            return redirect(url_for('home.login'))
        pagination=InterfaceTest.query.filter_by(status=False).order_by('-id').paginate(page, per_page=30,error_out=False)
        yongli=pagination.items
        return  render_template('home/interface_yongli.html', yonglis=yongli, pagination=pagination, projects=project, models=models)
class AdminuserView(MethodView):
    @admin_required
    @login_required
    def get(self,page=1):
        if not session.get('username'):
            return redirect(url_for('login'))
        user=User.query.filter_by(username=session.get('username')).first()
        pagination=User.query.filter_by(status=False).paginate(page, per_page=20,error_out=False)
        users=pagination.items
        return render_template('home/useradmin.html', users=users, pagination=pagination)
class TestrepView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,page=1):
        if not session.get('username'):
            return redirect(url_for('home.login'))
        pagination=TestResult.query.order_by('-id').paginate(page, per_page=20,error_out=False)
        inter=pagination.items
        return render_template('home/test_result.html', inte=inter, pagination=pagination)
class ProjectView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('home.login'))
        projects=Project.query.filter_by(status=False).order_by('-id').all()
        return  render_template('home/project.html', projects=projects)
class ModelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        models=Model.query.filter_by(status=False).order_by('-id').all()
        return  render_template('home/model.html', projects=models)
class TesteventVies(MethodView):#测试环境首页
    @login_required
    def get(self):
        events=Interfacehuan.query.filter_by(status=False).order_by('-id').all()
        return render_template('home/events.html', events=events)
class MockViews(MethodView):#mock服务首页
    @login_required
    def get(self,page=1):
        mock=Mockserver.query.filter_by(delete=False).order_by('-id').paginate(page, per_page=20,error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)
class TimingtasksView(MethodView):#定时任务
    @login_required
    def get(self,page=1):
        task = Task.query.filter_by(status=False).order_by('-id').paginate(page, per_page=20, error_out=False)
        inter = task.items
        return render_template('home/timingtask.html', inte=inter, pagination=task)