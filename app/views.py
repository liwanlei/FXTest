# encoding: utf-8
"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app,db
from  flask import  make_response,redirect,request,render_template,session,url_for,flash,send_file,abort,make_response,send_from_directory,jsonify,Response
from werkzeug import secure_filename
from  app.models import *
from app.form import  *
import os,time,datetime
from app.common.pares_excel_inter import pasre_inter
from app.common.py_Html import createHtml
from app.common.requ_case import Api
from app.common.panduan import assert_in
from app.test_case.Test_case import ApiTestCase
from app.common.send_email import send_emails 
from flask.views import MethodView,View
from flask_login import current_user,login_required,login_user,logout_user
from app.common.decorators import admin_required,permission_required
from app import loginManager
from app.common.dict_com import comp_dict,dict_par
import  json
from app import  scheduler
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
class InterfaceaddView(MethodView):
    @login_required
    def get(self):
        form=InterForm()
        project,models=get_pro_mo()
        return render_template('add/add_interface.html', form=form, projects=project, models=models)
    @login_required
    def post(self):
        form=InterForm()
        project,models=get_pro_mo()
        if form.validate_on_submit and request.method =="POST":
            project_name=request.form.get('project')
            model_name=request.form.get('model')
            interface_name=request.form.get('interface_name')
            interface_url=request.form.get('interface_url')
            interface_header=request.form.get('interface_headers')
            interface_meth=request.form.get('interface_meth')
            interface_par=request.form.get('interface_par')
            interface_bas=request.form.get('interface_bas')
            if project_name == None or model_name ==None or interface_header=='' or interface_name=='' or interface_url =='' or interface_meth=='':
                flash(u'请完整填写接口的各项信息')
                return render_template('add/add_interface.html', form=form, projects=project, models=models)
            user_id=User.query.filter_by(username=session.get('username')).first().id
            project_id=Project.query.filter_by(project_name=project_name).first().id
            models_id=Model.query.filter_by(model_name=model_name).first().id
            try:
                new_interface=Interface(model_id=models_id,projects_id=project_id,Interface_name=interface_name,Interface_url=interface_url,Interface_meth=interface_meth,Interface_par=interface_par,Interface_back=interface_bas,Interface_user_id=user_id,Interface_headers=interface_header)
                db.session.add(new_interface)
                db.session.commit()
                flash(u'添加成功')
                return redirect(url_for('home.interface'))
            except:
                db.session.rollback()
                flash(u'添加失败')
                return render_template('add/add_interface.html', form=form, projects=project, models=models)
        return render_template('add/add_interface.html', form=form, projects=project, models=models)
class EditInterfaceView(MethodView):
    @login_required
    def get(self,id):
        interface=Interface.query.filter_by(id=id).first()
        project, models = get_pro_mo()
        return render_template('edit/edit_inter.html', interface=interface, projects=project, models=models)
    @login_required
    def post(self,id):
        interface=Interface.query.filter_by(id=id).first()
        project, models = get_pro_mo()
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            intername=request.form.get('inter_name')
            url=request.form.get('url')
            headers=request.form.get('headers')
            meth=request.form.get('meth')
            reques=request.form.get('reque')
            back=request.form.get('back')
            if projecct ==None or model==None or intername=='' or headers =='' or url=='' or meth=='' or back=='':
                flash(u'请确定各项参数都正常填写')
                return render_template('edit/edit_inter.html', interface=interface, projects=project, models=models)
            project_id = Project.query.filter_by(project_name=projecct).first().id
            models_id = Model.query.filter_by(model_name=model).first().id
            interface.projects_id=project_id
            interface.model_id=models_id
            interface.Interface_name=intername
            interface.Interface_headers=headers
            interface.Interface_url=url
            interface.Interface_meth=meth
            interface.Interface_par=reques
            interface.Interface_back=back
            interface.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
            db.session.commit()
            return redirect(url_for('home.interface'))
        return render_template('edit/edit_inter.html', interface=interface, projects=project, models=models)
