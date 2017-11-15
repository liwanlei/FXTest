# encoding: utf-8
"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app,db
from  flask import  redirect,request,render_template,session,url_for,flash,send_file,abort,make_response,send_from_directory,jsonify
from werkzeug import secure_filename
from  app.models import *
from app.form import  *
import os,time,datetime,threading
from app.common.pares_excel_inter import pasre_inter
from app.common.py_Html import createHtml
from app.common.requ_case import Api
from app.common.dict_com import assert_in
from app.test_case.Test_case import ApiTestCase
from app.common.py_Html import createHtml
from app.common.send_email import send_emails 
from flask.views import MethodView,View
from flask_login import current_user,login_required,login_user,logout_user
from app.common.decorators import admin_required,permission_required
from app import loginManager
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
class Indexview(MethodView):
    @login_required
    def get(self):
        interface_cont=Interface.query.count()
        interfaceTest_cunt=InterfaceTest.query.count()
        resu_cout=TestResult.query.count()
        project_cout=Project.query.count()
        model_cout=Model.query.count()
        return  render_template('index.html',yongli=interfaceTest_cunt,jiekou=interface_cont,report=resu_cout,project_cout=project_cout,model_cout=model_cout)
class LoginView(MethodView):
    def get(self):
        form=LoginFrom()
        return render_template('login.html', form=form)
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
                            return  redirect(url_for('index'))
                        flash(u'用户冻结，请联系管理员')
                        return render_template('login.html', form=form)
                    flash(u'用户名密码错误')
                    return render_template('login.html', form=form)
                flash(u'用户已经冻结，请联系管理员！')
                return render_template('login.html', form=form)
            flash(u'用户名不存在')
            return  render_template('login.html',form=form)
        return  render_template('login.html',form=form)
class LogtView(MethodView):
    def get(self):
        session.clear()
        logout_user()
        return redirect(url_for('login'))
class InterfaceView(MethodView):
    @login_required
    def get(self,page=1):
        pagination=Interface.query.filter_by(status=False).paginate(page, per_page=20,error_out=False)
        inter=pagination.items
        return  render_template('interface.html',inte=inter,pagination=pagination)
class YongliView(MethodView):
    def get(self,page=1):
        project=Project.query.all()
        models=Model.query.all()
        if not session.get('username'):
            return redirect(url_for('login'))
        pagination=InterfaceTest.query.filter_by(status=False).paginate(page, per_page=30,error_out=False)
        yongli=pagination.items
        return  render_template('interface_yongli.html',yonglis=yongli,pagination=pagination,projects=project,models=models)
class AdminuserView(MethodView):
    @admin_required
    @login_required
    def get(self,page=1):
        if not session.get('username'):
            return redirect(url_for('login'))
        user=User.query.filter_by(username=session.get('username')).first()
        pagination=User.query.filter_by(status=False).paginate(page, per_page=20,error_out=False)
        users=pagination.items
        return render_template('useradmin.html',users=users,pagination=pagination)
class InterfaceaddView(MethodView):
    def get(self):
        if not session.get('username'):
            return redirect(url_for('login'))
        form=InterForm()
        project,models=get_pro_mo()
        return render_template('add_interface.html',form=form,projects=project,models=models)
    def post(self):
        if not session.get('username'):
            return redirect(url_for('login'))
        form=InterForm()
        project,models=get_pro_mo()
        if form.validate_on_submit and request.method =="POST":
            project_name=request.form.get('project')
            model_name=request.form.get('model')
            interface_name=request.form.get('interface_name')
            interface_url=request.form.get('interface_url')
            interface_meth=request.form.get('interface_meth')
            interface_par=request.form.get('interface_par')
            interface_bas=request.form.get('interface_bas')
            if project_name == None or model_name ==None or interface_name=='' or interface_url =='' or interface_meth=='':
                flash(u'请完整填写接口的各项信息')
                return render_template('add_interface.html',form=form,projects=project,models=models)
            user_id=User.query.filter_by(username=session.get('username')).first().id
            project_id=Project.query.filter_by(project_name=project_name).first().id
            models_id=Model.query.filter_by(model_name=model_name).first().id
            try:
                new_interface=Interface(model_id=models_id,projects_id=project_id,Interface_name=interface_name,Interface_url=interface_url,Interface_meth=interface_meth,Interface_par=interface_par,Interface_back=interface_bas,Interface_user_id=user_id)
                db.session.add(new_interface)
                db.session.commit()
                flash(u'添加成功')
                return redirect(url_for('interface'))
            except:
                flash(u'添加失败')
                return render_template('add_interface.html',form=form,projects=project,models=models)
        return render_template('add_interface.html',form=form,projects=project,models=models)
