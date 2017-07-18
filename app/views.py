# encoding: utf-8
"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app,db
from  flask import  redirect,request,render_template,session,url_for,flash,send_file,abort,make_response
from werkzeug import secure_filename
from  app.models import User,Interface,InterfaceTest,TestResult
from app.form import  LoginFrom,RegFrom,InterForm,Interface_yong_Form
import os
@app.route('/',methods=['GET'])
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    interface_cont=len(Interface.query.all())
    interfaceTest_cunt=len(InterfaceTest.query.all())
    resu_cout=len(TestResult.query.all())
    if not session.get('username'):
        return  redirect(url_for('login'))
    return  render_template('index.html',yongli=interfaceTest_cunt,jiekou=interface_cont,report=resu_cout)
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginFrom()
    if request.method=='POST' and form.validate_on_submit():
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password=password)==True:
                session['username']=username
                return  redirect(url_for('index'))
            flash('用户名密码错误')
            return render_template('login.html', form=form)
        flash('用户名不存在')
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
            flash('请确认两次密码输入是否一致')
            return render_template('reg.html',form=form)
        user=User.query.filter_by(username=usernmae).first()
        if user:
            flash('用户名已经存在')
            return render_template('reg.html', form=form)
        emai=User.query.filter_by(user_email=email).first()
        if emai:
            flash('邮箱已经注册')
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
    pagination=Interface.query.paginate(page, per_page=10,error_out=False)
    inter=pagination.items
    return  render_template('interface.html',inte=inter,pagination=pagination)