class DeleinterView(MethodView):
    @login_required
    def get(self,id):
        interface=Interface.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if user.id==interface.Interface_user_id or user.role_id==2:
            interface.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.interface'))
        flash(u'您没有权限删除这条接口')
        return redirect(url_for('home.interface'))
class AddtestcaseView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        form=Interface_yong_Form()
        project, models = get_pro_mo()
        if request.method=='POST' and form.validate_on_submit :
            yongli_nam=request.form.get('project')
            mode=request.form.get('model')
            interface_name=request.form.get('interface_name')
            interface_url=request.form.get('interface_url')
            interface_header=request.form.get('interface_headers')
            interface_meth=request.form.get('interface_meth')
            interface_can=request.form.get('interface_can')
            interface_re=request.form.get('interface_rest')
            if yongli_nam ==None or mode==None or interface_name=='' or interface_header==''or interface_url=='' or interface_meth=='' or interface_re=='':
                flash(u'请准确填写用例')
                return render_template('add/add_test_case.html', form=form, projects=project, models=models)
            project_id = Project.query.filter_by(project_name=yongli_nam).first().id
            models_id = Model.query.filter_by(model_name=mode).first().id
            try:
                newcase=InterfaceTest(projects_id=project_id,model_id=models_id,Interface_name=interface_name,Interface_headers=interface_header,Interface_url=interface_url,Interface_meth=interface_meth,Interface_pase=interface_can,Interface_assert=interface_re,Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                db.session.add(newcase)
                db.session.commit()
                flash(u'添加用例成功')
                return redirect(url_for('home.yongli'))
            except:
                db.session.rollback()
                flash(u'添加用例失败')
                return render_template('add/add_test_case.html', form=form, projects=project, models=models)
        return render_template('add/add_test_case.html', form=form, projects=project, models=models)
class Deletecase(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('home.login'))
        testcase=InterfaceTest.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if testcase.Interface_user_id==user.id or user.role_id==2:
            testcase.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.yongli'))
        flash(u'您没有权限去删除这条用例')
        return redirect(url_for('home.yongli'))
class EditcaseView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('home.login'))
        project, models = get_pro_mo()
        edit_case=InterfaceTest.query.filter_by(id=id).first()
        if request.method=='POST':
            yongli_nam = request.form.get('project')
            mode = request.form.get('model')
            url=request.form.get('url')
            meth=request.form.get('meth')
            headers=request.form.get('headers')
            parme=request.form.get('parme')
            reque=request.form.get('reque')
            if yongli_nam ==None  or mode== None or url==''or headers=='' or meth==''  or reque=='':
                flash(u'请确定各项参数都正常填写')
                return render_template('edit/edit_case.html', edit=edit_case, projects=project, models=models)
            projects_id = Project.query.filter_by(project_name=yongli_nam).first().id
            model_id = Model.query.filter_by(model_name=mode).first().id
            edit_case.projects_id=projects_id
            edit_case.model_id=model_id
            edit_case.Interface_url=url
            edit_case.Interface_headers=headers
            edit_case.Interface_meth=meth
            edit_case.Interface_pase=parme
            edit_case.Interface_assert=reque
            edit_case.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
            db.session.commit()
            flash(u'编辑成功')
            return redirect(url_for('home.yongli'))
        return render_template('edit/edit_case.html', edit=edit_case, projects=project, models=models)
@app.route('/down_jiekou',methods=['GET'])
def down_jiekou():
    if not session.get('username'):
        return redirect(url_for('home.login'))
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir=os.path.join(basedir,'upload')
    response=make_response(send_from_directory(file_dir,'interface.xlsx',as_attachment=True))
    return response
@app.route('/down_case',methods=['GET'])
def down_case():
    if not session.get('username'):
        return redirect(url_for('login'))
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir=os.path.join(basedir,'upload')
    response=make_response(send_from_directory(file_dir,'interface_case.xlsx',as_attachment=True))
    return response
