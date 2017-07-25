# encoding: utf-8
"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app,db
from  flask import  redirect,request,render_template,session,url_for,flash,send_file,abort,make_response,send_from_directory
from werkzeug import secure_filename
from  app.models import User,Interface,InterfaceTest,TestResult,Project,Model
from app.form import  LoginFrom,RegFrom,InterForm,Interface_yong_Form
import os,time,datetime,threading
from app.common.pares_excel_inter import pasre_inter
from app.common.py_Html import createHtml
from app.common.requ_case import Api
from app.test_case.Test_case import ApiTestCase
from app.common.py_Html import createHtml
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
@app.route('/',methods=['GET'])
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    interface_cont=Interface.query.count()
    interfaceTest_cunt=InterfaceTest.query.count()
    resu_cout=TestResult.query.count()
    project_cout=Project.query.count()
    model_cout=Model.query.count()
    return  render_template('index.html',yongli=interfaceTest_cunt,jiekou=interface_cont,report=resu_cout,project_cout=project_cout,model_cout=model_cout)
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginFrom()
    if request.method=='POST' and form.validate_on_submit():
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password=password)==True:
                if user.status==0:
                    session['username']=username
                    return  redirect(url_for('index'))
                flash(u'用户冻结，请联系管理员')
                return render_template('login.html', form=form)
            flash(u'用户名密码错误')
            return render_template('login.html', form=form)
        flash(u'用户名不存在')
        return  render_template('login.html',form=form)
    return  render_template('login.html',form=form)
@app.route('/reg',methods=['GET','POST'])
def reg():
    form=RegFrom()
    if request.method=='POST' and form.validate_on_submit():
        usernmae=request.form.get('username')
        pasword=request.form.get('password')
        setpasswod=request.form.get('se_password')
        email=request.form.get('email')
        if pasword !=setpasswod:
            flash(u'请确认两次密码输入是否一致')
            return render_template('reg.html',form=form)
        user=User.query.filter_by(username=usernmae).first()
        if user:
            flash(u'用户名已经存在')
            return render_template('reg.html', form=form)
        emai=User.query.filter_by(user_email=email).first()
        if emai:
            flash(u'邮箱已经注册')
            return render_template('reg.html', form=form)
        new_user=User(username=usernmae,user_email=email)
        new_user.set_password(pasword)
        db.session.add(new_user)
        db.session.commit()
        return  redirect(url_for('login'))
    return  render_template('reg.html',form=form)
@app.route('/logt',methods=['GET','POST'])
def logt():
    session.clear()
    return redirect(url_for('login'))
