# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import  Blueprint,jsonify
from common.hebinglist import hebinglist
from  flask import  redirect,request,render_template,url_for,session
home = Blueprint('home', __name__)
from app.models import *
from app.form import  *
from flask.views import MethodView,View
from flask_login import login_required,login_user,logout_user,current_user
from app import loginManager
from config import PageShow
from common.pagin_fen import  fenye_list
from common.fenye import Pagination
def get_pro_mo():
    projects=Project.query.filter_by(status=False).all()
    model=Model.query.filter_by(status=False).all()
    return  projects,model
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Indexview(MethodView):
    @login_required
    def get(self):
        interface_cont=Interface.query.filter_by(status=False).all()
        interface_list=[]
        for interface in range(len(interface_cont)+1):
            try:
                if interface_cont[interface].projects.status==False :
                    interface_list.append(interface_cont[interface])
                else:
                    interface+=1
            except:
                interface += 1
        interfaceTest_cunt=InterfaceTest.query.filter_by(status=False).all()
        case_list=[]
        for case in range(len(interfaceTest_cunt)):
            try:
                if interfaceTest_cunt[case].projects.status==False :
                    case_list.append(interfaceTest_cunt[case])
                else:
                    case+=1
            except:
                case += 1
        resu_cout=TestResult.query.filter_by(status=False).all()
        reslut_list=[]
        for result in range(len(resu_cout)):
            try:
                if resu_cout[result].projects.status == False :
                    reslut_list.append(resu_cout[result])
                else:
                    result += 1
            except:
                result += 1
        project_cout=Project.query.filter_by(status=False).count()
        model_cout=Model.query.filter_by(status=False).count()
        return  render_template('home/index.html', yongli=len(case_list), jiekou=len(interface_list),
                                report=len(reslut_list), project_cout=project_cout, model_cout=model_cout)
class LoginView(MethodView):
    def get(self):
        form=LoginFrom()
        return render_template('home/login.html', form=form)
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        if username is None:
            return  jsonify({'msg':u'用户名没有输入','code':33,'data':''})
        if password is None:
            return jsonify({'msg':u'密码没有输入','code':34,'data':''})
        user=User.query.filter_by(username=username).first()
        if user:
            if user.status is False:
                return jsonify({'msg': u'用户冻结！', 'code': 35, 'data': ''})
            if user.check_password(password):
                login_user(user)
                session['username'] = username
                return jsonify({'msg': u'登录成功！', 'code': 200, 'data': ''})
            return jsonify({'msg': u'密码错误', 'code': 36, 'data': ''})
        return jsonify({'msg': u'用户不存在', 'code': 37, 'data': ''})
class LogtView(MethodView):
    @login_required
    def get(self):
        session.clear()
        logout_user()
        return redirect(url_for('home.login'))
class InterfaceView(MethodView):
    @login_required
    def get(self):
        if current_user.is_sper==True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for pros in current_user.quanxians:
                projects.append(pros.projects)
        return  render_template('home/interface.html', projects=projects)
class YongliView(MethodView):
    @login_required
    def get(self,page=1):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).all()
        else:
            projects=[]
            for i in current_user.quanxians:
                projects.append(i.projects)
        return  render_template('home/interface_yongli.html',projects=projects)
class AdminuserView(MethodView):
    @login_required
    def get(self):
        if current_user.is_sper == True:
            pagination=(User.query.filter_by(status=False).order_by('-id').all())
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
    def dispatch_request(self,page=1):
        if current_user.is_sper == True:
            project=Project.query.filter_by(status=False).all()
        else:
            project=[]
            for projec in current_user.quanxians:
                project.append(projec.projects)
        projects_lsit = fenye_list(Ob_list=project, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/test_result.html', projects=pyth_post1,pages=pages)
        except:
            return redirect(url_for('home.test_rep'))
class ProjectView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,page=1):
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
        projects_lsit=fenye_list(Ob_list=projects,split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return  render_template('home/project.html', projects=pyth_post1,pages=pages)
        except:
            return redirect(url_for('home.project'))
class ModelView(View):
    methods=['GET']
    @login_required
    def dispatch_request(self,page=1):
        models=Model.query.filter_by(status=False).order_by('-id').all()
        projects_lsit = fenye_list(Ob_list=models, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return  render_template('home/model.html', projects=pyth_post1,pages=pages)
        except:
            return redirect(url_for('home.model'))
class TesteventVies(MethodView):
    @login_required
    def get(self,page=1):
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
        projects_lsit = fenye_list(Ob_list=events, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/events.html', events=pyth_post1,pages=pages)
        except:
            return redirect(url_for('home.ceshihuanjing'))
class MockViews(MethodView):
    @login_required
    def get(self,page=1):
        mock=Mockserver.query.filter_by(delete=False).order_by('-id').paginate(page, per_page=int(PageShow),error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)
class TimingtasksView(MethodView):
    @login_required
    def get(self,page=1):
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

        old_yask=hebinglist(task)
        projects_lsit = fenye_list(Ob_list=old_yask, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/timingtask.html', inte=pyth_post1,pages=pages)
        except:
            return  redirect(url_for('home.timingtask'))
class GettProtestreport(MethodView):
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not  project:
            return jsonify({'msg': u'没有发送数据', 'code': 38,'data':''})
        project_is=Project.query.filter_by(project_name=project).first()
        testreport=TestResult.query.filter_by(projects_id=project_is.id, status=False).order_by('-id').all()
        testreportlist=[]
        for test in testreport:
            testreportlist.append({'test_num':test.test_num,'pass_num':test.pass_num,'fail_num':test.fail_num,'hour_time':str(test.hour_time),'test_rep':test.test_rep,'test_log':test.test_log,
                                   'Exception_num':test.Exception_num,'can_num':test.can_num,'wei_num':test.wei_num,'test_time':str(test.test_time),'Test_user_id':test.users.username,'id':test.id,'fenshu':test.pass_num/test.test_num})
        return jsonify(({'msg': u'成功', 'code': 200,'data':(testreportlist)}))