class DaoruinterView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not session.get('home.username'):
            return redirect(url_for('home.login'))
        if request.method == 'POST':
            file = request.files['myfile']
            if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
                filename='jiekou.xlsx'
                file.save(filename)
                jiekou_bianhao,project_nam,model_nam,interface_name,interface_url, interface_header,interface_meth, interface_par, interface_bas = pasre_inter(filename)
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first().id
                        model_id = Model.query.filter_by(model_name=model_nam[i]).first().id
                        new_interface=Interface(projects_id=projects_id,model_id=model_id,Interface_name=str(interface_name[i]),Interface_url=str(interface_url[i]),Interface_headers=str(interface_header[i]),Interface_meth=str(interface_meth[i]),Interface_par=(interface_par[i]),Interface_back=str(interface_bas[i]),Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                        db.session.add(new_interface)
                    db.session.commit()
                    flash(u'导入成功')
                    return redirect(url_for('home.interface'))
                except:
                    flash(u'导入失败，请检查格式是否正确')
                    return render_template('daoru.html')
            flash(u'导入失败')
            return render_template('daoru.html')
        return render_template('daoru.html')
class DaorucaseView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not session.get('username'):
            return redirect(url_for('login'))
        if request.method == 'POST':
            file = request.files['myfile']
            if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
                filename='jiekoucase.xlsx'
                file.save(filename)
                jiekou_bianhao,interface_name,project_nam, model_nam, interface_url,interfac_header, interface_meth, interface_par, interface_bas = pasre_inter(filename)
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first().id
                        model_id = Model.query.filter_by(model_name=model_nam[i]).first().id
                        new_interface = InterfaceTest(projects_id=projects_id, model_id=model_id,Interface_name=str(interface_name[i]), Interface_url=str(interface_url[i]),Interface_headers=interfac_header[i],Interface_meth=str(interface_meth[i]), Interface_pase=(interface_par[i]),Interface_assert=str(interface_bas[i]),Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                        db.session.add(new_interface)
                    db.session.commit()
                    flash(u'导入成功')
                    return redirect(url_for('home.yongli'))
                except:
                    db.session.rollback()
                    flash(u'导入失败，请检查格式是否正确')
                    return render_template('daoru_case.html')
            flash(u'导入失败')
            return render_template('daoru_case.html')
        return  render_template('daoru_case.html')
class SeryongliView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        project=Project.query.all()
        models=Model.query.all()
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            if projecct =='':
                interd=InterfaceTest.query.filter(InterfaceTest.model_id==int(model)).all()
                return render_template('home/ser_yonglo.html', yonglis=interd, projects=project, models=models)
            if model =='':
                interd=InterfaceTest.query.filter(InterfaceTest.projects_id==int(projecct)).all()
                return render_template('home/ser_yonglo.html', yonglis=interd, projects=project, models=models)
            interd=InterfaceTest.query.filter(InterfaceTest.projects_id==int(projecct),InterfaceTest.model_id==int(model)).order_by('-id').all()
            return render_template('home/ser_yonglo.html', yonglis=interd, projects=project, models=models)
        return redirect(url_for('home.yongli'))
class SerinterView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            if projecct =='' and model  =='':
                flash(u'请输入搜索的内容')
                return redirect(url_for('interface'))
            try:
                projects_id = Project.query.filter_by(project_name=projecct).first().id
                model_id = Model.query.filter_by(model_name=model).first().id
                interd=Interface.query.filter(Interface.model_id.like('%'+str(model_id)+'%'),Interface.projects_id.like('%'+str(projects_id)+'%')).all()
                if len(interd)<=0:
                    flash(u'搜索的内容不存在')
                    return redirect(url_for('home.interface'))
                return render_template('home/ser_inter.html', inte=interd)
            except:
                flash(u'搜索的内容不存在')
                return redirect(url_for('home.interface'))
        return redirect(url_for('home.interface'))
class LoadView(View):
    methods=['GET']
    def dispatch_request(self,filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir=os.path.join(basedir,'upload')
        response=make_response(send_from_directory(file_dir,filename,as_attachment=True))
        return response
class MakeonecaseView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        case=InterfaceTest.query.filter_by(id=id).first()
        me=Api(url=case.Interface_url,fangshi=case.Interface_meth,params=case.Interface_pase,headers=case.Interface_headers)
        result=me.testapi()
        retur_re=assert_in(case.Interface_assert,result)
        try:
            if retur_re=='pass':
                flash(u'用例测试通过')
                return redirect(url_for('home.yongli'))
            flash(u'用例测试失败')
            return redirect(url_for('home.yongli'))
        except:
            flash(u'用例测试失败,请检查您的用例')
            return redirect(url_for('home.yongli'))
class DuoyongliView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        starttime=datetime.datetime.now()
        star=time.time()
        day = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir, 'upload')
        file = os.path.join(file_dir, (day + '.log'))
        if os.path.exists(file) is False:
            os.system('touch %s' % file)
        filepath =os.path.join(file_dir,(day+'.html'))
        if os.path.exists(filepath) is False:
            os.system(r'touch %s' % filepath)
        if request.method=='POST':
            f=request.form.get('checkbox')
            me=request.form.getlist('yongli')
            if len(me)<=1:
                flash(u'请选择一个以上的用例来执行')
                return redirect(url_for('yongli'))
            projecct_list=[]
            model_list=[]
            Interface_name_list=[]
            Interface_url_list=[]
            Interface_meth_list=[]
            Interface_pase_list=[]
            Interface_assert_list=[]
            Interface_headers_list=[]
            id_list=[]
            for case in me:
                case_one=InterfaceTest.query.filter_by(id=case).first()
                id_list.append(case_one.id)
                projecct_list.append(case_one.projects)
                model_list.append(case_one.models)
                Interface_url_list.append(case_one.Interface_url)
                Interface_name_list.append(case_one.Interface_name)
                Interface_meth_list.append(case_one.Interface_meth)
                Interface_pase_list.append(case_one.Interface_pase)
                Interface_assert_list.append(case_one.Interface_assert)
                Interface_headers_list.append(case_one.Interface_headers)
            if (len(set(projecct_list)))>1:
                flash('目前单次只能执行一个项目')
                return redirect(url_for('yongli'))
            if f =='on':
                email=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True).first()
                if email:
                    try:
                        apitest=ApiTestCase(Interface_url_list,Interface_meth_list,Interface_pase_list,Interface_assert_list,file,Interface_headers_list)
                        result_toal,result_pass,result_fail,relusts,bask_list=apitest.testapi()
                        endtime=datetime.datetime.now()
                        end = time.time()
                        createHtml(titles=u'接口测试报告',filepath=filepath,starttime=starttime,endtime=endtime,passge=result_pass,fail=result_fail,id=id_list,name=projecct_list,headers=Interface_headers_list,coneent=Interface_url_list,url=Interface_meth_list,meth=Interface_pase_list,yuqi=Interface_assert_list,json=bask_list,relusts=relusts)
                        hour=end-star
                        user_id=User.query.filter_by(username=session.get('username')).first().id
                        new_reust=TestResult(Test_user_id=user_id,test_num=result_toal,pass_num=result_pass,fail_num=result_fail,test_time=starttime,hour_time=hour,test_rep=(day+'.html'),test_log=(day+'.log'))
                        db.session.add(new_reust)
                        db.session.commit()
                        m=send_emails(sender=email.send_email,receivers=email.to_email,password=email.send_email_password,smtp=email.stmp_email,port=email.port,fujian1=file,fujian2=filepath,subject=u'%s用例执行测试报告'%day,url='http://127.0.0.1:5000/test_rep')
                        if m==False:
                            flash(u'发送邮件失败，请检查您默认的邮件设置是否正确')
                            return redirect(url_for('home.test_rep'))
                        flash(u'测试已经完成，并且给您默认设置发送了测试报告')
                        return redirect(url_for('home.test_rep'))
                    except:
                        flash(u'测试失败，请检查您的测试用例单个执行是否出错')
                        return redirect(url_for('home.yongli'))
                flash(u'无法完成，需要去您的个人设置去设置一个默认的邮件发送')
                return redirect(url_for('home.yongli'))
            try:
                apitest=ApiTestCase(Interface_url_list,Interface_meth_list,Interface_pase_list,Interface_assert_list,file,Interface_headers_list)
                result_toal,result_pass,result_fail,relusts,bask_list=apitest.testapi()
                endtime=datetime.datetime.now()
                end = time.time()
                createHtml(titles=u'接口测试报告',filepath=filepath,starttime=starttime,endtime=endtime,passge=result_pass,fail=result_fail,id=id_list,name=projecct_list,headers=Interface_headers_list,coneent=Interface_url_list,url=Interface_meth_list,meth=Interface_pase_list,yuqi=Interface_assert_list,json=bask_list,relusts=relusts)
                hour=end-star
                user_id=User.query.filter_by(username=session.get('username')).first().id
                new_reust=TestResult(Test_user_id=user_id,test_num=result_toal,pass_num=result_pass,fail_num=result_fail,test_time=starttime,hour_time=hour,test_rep=(day+'.html'),test_log=(day+'.log'))
                db.session.add(new_reust)
                db.session.commit()
                flash(u'测试已经完成')
                return redirect(url_for('home.test_rep'))
            except:
                flash(u'测试失败，请检查您的测试用例单个执行是否出错')
                return redirect(url_for('home.yongli'))
        return redirect(url_for('home.yongli'))
class AddmodelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('home.login'))
        if request.method=="POST":
            model=request.form.get('project')
            if model=='':
                flash(u'请添加您的模块名')
                return render_template('add/add_moel.html')
            user_id=User.query.filter_by(username=session.get('username')).first().id
            models=Model.query.filter_by(model_name=model).first()
            if models:
                flash(u'模块不能重复')
                return render_template('add/add_moel.html')
            new_moel=Model(model_name=model,model_user_id=user_id)
            db.session.add(new_moel)
            db.session.commit()
            flash(u'添加成功!')
            return  redirect(url_for('home.model'))
        return  render_template('add/add_moel.html')