class EditInterfaceView(MethodView):
    def get(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        interface=Interface.query.filter_by(id=id).first()
        project, models = get_pro_mo()
        return render_template('edit_inter.html',interface=interface,projects=project,models=models)
    def post(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        interface=Interface.query.filter_by(id=id).first()
        project, models = get_pro_mo()
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            intername=request.form.get('inter_name')
            url=request.form.get('url')
            meth=request.form.get('meth')
            reques=request.form.get('reque')
            back=request.form.get('back')
            if projecct ==None or model==None or intername=='' or url=='' or meth=='' or back=='':
                flash(u'请确定各项参数都正常填写')
                return render_template('edit_inter.html', interface=interface, projects=project, models=models)
            project_id = Project.query.filter_by(project_name=projecct).first().id
            models_id = Model.query.filter_by(model_name=model).first().id
            interface.projects_id=project_id
            interface.model_id=models_id
            interface.Interface_name=intername
            interface.Interface_url=url
            interface.Interface_meth=meth
            interface.Interface_par=reques
            interface.Interface_back=back
            interface.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
            db.session.commit()
            return redirect(url_for('interface'))
        return render_template('edit_inter.html',interface=interface,projects=project,models=models)
class DeleinterView(MethodView):
    def get(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        interface=Interface.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if user.id==interface.Interface_user_id or user.role_id==2:
            interface.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('interface'))
        flash(u'您没有权限删除这条接口')
        return redirect(url_for('interface'))
class AddtestcaseView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not session.get('username'):
            return redirect(url_for('login'))
        form=Interface_yong_Form()
        project, models = get_pro_mo()
        if request.method=='POST' and form.validate_on_submit :
            yongli_nam=request.form.get('project')
            mode=request.form.get('model')
            interface_name=request.form.get('interface_name')
            interface_url=request.form.get('interface_url')
            interface_meth=request.form.get('interface_meth')
            interface_can=request.form.get('interface_can')
            interface_re=request.form.get('interface_rest')
            if yongli_nam ==None or mode==None or interface_name=='' or interface_url=='' or interface_meth=='' or interface_re=='':
                flash(u'请准确填写用例')
                return render_template('add_test_case.html',form=form,projects=project,models=models)
            project_id = Project.query.filter_by(project_name=yongli_nam).first().id
            models_id = Model.query.filter_by(model_name=mode).first().id
            try:
                newcase=InterfaceTest(projects_id=project_id,model_id=models_id,Interface_name=interface_name,Interface_url=interface_url,Interface_meth=interface_meth,Interface_pase=interface_can,Interface_assert=interface_re,Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                db.session.add(newcase)
                db.session.commit()
                flash(u'添加用例成功')
                return redirect(url_for('yongli'))
            except:
                flash(u'添加用例失败')
                return render_template('add_test_case.html',form=form,projects=project,models=models)
        return render_template('add_test_case.html',form=form,projects=project,models=models)
class Deletecase(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        testcase=InterfaceTest.query.filter_by(id=id).first()
        user=User.query.filter_by(username=session.get('username')).first()
        if testcase.Interface_user_id==user.id or user.role_id==2:
            testcase.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('yongli'))
        flash(u'您没有权限去删除这条用例')
        return redirect(url_for('yongli'))
class EditcaseView(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        project, models = get_pro_mo()
        edit_case=InterfaceTest.query.filter_by(id=id).first()
        if request.method=='POST':
            yongli_nam = request.form.get('project')
            mode = request.form.get('model')
            url=request.form.get('url')
            meth=request.form.get('meth')
            parme=request.form.get('parme')
            reque=request.form.get('reque')
            if yongli_nam ==None  or mode== None or url=='' or meth==''  or reque=='':
                flash(u'请确定各项参数都正常填写')
                return render_template('edit_case.html',edit=edit_case,projects=project,models=models)
            projects_id = Project.query.filter_by(project_name=yongli_nam).first().id
            model_id = Model.query.filter_by(model_name=mode).first().id
            edit_case.projects_id=projects_id
            edit_case.model_id=model_id
            edit_case.Interface_url=url
            edit_case.Interface_meth=meth
            edit_case.Interface_pase=parme
            edit_case.Interface_assert=reque
            edit_case.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
            db.session.commit()
            flash(u'编辑成功')
            return redirect(url_for('yongli'))
        return render_template('edit_case.html',edit=edit_case,projects=project,models=models)
@app.route('/down_jiekou',methods=['GET'])
def down_jiekou():
    if not session.get('username'):
        return redirect(url_for('login'))
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
        if not session.get('username'):
            return redirect(url_for('login'))
        if request.method == 'POST':
            file = request.files['myfile']
            if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
                filename='jiekou.xlsx'
                file.save(filename)
                jiekou_bianhao,interface_name,project_nam, model_nam, interface_url, interface_meth, interface_par, interface_bas = pasre_inter(filename)
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first().id
                        model_id = Model.query.filter_by(model_name=project_nam[i]).first().id
                        new_interface=Interface(projects_id=projects_id,model_id=model_id,Interface_name=str(interface_name[i]),Interface_url=str(interface_url[i]),Interface_meth=str(interface_meth[i]),Interface_par=(interface_par[i]),Interface_back=str(interface_bas[i]),Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                        db.session.add(new_interface)
                    db.session.commit()
                    flash(u'导入成功')
                    return redirect(url_for('interface'))
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
                jiekou_bianhao,interface_name,project_nam, model_nam, interface_url, interface_meth, interface_par, interface_bas = pasre_inter(filename)
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first().id
                        model_id = Model.query.filter_by(model_name=model_nam[i]).first().id
                        new_interface = InterfaceTest(projects_id=projects_id, model_id=model_id,Interface_name=str(interface_name[i]), Interface_url=str(interface_url[i]),Interface_meth=str(interface_meth[i]), Interface_pase=(interface_par[i]),Interface_assert=str(interface_bas[i]),Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
                        db.session.add(new_interface)
                    db.session.commit()
                    flash(u'导入成功')
                    return redirect(url_for('yongli'))
                except:
                    flash(u'导入失败，请检查格式是否正确')
                    return render_template('daoru_case.html')
            flash(u'导入失败')
            return render_template('daoru_case.html')
        return  render_template('daoru_case.html')
class AdduserView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self):
        wrok=Work.query.all()
        if request.method =='POST':
            user=request.form.get('user')
            password=request.form.get('password')
            password1=request.form.get('password1')
            email=request.form.get('email')
            work=request.form.get('work')
            if email =='' or user =='':
                flash(u'请准确填写用户信息')
                return render_template('add_user.html',wroks=wrok)
            if password!= password1:
                flash(u'请确定两次密码是否一致')
                return render_template('add_user.html',wroks=wrok)
            use=User.query.filter_by(username=user).first()
            if use:
                flash(u'用户已经存在')
                return render_template('add_user.html',wroks=wrok)
            emai=User.query.filter_by(user_email=email).first()
            if emai:
                flash(u'邮箱已经存在')
                return render_template('add_user.html',wroks=wrok)
            new_user=User(username=user,user_email=email)
            new_user.set_password(password)
            new_user.work_id=work
            db.session.add(new_user)
            db.session.commit()
            flash(u'添加成功')
            return redirect(url_for('adminuser'))
        return render_template('add_user.html',wroks=wrok)
class SetadView(View):
    methods=['GET','POST']
    @admin_required
    @login_required
    def dispatch_request(self,id):
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id!=2:
            flash(u'您不是管理员，无法设置！')
            return redirect(url_for('adminuser'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.role_id==2:
            flash(u'已经是管理员，无需设置')
            return redirect(url_for('adminuser'))
        new_ad.role_id=2
        db.session.commit()
        flash(u'已经是管理员')
        return redirect(url_for('adminuser'))
class DeladView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self,id):
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id!=2:
            flash(u'您不是管理员，无法取消管理！')
            return redirect(url_for('adminuser'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad==user:
            flash(u'自己不能取消自己的管理员')
            return redirect(url_for('adminuser'))
        new_ad.role_id=1
        db.session.commit()
        flash(u'已经取消管理员权限')
        return redirect(url_for('adminuser'))
class FreadView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self,id):
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id!=2:
            flash(u'您不是管理员，无法冻结！')
            return redirect(url_for('adminuser'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.status==1:
            flash(u'已经冻结')
            return redirect(url_for('adminuser'))
        if new_ad==user:
            flash(u'自己不能冻结自己')
            return redirect(url_for('adminuser'))
        new_ad.status=1
        db.session.commit()
        flash(u'已经冻结')
        return redirect(url_for('adminuser'))
class FrereView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self,id):
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id!=2:
            flash(u'您不是管理员，无法解冻！')
            return redirect(url_for('adminuser'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.status==0:
            flash(u'已经解冻')
            return redirect(url_for('adminuser'))
        if new_ad==user:
            flash(u'自己不能解冻自己')
            return redirect(url_for('adminuser'))
        new_ad.status=0
        db.session.commit()
        flash(u'已经解冻')
        return redirect(url_for('adminuser'))
class RedpassView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        user=User.query.filter_by(username=session.get('username')).first()
        if user.role_id!=2:
            flash(u'您不是管理员，重置密码！')
            return redirect(url_for('adminuser'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad==user:
            flash(u'自己不能重置自己的密码')
            return redirect(url_for('adminuser'))
        new_ad.set_password=111111
        db.session.commit()
        flash(u'已经重置！密码：111111')
        return redirect(url_for('adminuser'))
class SeruserView(View):
    methods=['GET','POST']
    @admin_required
    def dispatch_request(self):
        if request.method=='POST':
            user=request.form.get('user')
            if user=='':
                flash(u'请输入您要查询的用户')
                return redirect(url_for('adminuser'))
            try:
                use=User.query.filter(User.username.like('%'+user+'%')).all()
                if len(use)<=0:
                    flash(u'没有找到您输入的用户')
                    return redirect(url_for('adminuser'))
                return render_template('user_ser.html',users=use)
            except:
                flash(u'没有找到您输入的用户')
                return redirect(url_for('adminuser'))
        return redirect(url_for('adminuser'))
class SeryongliView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        project=Project.query.all()
        models=Model.query.all()
        if not session.get('username'):
            return redirect(url_for('login'))
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            if projecct =='':
                interd=InterfaceTest.query.filter(InterfaceTest.model_id==int(model)).all()
                return render_template('ser_yonglo.html',yonglis=interd,projects=project,models=models)
            if model =='':
                interd=InterfaceTest.query.filter(InterfaceTest.projects_id==int(projecct)).all()
                return render_template('ser_yonglo.html',yonglis=interd,projects=project,models=models)
            interd=InterfaceTest.query.filter(InterfaceTest.projects_id==int(projecct),InterfaceTest.model_id==int(model)).all()
            return render_template('ser_yonglo.html',yonglis=interd,projects=project,models=models)
        return redirect(url_for('yongli'))
class SerinterView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not session.get('username'):
            return redirect(url_for('login'))
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
                    return redirect(url_for('interface'))
                return render_template('ser_inter.html',inte=interd)
            except:
                flash(u'搜索的内容不存在')
                return redirect(url_for('interface'))
        return redirect(url_for('interface'))
class TestrepView(View):
    methods=['GET','POST']
    def dispatch_request(self,page=1):
        if not session.get('username'):
            return redirect(url_for('login'))
        pagination=TestResult.query.paginate(page, per_page=20,error_out=False)
        inter=pagination.items
        return render_template('test_result.html',inte=inter,pagination=pagination)
class LoadView(View):
    methods=['GET']
    def dispatch_request(self,filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir=os.path.join(basedir,'upload')
        response=make_response(send_from_directory(file_dir,filename,as_attachment=True))
        return response
class MakeonecaseView(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return redirect(url_for('login'))
        case=InterfaceTest.query.filter_by(id=id).first()
        me=Api(url=case.Interface_url,fangshi=case.Interface_meth,params=case.Interface_pase)
        result=me.testapi()
        retur_re=assert_in(case.Interface_assert,result)
        try:
            if retur_re=='pass':
                flash(u'用例测试通过')
                return redirect(url_for('yongli'))
            flash(u'用例测试失败')
            return redirect(url_for('yongli'))
        except:
            flash(u'用例测试失败,请检查您的用例')
            return redirect(url_for('yongli'))
class DuoyongliView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not session.get('username'):
            return redirect(url_for('login'))
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
            if (len(set(projecct_list)))>1:
                flash('目前单次只能执行一个项目')
                return redirect(url_for('yongli'))
            if f =='on':
                email=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True).first()
                if email:
                    try:
                        apitest=ApiTestCase(Interface_url_list,Interface_meth_list,Interface_pase_list,Interface_assert_list,file)
                        result_toal,result_pass,result_fail,relusts,bask_list=apitest.testapi()
                        endtime=datetime.datetime.now()
                        end = time.time()
                        createHtml(titles=u'接口测试报告',filepath=filepath,starttime=starttime,endtime=endtime,passge=result_pass,fail=result_fail,id=id_list,name=projecct_list,key=model_list,coneent=Interface_url_list,url=Interface_meth_list,meth=Interface_pase_list,yuqi=Interface_assert_list,json=bask_list,relusts=relusts)
                        hour=end-star
                        user_id=User.query.filter_by(username=session.get('username')).first().id
                        new_reust=TestResult(Test_user_id=user_id,test_num=result_toal,pass_num=result_pass,fail_num=result_fail,test_time=starttime,hour_time=hour,test_rep=(day+'.html'),test_log=(day+'.log'))
                        db.session.add(new_reust)
                        db.session.commit()
                        m=send_emails(sender=email.send_email,receivers=email.to_email,password=email.send_email_password,smtp=email.stmp_email,port=email.port,fujian1=file,fujian2=filepath,subject=u'%s用例执行测试报告'%day,url='http://127.0.0.1:5000/test_rep')
                        if m==False:
                            flash(u'发送邮件失败，请检查您默认的邮件设置是否正确')
                            return redirect(url_for('test_rep'))
                        flash(u'测试已经完成，并且给您默认设置发送了测试报告')
                        return redirect(url_for('test_rep'))
                    except:
                        flash(u'测试失败，请检查您的测试用例单个执行是否出错')
                        return redirect(url_for('yongli'))
                flash(u'无法完成，需要去您的个人设置去设置一个默认的邮件发送')
                return redirect(url_for('yongli'))
            try:
                apitest=ApiTestCase(Interface_url_list,Interface_meth_list,Interface_pase_list,Interface_assert_list,file)
                result_toal,result_pass,result_fail,relusts,bask_list=apitest.testapi()
                endtime=datetime.datetime.now()
                end = time.time()
                createHtml(titles=u'接口测试报告',filepath=filepath,starttime=starttime,endtime=endtime,passge=result_pass,fail=result_fail,id=id_list,name=projecct_list,key=model_list,coneent=Interface_url_list,url=Interface_meth_list,meth=Interface_pase_list,yuqi=Interface_assert_list,json=bask_list,relusts=relusts)
                hour=end-star
                user_id=User.query.filter_by(username=session.get('username')).first().id
                new_reust=TestResult(Test_user_id=user_id,test_num=result_toal,pass_num=result_pass,fail_num=result_fail,test_time=starttime,hour_time=hour,test_rep=(day+'.html'),test_log=(day+'.log'))
                db.session.add(new_reust)
                db.session.commit()
                flash(u'测试已经完成')
                return redirect(url_for('test_rep'))
            except:
                flash(u'测试失败，请检查您的测试用例单个执行是否出错')
                return redirect(url_for('yongli'))
        return redirect(url_for('yongli'))
class ProjectView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('login'))
        projects=Project.query.filter_by(status=False).all()
        return  render_template('project.html',projects=projects)
class ModelView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('login'))
        models=Model.query.filter_by(status=False).all()
        return  render_template('model.html',projects=models)
class AddmodelView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('login'))
        if request.method=="POST":
            model=request.form.get('project')
            if model=='':
                flash(u'请添加您的模块名')
                return render_template('add_moel.html')
            user_id=User.query.filter_by(username=session.get('username')).first().id
            models=Model.query.filter_by(model_name=model).first()
            if models:
                flash(u'模块不能重复')
                return render_template('add_moel.html')
            new_moel=Model(model_name=model,model_user_id=user_id)
            db.session.add(new_moel)
            db.session.commit()
            flash(u'添加成功!')
            return  redirect(url_for('model'))
        return  render_template('add_moel.html')
class AddproView(View):
    methods=['GET','POST']
    def dispatch_request(self):
        if not  session.get('username'):
            return  redirect(url_for('login'))
        if request.method=="POST":
            model=request.form.get('project')
            if model=='':
                flash(u'请添加您的项目名')
                return render_template('add_pro.html')
            user_id=User.query.filter_by(username=session.get('username')).first().id
            projec=Project.query.filter_by(project_name=model).first()
            if projec:
                flash(u'项目不能重复')
                return render_template('add_pro.html')
            new_moel=Project(project_name=model,project_user_id=user_id)
            db.session.add(new_moel)
            db.session.commit()
            flash(u'添加成功!')
            return  redirect(url_for('project'))
        return  render_template('add_pro.html')
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
            return redirect(url_for('model'))
        flash(u'您没有权限删除这个模块')
        return redirect(url_for('model'))
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
            return redirect(url_for('project'))
        flash(u'您没有权限删除这个项目')
        return redirect(url_for('project'))
class EditmoelView(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return  redirect(url_for('login'))
        user = User.query.filter_by(username=session.get('username')).first()
        model=Model.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('model')
            if ed_mode=='':
                flash(u'请添加模块名')
                return render_template('edit_model.html', mode=model)
            models = Model.query.filter_by(model_name=ed_mode).first()
            model.model_name=ed_mode
            db.session.commit()
            flash(u'编辑成功')
            return  redirect(url_for('model'))
        return  render_template('edit_model.html',mode=model)
class EditproView(View):
    methods=['GET','POST']
    def dispatch_request(self,id):
        if not session.get('username'):
            return  redirect(url_for('login'))
        user = User.query.filter_by(username=session.get('username')).first()
        project=Project.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('project')
            if ed_mode=='':
                flash(u'请添加项目')
                return render_template('edit_pro.html', project=project)
            models = Project.query.filter_by(project_name=ed_mode).first()
            project.project_name=ed_mode
            db.session.commit()
            flash(u'编辑成功')
            return  redirect(url_for('project'))
        return  render_template('edit_pro.html',project=project)
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
            return redirect(url_for('test_rep'))
        flash(u'您没有权限去删除测试报告')
        return redirect(url_for('test_rep'))
class Set_emaiView(MethodView):
    @login_required
    def get(self):
        user=User.query.filter_by(username=session.get('username')).first().id
        email_report=EmailReport.query.filter_by(email_re_user_id=user).all()
        if len(email_report)<=0:
            return render_template('set_send.html',errmessage=u'您还没有设置发送测试报告邮件')
        return render_template('set_send.html',email_reports=email_report)
class Add_emaiView(MethodView):
    @login_required
    def get(self):
        form=Set_email_Form()
        return render_template('add_emali.html',form=form)
    @login_required
    def post(self):
        form=Set_email_Form()
        if form.validate_on_submit():
            email=request.form.get('send_email')
            password=request.form.get('password')
            shi_f=request.form.get('checkbox')
            resv_email=request.form.get('email')
            resv_email=(str(resv_email).split(','))
            port=request.form.get('port')
            stmp_email=request.form.get('stmp_email')
            if email =='' or password=='' or resv_email=='' or post=='' or stmp_email =='':
                flash(u'请准确填写信息')
                return render_template('add_emali.html',form=form)
            user_id=current_user.id
            if shi_f =='on':
                shi_f=True
                user_is=EmailReport.query.filter_by(email_re_user_id=user_id,default_set=True).first()
                if user_is:
                    flash(u'只能有一个为默认设置')
                    return render_template('add_emali.html',form=form)
                email_new=EmailReport(email_re_user_id=int(user_id),send_email=str(email),send_email_password=str(password),to_email=str(resv_email),default_set=True,port=int(port),stmp_email=str(stmp_email))
                db.session.add(email_new)
                db.session.commit()
                flash(u'成功设置一个默认配置')
                return redirect(url_for('setting'))
            email_new=EmailReport(email_re_user_id=int(user_id),send_email=str(email),send_email_password=str(password),to_email=str(resv_email))
            db.session.add(email_new)
            db.session.commit()
            flash(u'成功设置一个配置')
            return redirect(url_for('setting'))
        return render_template('add_emali.html',form=form)
class DeleteView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        email_re=EmailReport.query.filter_by(id=id).first()
        user_id=current_user.id
        if email_re.email_re_user_id==int(user_id):
            email_re.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('setting'))
        flash(u'您没有权限删除')
        return redirect(url_for('setting'))
class EditemailView(MethodView):
    @login_required
    def get(self,id):
        emai=EmailReport.query.filter_by(id=id).first()
        return render_template('edit_emali.html',emai=emai)
    @login_required
    def post(self,id):
        emai=EmailReport.query.filter_by(id=id).first()
        email=request.form.get('send_email')
        password=request.form.get('password')
        shi_f=request.form.get('checkbox')
        resv_email=request.form.get('email')
        resv_email=(str(resv_email).split(','))
        stmp_em=request.form.get('stmp')
        port=request.form.get('port')
        if email =='' or password=='' or resv_email=='' or stmp_em =='' or port =='':
            flash(u'请准确填写信息')
            return render_template('edit_emali.html',emai=emai)
        user_id=current_user.id
        if shi_f =='on':
            shi_f=True
            user_is=EmailReport.query.filter_by(email_re_user_id=user_id,default_set=True).first()
            if user_is:
                flash(u'只能有一个为默认设置')
                return render_template('edit_emali.html',emai=emai)
            emai.email_re_user_id=int(user_id)
            emai.send_email=str(email)
            emai.send_email_password=str(password)
            emai.to_email=str(resv_email)
            emai.stmp_email=str(stmp_em)
            emai.port=int(port)
            emai.default_set=True
            db.session.commit()
            flash(u'编辑成功')
            return redirect(url_for('setting'))
        emai.email_re_user_id=int(user_id)
        emai.send_email=str(email)
        emai.send_email_password=str(password)
        emai.to_email=str(resv_email)
        emai.stmp_email=str(stmp_em)
        emai.port=int(port)
        db.session.commit()
        flash(u'编辑成功')
        return redirect(url_for('setting'))
class QuzhiMoView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        del_em=EmailReport.query.filter_by(id=id).first()
        if del_em:
            if int(current_user.id)==del_em.email_re_user_id:
                del_e=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True).all()
                del_em.default_set=False
                db.session.commit()
                flash(u'取消默认成功')
                return redirect(url_for('setting'))
            flash(u'您没有权限来取消')
            return redirect(url_for('setting'))
        flash(u'你要取消的默认不存在')
        return redirect(url_for('setting'))
class ShezhiMoView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        shezi_em=EmailReport.query.filter_by(id=id).first()
        if shezi_em:
            if int(current_user.id)==shezi_em.email_re_user_id:
                del_e=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True).all()
                if len(del_e)>0:
                    flash(u'一个账户只能有一个默认设置')
                    return redirect(url_for('setting'))
                shezi_em.default_set=True
                db.session.commit()
                flash(u'设置默认成功')
                return redirect(url_for('setting'))
            flash(u'您没有权限来设置')
            return redirect(url_for('setting'))
        flash(u'你要设置的默认邮箱配置不存在')
        return redirect(url_for('setting'))
class TestrepoView(MethodView):
    @login_required
    def get(self):
        user_test=TestResult.query.filter_by(Test_user_id=int(current_user.id)).all()
        project=[]
        test_prco=[]
        riqi=[]
        for i in range(len(user_test)):
            project.append((user_test[i]).projects.project_name)
            test_prco.append({(user_test[i]).projects.project_name:(int(user_test[i].pass_num)/int(user_test[i].test_num))*100})
            riqi.append( user_test[i].test_time.strftime( '%y-%m-%d %H:%M'))
        return jsonify({'data':list(set(project)),'num':test_prco,'riqi':riqi})