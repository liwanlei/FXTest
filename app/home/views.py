# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 9:23
from flask import  Blueprint,jsonify
import  json,datetime
from common.hebinglist import hebinglist
from  flask import  redirect,request,render_template,url_for,session
home = Blueprint('home', __name__)
from app.models import *
from app.form import  *
from flask.views import MethodView
from flask_login import login_required,login_user,logout_user,current_user
from app import loginManager,sched
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
        My_task=[]
        time_format = "%Y-%m-%d %H:%M:%S"
        for job in sched.get_jobs():
            job_task=Task.query.filter_by(id=job.id).first()
            if job_task.makeuser==current_user.id:
                My_task.append({'taskname':job_task.taskname,'next_run':job.next_run_time.strftime( '%Y-%m-%d %H:%M:%S ')})
        project_cout=Project.query.filter_by(status=False).count()
        model_cout=Model.query.filter_by(status=False).count()
        return  render_template('home/index.html', yongli=len(case_list),
                                jiekou=len(interface_list),
                                report=len(reslut_list), project_cout=project_cout,
                                model_cout=model_cout,my_tasl=My_task)
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
        models = Model.query.filter_by(status=False).all()
        if current_user.is_sper==True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for pros in current_user.quanxians:
                projects.append(pros.projects)
        return  render_template('home/interface.html', projects=projects,models=models)
    @login_required
    def post(self):
        data=request.get_json()
        project=data['project']
        model=data['model']
        name=data['name']
        url=data['url']
        headers=data['headers']
        xieyi=data['xieyi']
        meth=data['meth']
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
            return jsonify({'data': u'添加成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': u'添加接口失败，原因:%s' % e, 'code': 3})
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        interface = Interface.query.filter_by(id=data, status=False).first()
        if not interface:
            return jsonify({"data": '删除接口不存在', 'code': 4})
        interface.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除接口失败，原因：%s'%e, 'code':3})
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
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        testcase = InterfaceTest.query.filter_by(id=data).first()
        if not testcase:
            return jsonify({"data": '删除用例不存在', 'code': 4})
        try:
            testcase.status = True
            db.session.commit()
            return jsonify({"data": '删除用例成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除用例失败，原因：%s'%e, 'code':3})
class AdminuserView(MethodView):
    @login_required
    def get(self):
        wrok = Work.query.all()
        projects = Project.query.filter_by(status=False).all()
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
        return render_template('home/useradmin.html', users=index_list,html=html, wroks=wrok, projects=projects)
    @login_required
    def post(self):
        data=request.get_json()
        name=data['name']
        password=data['password']
        work=data['work']
        project=data['project']
        email=data['email']
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
        if len(project)<=0:
            return jsonify({'data': '成功', 'code': 2})
        else:
            try:
                user_id = User.query.filter_by(username=name).first()
                for proj in project:
                    project_one=Project.query.filter_by(project_name=proj).first()
                    quanxian = Quanxian(project=project_one.id, rose=1)
                    quanxian.user.append(user_id)
                    db.session.add(quanxian)
                db.session.commit()
                return jsonify({'data': '成功', 'code': 2})
            except Exception as e:
                db.session.rollback()
                return jsonify({'data': '添加失败，原因：%s' % e, 'code':1})
class TestrepView(MethodView):
    @login_required
    def get(self,page=1):
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
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        delTest=TestResult.query.filter_by(id=data,status=False).first()
        if not  delTest:
            return jsonify({"data": '删除的测试报告不存在', 'code':3})
        delTest.status=True
        try:
            db.session.commit()
            return jsonify({"data": '删除测试报告成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除测试报告失败！', 'code': 2})
class ProjectView(MethodView):
    @login_required
    def get(self,page=1):
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
    @login_required
    def post(self):
        name=request.data.decode('utf-8')
        if current_user.is_sper == False:
            return jsonify({'code': 3, 'data': '权限不足！' })
        if name =='':
            return jsonify({'code': 4, 'data': '不能为空！'})
        projec=Project.query.filter_by(project_name=name,status=False).first()
        if projec:
            return jsonify({'code': 5, 'data': '项目不能重复！'})
        new_moel=Project(project_name=name,project_user_id=current_user.id)
        db.session.add(new_moel)
        try:
            db.session.commit()
            return jsonify({'code': 2, 'data': '添加成功！', '': ''})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 7, 'data': '添加失败，原因:%s！'%e,})
    @login_required
    def put(self):
        data=request.data.decode('utf-8')
        json_data=json.loads(data)
        id=json_data['id']
        name=json_data['name']
        prohect = Project.query.filter_by(id=id).first()
        if not prohect:
            new=Project(project_name=name,project_user_id=current_user.id)
            db.session.add(new)
            db.session.commit()
            return jsonify({"data": '添加项目成功', 'code':2})
        prohect.project_name = name
        try:
            db.session.commit()
            return jsonify({'code': 2, 'data': '编辑项目成功！'})
        except Exception as e:
            db.session.rollback()
            return jsonify({"code":3, 'data': '编辑出现问题！原因：%s' % e})
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        proje = Project.query.filter_by(id=data, status=False).first()
        if not proje:
            return jsonify({"data": '删除项目不存在', 'code': 4})
        proje.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除失败', 'code':3})