class AddproView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('home.login'))
        if request.method=="POST":
            model=request.form.get('project')
            if model=='':
                flash(u'请添加您的项目名')
                return render_template('add/add_pro.html')
            user_id=User.query.filter_by(username=session.get('username')).first().id
            projec=Project.query.filter_by(project_name=model).first()
            if projec:
                flash(u'项目不能重复')
                return render_template('add/add_pro.html')
            new_moel=Project(project_name=model,project_user_id=user_id)
            db.session.add(new_moel)
            try:
                db.session.commit()
                flash(u'添加成功!')
                return  redirect(url_for('home.project'))
            except:
                db.session.rollback()
                flash(u'添加guo程总是不理想!')
                return redirect(url_for('home.project'))
        return  render_template('add/add_pro.html')
class DelemodelView(View):
    methods=['GET','POST']
    @admin_required
    @login_required
    def dispatch_request(self,id):
        model=Model.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id==2:
            model.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.model'))
        flash(u'您没有权限删除这个模块')
        return redirect(url_for('home.model'))
class DeleproView(View):
    methods=['GET','POST']
    @admin_required
    @login_required
    def dispatch_request(self,id):
        proje=Project.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id==2:
            proje.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.project'))
        flash(u'您没有权限删除这个项目')
        return redirect(url_for('home.project'))
class EditmoelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if not session.get('username'):
            return  redirect(url_for('home.login'))
        user = User.query.filter_by(username=session.get('username')).first()
        model=Model.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('model')
            if ed_mode=='':
                flash(u'请添加模块名')
                return render_template('edit/edit_model.html', mode=model)
            models = Model.query.filter_by(model_name=ed_mode).first()
            model.model_name=ed_mode
            try:
                db.session.commit()
                flash(u'编辑成功')
                return  redirect(url_for('home.model'))
            except:
                db.session.rollback()
                flash(u'编辑zhi路漫漫兮')
                return redirect(url_for('home.model'))
        return  render_template('edit/edit_model.html', mode=model)
class EditproView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if not session.get('username'):
            return  redirect(url_for('home.login'))
        user = User.query.filter_by(username=session.get('username')).first()
        project=Project.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('project')
            if ed_mode=='':
                flash(u'请添加项目')
                return render_template('edit/edit_pro.html', project=project)
            models = Project.query.filter_by(project_name=ed_mode).first()
            project.project_name=ed_mode
            try:
                db.session.commit()
                flash(u'编辑成功')
                return  redirect(url_for('home.project'))
            except:
                db.session.rollback()
                flash(u'编辑出现小异常')
                return redirect(url_for('home.project'))
        return  render_template('edit/edit_pro.html', project=project)