@app.route('/interface',methods=['GET','POST'])
@app.route('/interface/<int:page>',methods=['GET','POST'])
def interface(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    pagination=Interface.query.paginate(page, per_page=20,error_out=False)
    inter=pagination.items
    return  render_template('interface.html',inte=inter,pagination=pagination)
@app.route('/yongli',methods=['GET','POST'])
@app.route('/yongli/<int:page>',methods=['GET','POST'])
def yongli(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    pagination=InterfaceTest.query.paginate(page, per_page=30,error_out=False)
    yongli=pagination.items
    return  render_template('interface_yongli.html',yonglis=yongli,pagination=pagination)
@app.route('/adminuser',methods=['GET','POST'])
@app.route('/adminuser/<int:page>',methods=['GET','POST'])
def adminuser(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level!=1:
        flash(u'您没有权限进入管理中心')
        return redirect(url_for('index'))
    pagination=User.query.paginate(page, per_page=20,error_out=False)
    users=pagination.items
    return render_template('useradmin.html',users=users,pagination=pagination)
@app.route('/interface_add',methods=['GET','POST'])
def interface_add():
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
            flash(u'请准确的填写接口的各项信息')
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
@app.route('/edit_interface/<int:id>',methods=['GET','POST'])
def interfac_edit(id):
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
@app.route('/dele_inter/<int:id>',methods=['GET','POST'])
def dele_inter(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    interface=Interface.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if user.id==interface.Interface_user_id or user.level==1:
        db.session.delete(interface)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('interface'))
    flash(u'您没有权限删除这条接口')
    return redirect(url_for('interface'))
@app.route('/addtestcase',methods=['GET','POST'])
def addtestcase():
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
@app.route('/delete_case/<int:id>',methods=['GET','POST'])
def delete_case(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    testcase=InterfaceTest.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if testcase.Interface_user_id==user.id or user.level==1:
        db.session.delete(testcase)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('yongli'))
    flash(u'您没有权限去删除这条用例')
    return redirect(url_for('yongli'))
@app.route('/edit_case/<int:id>',methods=['GET','POST'])
def edit_case(id):
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
        if yongli_nam ==None  or mode== None or url=='' or meth=='' or parme=='' or reque=='':
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
        interface.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
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
@app.route('/daoru_inter',methods=['GET','POST'])
def daoru_inter():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['myfile']
        if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
            filename='jiekou.xlsx'
            file.save(filename)
            model_names,project_name,model_name,interface_name,interface_url,interface_meth,interface_par,interface_bas=pasre_inter(filename)
            try:
                for i in range(len(project_name)):
                    projects_id = Project.query.filter_by(project_name=project_name[i]).first().id
                    model_id = Model.query.filter_by(model_name=model_name[i]).first().id
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
@app.route('/daoru_case',methods=['GET','POST'])
def daoru_case():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['myfile']
        if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
            filename='jiekoucase.xlsx'
            file.save(filename)
            jiekou_bianhao,project_nam, model_nam, interface_name, interface_url, interface_meth, interface_par, interface_bas = pasre_inter(filename)
            try:
                for i in range(len(project_nam)):
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
@app.route('/add_user',methods=['GET','POST'])
def add_user():
    if not session.get('username'):
        return  redirect(url_for('login'))
    if request.method =='POST':
        user=request.form.get('user')
        password=request.form.get('password')
        password1=request.form.get('password1')
        email=request.form.get('email')
        if password!= password1:
            flash(u'请确定两次密码是否一致')
            return render_template('add_user.html')
        use=User.query.filter_by(username=user).first()
        if use:
            flash(u'用户已经存在')
            return render_template('add_user.html')
        emai=User.query.filter_by(user_email=email).first()
        if emai:
            flash(u'邮箱已经存在')
            return render_template('add_user.html')
        new_user=User(username=user,user_email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('adminuser'))
    return render_template('add_user.html')
@app.route('/set_ad/<int:id>',methods=['GET','POST'])
def set_ad(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level !=1:
        flash(u'您不是管理员，无法设置！')
        return redirect(url_for('adminuser'))
    new_ad=User.query.filter_by(id=id).first()
    if new_ad.level==1:
        flash(u'已经是管理员，无需设置')
        return redirect(url_for('adminuser'))
    new_ad.level=1
    db.session.commit()
    flash(u'已经是管理员')
    return redirect(url_for('adminuser'))
@app.route('/del_ad/<int:id>',methods=['GET','POST'])
def del_ad(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level !=1:
        flash(u'您不是管理员，无法取消管理！')
        return redirect(url_for('adminuser'))
    new_ad=User.query.filter_by(id=id).first()
    if new_ad.level==0:
        flash(u'已经不是管理员，无需设置')
        return redirect(url_for('adminuser'))
    if new_ad==user:
        flash(u'自己不能取消自己的管理员')
        return redirect(url_for('adminuser'))
    new_ad.level=0
    db.session.commit()
    flash(u'已经取消管理员权限')
    return redirect(url_for('adminuser'))
@app.route('/fre_ad/<int:id>',methods=['GET','POST'])
def fre_ad(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level !=1:
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
@app.route('/fre_re/<int:id>',methods=['GET','POST'])
def fre_re(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level !=1:
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
@app.route('/red_pass/<int:id>',methods=['GET','POST'])
def red_pass(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level !=1:
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
@app.route('/ser_user',methods=['GET','POST'])
def ser_user():
    if not session.get('username'):
        return redirect(url_for('login'))
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
@app.route('/ser_yongli',methods=['GET','POST'])
def ser_yongli():
    if not session.get('username'):
        return redirect(url_for('login'))
    if request.method=='POST':
        projecct=request.form.get('project')
        model=request.form.get('model')
        if projecct =='' and model  =='':
            flash(u'请输入搜索的内容')
            return redirect(url_for('yongli'))
        try:
            projects_id = Project.query.filter_by(project_name=projecct).first().id
            model_id = Model.query.filter_by(model_name=model).first().id
            interd=InterfaceTest.query.filter(InterfaceTest.model_id.like('%'+str(model_id)+'%'),InterfaceTest.projects_id.like('%'+str(projects_id)+'%')).all()
            if len(interd)<1:
                flash(u'搜索的内容没有找到')
                return redirect(url_for('yongli'))
            return render_template('ser_yonglo.html',yonglis=interd)
        except:
            flash(u'搜索的内容没有找到')
            return redirect(url_for('yongli'))
    return redirect(url_for('yongli'))
@app.route('/ser_inter',methods=['GET','POST'])
def ser_inter():
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
@app.route('/test_rep',methods=['GET','POST'])
@app.route('/test_rep/<int:page>',methods=['GET','POST'])
def test_rep(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    pagination=TestResult.query.paginate(page, per_page=20,error_out=False)
    inter=pagination.items
    return render_template('test_result.html',inte=inter,pagination=pagination)
@app.route('/load/<string:filename>',methods=['GET'])
def load(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir=os.path.join(basedir,'upload')
    response=make_response(send_from_directory(file_dir,filename,as_attachment=True))
    return response
@app.route('/make_one_case/<int:id>',methods=['GET','POST'])
def make_one_case(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    case=InterfaceTest.query.filter_by(id=id).first()
    me=Api(url=case.Interface_url,fangshi=case.Interface_meth,params=case.Interface_pase)
    result=me.testapi()
    try:
        if result==eval(case.Interface_assert):
            flash(u'用例测试通过')
            return redirect(url_for('yongli'))
        flash(u'用例测试失败')
        return redirect(url_for('yongli'))
    except:
        flash(u'用例测试失败,请检查您的用例')
        return redirect(url_for('yongli'))
@app.route('/duoyongli',methods=['GET','POST'])
def duoyongli():
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
@app.route('/project',methods=['GET','POST'])
def project():
    if not  session.get('username'):
        return  redirect(url_for('login'))
    projects=Project.query.all()
    return  render_template('project.html',projects=projects)
@app.route('/model',methods=['GET','POST'])
def model():
    if not  session.get('username'):
        return  redirect(url_for('login'))
    models=Model.query.all()
    return  render_template('model.html',projects=models)
@app.route('/add_moel',methods=['GET','POST'])
def add_moel():
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
@app.route('/add_pro',methods=['GET','POST'])
def add_pro():
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
@app.route('/dele_moel/<int:id>',methods=['GET','POST'])
def dele_moel(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    model=Model.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if user.id==model.model_user_id or user.level==1:
        db.session.delete(model)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('model'))
    flash(u'您没有权限删除这个模块')
    return redirect(url_for('model'))
@app.route('/dele_pro/<int:id>',methods=['GET','POST'])
def dele_pro(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    proje=Project.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if user.id==proje.project_user_id or user.level==1:
        db.session.delete(proje)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('project'))
    flash(u'您没有权限删除这个项目')
    return redirect(url_for('project'))
@app.route('/edit_moel/<int:id>',methods=['GET','POST'])
def edit_moel(id):
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
        if models:
            flash(u'模块不能重复')
            return render_template('edit_model.html', mode=model)
        model.model_name=ed_mode
        db.session.commit()
        flash(u'编辑成功')
        return  redirect(url_for('model'))
    return  render_template('edit_model.html',mode=model)
@app.route('/edit_pro/<int:id>',methods=['GET','POST'])
def edit_pro(id):
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
        if models:
            flash(u'项目不能重复')
            return render_template('edit_pro.html', project=project)
        project.project_name=ed_mode
        db.session.commit()
        flash(u'编辑成功')
        return  redirect(url_for('project'))
    return  render_template('edit_pro.html',project=project)


