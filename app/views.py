# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app,db
from  flask import  redirect,request,render_template,session,url_for,flash
from  app.models import User,Interface,InterfaceTest,TestResult
from app.form import  LoginFrom,RegFrom
@app.route('/',methods=['GET'])
def index():
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
def interface():
    return  render_template('interface.html')
@app.route('/yongli',methods=['GET','POST'])
def yongli():
    return  render_template('interface_yongli.html')