class DeleteResultView(View):
    methods=['GET','POST']
    @admin_required
    @login_required
    def dispatch_request(self,id):
        delTest=TestResult.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id==2:
            delTest.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.test_rep'))
        flash(u'您没有权限去删除测试报告')
        return redirect(url_for('home.test_rep'))
class ADDTesteventView(MethodView):#添加测试环境
    @login_required
    def get(self):
        peoject,modesl=get_pro_mo()
        forms=Interface_Env()
        return render_template('add/add_even.html', form=forms, projects=peoject)
    @login_required
    def post(self):
        peoject, modesl = get_pro_mo()
        forms = Interface_Env()
        if forms.validate_on_submit:
            peoject=request.form['project']
            url=request.form['envtion']
            desc=request.form['desc']
            user_id = current_user.id
            if peoject =='' or url=='' or desc =='':
                flash(u'请准确填写测试环境的信息')
                return redirect(url_for('addevent'))
            url_old=Interfacehuan.query.filter_by(url=url).first()
            if url_old:
                flash(u'测试环境必须是相互独立的')
                return redirect(url_for('addevent'))
            end=Interfacehuan()
            end.url=url
            end.desc=desc
            end.project=peoject
            end.make_user=user_id
            db.session.add(end)
            try:
                db.session.commit()
                return redirect(url_for('home.yongli'))
            except:
                db.session.rollback()
            return redirect(url_for('home.yongli'))
        return render_template('add/add_even.html', form=forms, projects=peoject)
class DeleteEventViews(MethodView):#删除测试环境
    @login_required
    def get(self,id):
        event=Interfacehuan.query.filter_by(id=id).first()
        user_id = current_user.id
        if event.make_user==user_id or current_user.role_id==2:
            event.status=True
            db.session.commit()
            flash(u'删除成功')
            return  redirect(url_for('home.ceshihuanjing'))
        flash(u'权利不足以删除！')
        return  redirect(url_for('home.ceshihuanjing'))
class EditEventViews(MethodView):#编辑测试环境
    @login_required
    def get(self,id):
        project,models=get_pro_mo()
        event=Interfacehuan.query.filter_by(id=id).first()
        return  render_template('edit/edit_events.html', enents=event, projects=project)
    def post(self,id):
        project, models = get_pro_mo()
        event = Interfacehuan.query.filter_by(id=id).first()
        projectd=request.form['project']
        url=request.form['url']
        desc=request.form['desc']
        ueris=current_user.id
        event.url=url
        event.desc=desc
        event.project=projectd
        event.make_user=ueris
        try:
            db.session.commit()
            return  redirect(url_for('home.ceshihuanjing'))
        except:
            db.session.rollback()
            flash(u'编辑出现问题，重新编辑')
            return render_template('edit/edit_events.html', enents=event, projects=project)
        return render_template('edit/edit_events.html', enents=event, projects=project)
@app.route('/gettest',methods=['POST'])
@login_required
def gettest():#ajax获取项目的测试用例
    projec=(request.get_data('project')).decode('utf-8')
    if not projec:
        return []
    proje=Project.query.filter_by(project_name=str(projec)).first()
    if not proje:
        return  []
    testyong=InterfaceTest.query.filter_by(projects_id=proje.id).all()
    testyong_list=[]
    for i in testyong:
        testyong_list.append({'name':i.Interface_name,'id':i.id})
    return   jsonify({'data':testyong_list})