@app.route('/yongli',methods=['GET','POST'])
@app.route('/yongli/<int:page>',methods=['GET','POST'])
def yongli(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    pagination=InterfaceTest.query.paginate(page, per_page=10,error_out=False)
    yongli=pagination.items
    return  render_template('interface_yongli.html',yonglis=yongli,pagination=pagination)
@app.route('/adminuser',methods=['GET','POST'])
@app.route('/adminuser/<int:page>',methods=['GET','POST'])
def adminuser(page=1):
    if not session.get('username'):
        return redirect(url_for('login'))
    user=User.query.filter_by(username=session.get('username')).first()
    if user.level!=1:
        flash('您没有权限进入管理中心')
        return redirect(url_for('index'))
    pagination=User.query.paginate(page, per_page=10,error_out=False)
    users=pagination.items
    return render_template('useradmin.html',users=users,pagination=pagination)
@app.route('/interface_add',methods=['GET','POST'])
def interface_add():
    if not session.get('username'):
        return redirect(url_for('login'))
    form=InterForm()
    if form.validate_on_submit and request.method =="POST":
        project_name=request.form.get('project_name')
        model_name=request.form.get('model_name')
        interface_name=request.form.get('interface_name')
        interface_url=request.form.get('interface_url')
        interface_meth=request.form.get('interface_meth')
        interface_par=request.form.get('interface_par')
        interface_bas=request.form.get('interface_bas')
        if project_name == '' or model_name =='' or interface_name=='' or interface_url =='' or interface_meth=='':
            flash('请准确的填写接口的各项信息')
            return render_template('add_interface.html',form=form)
        user_id=User.query.filter_by(username=session.get('username')).first().id
        new_interface=Interface(
            project_name=project_name,models_name=model_name,Interface_name=interface_name,Interface_url=interface_url,
            Interface_meth=interface_meth,Interface_par=interface_par,Interface_back=interface_bas,Interface_user_id=user_id
            )
        db.session.add(new_interface)
        db.session.commit()
        return redirect(url_for('interface'))
    return render_template('add_interface.html',form=form)
@app.route('/edit_interface/<int:id>',methods=['GET','POST'])
def interfac_edit(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    interface=Interface.query.filter_by(id=id).first()
    if request.method=='POST':
        projecct=request.form.get('project')
        model=request.form.get('model')
        intername=request.form.get('inter_name')
        url=request.form.get('url')
        meth=request.form.get('meth')
        reques=request.form.get('reque')
        back=request.form.get('back')
        if projecct =='' or model=='' or intername=='' or url=='' or meth=='' or back=='':
            flash('请确定各项参数都正常填写')
        interface.project_name=projecct
        interface.models_name=model
        interface.Interface_name=intername
        interface.Interface_url=url
        interface.Interface_meth=meth
        interface.Interface_par=reques
        interface.Interface_back=back
        interface.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
        db.session.commit()
        return redirect(url_for('interface'))
    return render_template('edit_inter.html',interface=interface)
@app.route('/dele_inter/<int:id>',methods=['GET','POST'])
def dele_inter(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    interface=Interface.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if user.id==interface.Interface_user_id or user.level==1:
        db.session.delete(interface)
        db.session.commit()
        flash('删除成功')
        return redirect(url_for('interface'))
    flash('您没有权限删除这条接口')
    return redirect(url_for('interface'))
@app.route('/addtestcase',methods=['GET','POST'])
def addtestcase():
    if not session.get('username'):
        return redirect(url_for('login'))
    form=Interface_yong_Form()
    if form.validate_on_submit() and request.method=='POST':
        yongli_name=request.form.get('yongli_name')
        interface_name=request.form.get('interface_name')
        interface_url=request.form.get('interface_url')
        interface_meth=request.form.get('interface_meth')
        interface_can=request.form.get('interface_can')
        interface_re=request.form.get('interface_rest')
        if yongli_name ==''or interface_name=='' or interface_url=='' or interface_meth=='' or interface_re=='':
            flash('请准确填写用例')
            return render_template('add_test_case.html',form=form)
        newcase=InterfaceTest(yongli_name=yongli_name,Interface_name=interface_name,Interface_url=interface_url,
            Interface_meth=interface_meth,Interface_pase=interface_can,Interface_assert=interface_re,Interface_user_id=User.query.filter_by(username=session.get('username')).first().id)
        db.session.add(newcase)
        db.session.commit()
        flash('添加用例成功')
        return redirect(url_for('yongli'))
    return render_template('add_test_case.html',form=form)
@app.route('/delete_case/<int:id>',methods=['GET','POST'])
def delete_case(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    testcase=InterfaceTest.query.filter_by(id=id).first()
    user=User.query.filter_by(username=session.get('username')).first()
    if testcase.Interface_user_id==user.id or user.level==1:
        db.session.delete(testcase)
        db.session.commit()
        flash('删除成功')
        return redirect(url_for('yongli'))
    flash('您没有权限去删除这条用例')
    return redirect(url('yongli'))
@app.route('/edit_case/<int:id>',methods=['GET','POST'])
def edit_case(id):
    if not session.get('username'):
        return redirect(url_for('login'))
    edit_case=InterfaceTest.query.filter_by(id=id).first()
    if request.method=='POST':
        projecct=request.form.get('project')
        model=request.form.get('model')
        url=request.form.get('url')
        meth=request.form.get('meth')
        parme=request.form.get('parme')
        reque=request.form.get('reque')
        if projecct =='' or model=='' or url=='' or meth=='' or parme=='' or reque=='':
            flash('请确定各项参数都正常填写')
        edit_case.yongli_name=projecct
        edit_case.Interface_name=model
        edit_case.Interface_url=url
        edit_case.Interface_meth=meth
        edit_case.Interface_pase=parme
        edit_case.Interface_assert=reque
        interface.Interface_user_id=User.query.filter_by(username=session.get('username')).first().id
        db.session.commit()
        flash('编辑成功')
        return redirect(url_for('yongli'))
    return render_template('edit_case.html',edit=edit_case)
@app.route('/down_jiekou',methods=['GET'])
def down_jiekou():
    response = make_response(send_file("接口.xlsx"))
    return response
@app.route('/down_case',methods=['GET'])
def down_case():
    response=make_response(send_file('测试用例.xlsx'))
    return response
@app.route('/daoru_inter',methods=['GET','POST'])
def daoru_inter():
    if request.method == 'POST':
        file = request.files['myfile']
        if file and '.' in file.filename and file.filename.split('.')[1]=='xlsx':
            filename='jiekou.xlsx'
            file.save(filename)
            flash('导入成功')
            return redirect(url_for('index'))
        flash('导入失败')
        return render_template('daoru.html')
    return render_template('daoru.html')