class ModelView(MethodView):
    @login_required
    def get(self,page=1):
        models=Model.query.filter_by(status=False).order_by('-id').all()
        projects_lsit = fenye_list(Ob_list=models, split=PageShow)
        pages = range(1, len(projects_lsit) + 1)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return  render_template('home/model.html', projects=pyth_post1,pages=pages)
        except:
            return redirect(url_for('home.model'))
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        model = Model.query.filter_by(id=data, status=False).first()
        if not model:
            return jsonify({"data": '模块不存在', 'code':3})
        model.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": '删除失败', 'code':4})
    @login_required
    def post(self):
        data = request.data.decode('utf-8')
        models = Model.query.filter_by(model_name=data).first()
        if models:
            return jsonify({'code': 1, 'data': u'模块不能重复存在'})
        new_moel = Model(model_name=data, model_user_id=current_user.id)
        db.session.add(new_moel)
        try:
            db.session.commit()
            return jsonify({'code':2, 'data': u'添加成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 3, 'data': u'添加失败，原因：%s' % e})
    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        edit_mode = Model.query.filter_by(id=id).first()
        if not edit_mode:
            mew=Model(model_name=name,model_user_id=current_user.id)
            db.session.add(mew)
            db.session.commit()
            return jsonify({'data': '编辑成功', 'code': 2})
        edit_mode.model_name = name
        try:
            db.session.commit()
            return jsonify({'data': '编辑模块成功', 'code': 2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': '编辑模块出现问题！原因：%s' % e, 'code': 308})
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
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            for i in current_user.quanxians:
                if  (i.projects in i)==False:
                    projects.append(i.projects)
        try:
            pyth_post1 = projects_lsit[int(page) - 1]
            return render_template('home/events.html', events=pyth_post1,pages=pages,projects=projects)
        except:
            return redirect(url_for('home.ceshihuanjing'))
    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        event = Interfacehuan.query.filter_by(id=data).first()
        event.status = True
        try:
            db.session.commit()
            return jsonify({"data": '删除成功', 'code':2})
        except Exception as e:
            return jsonify({"data": '删除失败', 'code': 4})
    @login_required
    def post(self):
        data = request.get_json()
        json_data=data
        project=json_data['project']
        url=json_data['url']
        desc=json_data['desc']
        name=json_data['name']
        host=json_data['host']
        port=json_data['port']
        usernmae=json_data['username']
        password=json_data['password']
        url_old = Interfacehuan.query.filter_by(url=str(url)).first()
        if url_old:
            return jsonify({"msg": u'测试环境必须是相互独立的', "code": 209, 'data': ''})
        prkcyt = Project.query.filter_by(project_name=project).first()
        end = Interfacehuan(url = url,desc = desc,project = prkcyt.id,database = name,
                                databaseuser=usernmae,databasepassword = password,dbhost = host,
                                dbport=port,make_user = current_user.id)
        db.session.add(end)
        try:
            db.session.commit()
            return jsonify({"data": u'添加测试环境成功!', "code":2})
        except Exception as e:
            db.session.rollback()
            return jsonify({"data": u'添加测试用例失败！原因：%s' % e, "code": 211})
    @login_required
    def put(self):
        data = request.get_json()
        json_data = data
        project = json_data['project']
        id=json_data['id']
        url = json_data['url']
        desc = json_data['desc']
        name = json_data['name']
        host = json_data['host']
        port = json_data['port']
        usernmae = json_data['username']
        password = json_data['password']
        project = Project.query.filter_by(project_name=project).first()
        event = Interfacehuan.query.filter_by(id=id).first()
        if not  event:
            end = Interfacehuan(url = url,desc = desc,project = project.id,database = name,
                                databaseuser=usernmae,databasepassword = password,dbhost = host,
                                dbport=port,make_user = current_user.id)
            db.session.add(end)
            db.session.commit()
            return jsonify({'data': '编辑成功', 'code': 2})
        event.url = url
        event.desc = desc
        event.database = name
        event.databaseuser =usernmae
        event.datebasepassword = password
        event.dbhost =host
        event.dbport = port
        event.project = project.id
        event.make_user = current_user.id
        try:
            db.session.commit()
            return jsonify({'data': '编辑成功', 'code':2})
        except Exception as e:
            db.session.rollback()
            return jsonify({'data': '编辑失败！原因是:%s' % e, 'code': 321})
class MockViews(MethodView):
    @login_required
    def get(self,page=1):
        mock=Mockserver.query.filter_by(delete=False).order_by('-id').paginate(page,
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
        return jsonify({'data': '删除失败，找不到mocksever', 'code':3})
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
        if not  project_is:
            return jsonify(({'msg': u'成功', 'code': 200, 'data':[]}))
        testreport=TestResult.query.filter_by(projects_id=project_is.id, status=False).order_by('-id').all()
        testreportlist=[]
        for test in testreport:
            testreportlist.append({'test_num':test.test_num,'pass_num':test.pass_num,
                                   'fail_num':test.fail_num,'hour_time':str(test.hour_time),
                                   'test_rep':test.test_rep,'test_log':test.test_log,
                                   'Exception_num':test.Exception_num,'can_num':test.can_num,
                                   'wei_num':test.wei_num,'test_time':str(test.test_time),
                                   'Test_user_id':test.users.username,'id':test.id,
                                   'fenshu':test.pass_num/test.test_num})
        return jsonify(({'msg': u'成功', 'code': 200,'data':(testreportlist)}))