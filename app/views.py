"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app
from  flask import  redirect,request,render_template,session,url_for,flash,make_response,send_from_directory,jsonify
from  app.models import *
from app.form import  *
import os
from flask.views import MethodView,View
from flask_login import current_user,login_required
from app.common.decorators import chckuserpermisson
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
@app.route('/down_jiekou',methods=['GET'])
@login_required
def down_jiekou():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir=os.path.join(basedir,'upload')
    response=make_response(send_from_directory(file_dir,'interface.xlsx',as_attachment=True))
    return response
@app.route('/down_case',methods=['GET'])
@login_required
def down_case():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir=os.path.join(basedir,'upload')
    response=make_response(send_from_directory(file_dir,'interface_case.xlsx',as_attachment=True))
    return response
class LoadView(View):
    methods=['GET']
    def dispatch_request(self,filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir=os.path.join(basedir,'upload')
        response=make_response(send_from_directory(file_dir,filename,as_attachment=True))
        return response
class AddmodelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
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
            try:
                db.session.commit()
                flash(u'%s模块 添加成功!'%model)
                return  redirect( url_for('home.model'))
            except:
                db.session.rollback()
                flash(u'%s模块 添加失败！！'%model)
                return redirect(url_for('home.model'))
        return  render_template('add/add_moel.html')
class AddproView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if current_user.is_sper == False:
            flash('权限不足，不能添加项目')
            return  redirect(request.headers.get('Referer'))
        if request.method=="POST":
            model=request.form.get('project')
            if model=='':
                flash(u'请添加您的项目名')
                return render_template('add/add_pro.html')
            user_id=User.query.filter_by(username=session.get('username')).first().id
            projec=Project.query.filter_by(project_name=model).first()
            if projec:
                flash(u'%s项目  不能重复'%model)
                return render_template('add/add_pro.html')
            new_moel=Project(project_name=model,project_user_id=user_id)
            db.session.add(new_moel)
            try:
                db.session.commit()
                flash(u'%s项目   添加成功!'%model)
                return  redirect(url_for('home.project'))
            except:
                db.session.rollback()
                flash(u'添加guo程总是不理想!')
                return redirect(url_for('home.project'))
        return  render_template('add/add_pro.html')
class DelemodelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        next = request.headers.get('Referer')
        model=Model.query.filter_by(id=id).first()
        model.status=True
        db.session.commit()
        flash(u'删除成功')
        return redirect(next or url_for('home.model'))
class DeleproView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if  current_user.is_sper == False:
            flash('权限不足，不能删除项目')
            return redirect(request.headers.get('Referer'))
        proje=Project.query.filter_by(id=id).first()
        proje.status=True
        db.session.commit()
        flash(u'删除成功')
        return redirect( url_for('home.project'))
class EditmoelView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        model=Model.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('model')
            if ed_mode=='':
                flash(u'请添加模块名')
                return render_template('edit/edit_model.html', mode=model)
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
        if current_user.is_sper==False:
            flash('权限不足,')
            return  redirect(url_for('home.project'))
        project=Project.query.filter_by(id=id).first()
        if request.method=="POST":
            ed_mode=request.form.get('project')
            if ed_mode=='':
                flash(u'请添加项目')
                return render_template('edit/edit_pro.html', project=project)
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
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能删除测试报告')
            return  redirect(request.headers.get('Referer'))
        delTest=TestResult.query.filter_by(id=id).first()
        delTest.status=True
        db.session.commit()
        flash(u'删除成功')
        return redirect( url_for('home.test_rep'))
class ADDTesteventView(MethodView):#添加测试环境
    @login_required
    def get(self):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    projects.append(i.projects)
                    id.append(i.projects)
        if len(projects)<=0:
            flash(u'你没有所属的项目，请在后台添加')
            return redirect(url_for('home.ceshihuanjing'))
        forms=Interface_Env()
        return render_template('add/add_even.html', form=forms, projects=projects)
    @login_required
    def post(self):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    projects.append(i.projects)
                    id.append(i.projects)
        if len(projects)<=0:
            flash(u'你没有所属的项目，请在后台添加')
            return redirect(url_for('home.ceshihuanjing'))
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
                flash('添加测试用例成功！')
                return redirect(url_for('home.ceshihuanjing'))
            except:
                db.session.rollback()
                return redirect(url_for('home.ceshihuanjing'))
        return render_template('add/add_even.html', form=forms, projects=projects)
class DeleteEventViews(MethodView):#删除测试环境
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        event=Interfacehuan.query.filter_by(id=id).first()
        event.status=True
        db.session.commit()
        flash(u'删除成功')
        return  redirect(next or url_for('home.ceshihuanjing'))
class EditEventViews(MethodView):#编辑测试环境
    @login_required
    def get(self,id):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    projects.append(i.projects)
                    id.append(i.projects)
        if len(projects)<=0:
            flash(u'你没有所属的项目，请在后台添加')
            return redirect(url_for('home.ceshihuanjing'))
        event=Interfacehuan.query.filter_by(id=id).first()
        return  render_template('edit/edit_events.html', enents=event, projects=projects)
    def post(self,id):
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    projects.append(i.projects)
                    id.append(i.projects)
        if len(projects)<=0:
            flash(u'你没有所属的项目，请在后台添加')
            return redirect(url_for('home.ceshihuanjing'))
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
            return render_template('edit/edit_events.html', enents=event, projects=projects)
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
@app.route('/getprojects',methods=['GET','POST'])
@login_required
def getprojects():
    id = request.get_data('id')
    if not id:
        return jsonify({'msg':'没有发送数据','code':108})
    peoject=InterfaceTest.query.filter_by(id=int(id)).first()
    result=peoject.projects
    testhuanjing=Interfacehuan.query.filter_by(project=result.project_name).all()
    if len(testhuanjing)<=0:
        return jsonify({'msg': '没有找到测试环境','code':107,'data':str(result)})
    url_list=[]
    for huanjing in testhuanjing:
        url_list.append(huanjing.url)
    if not  peoject:
        return jsonify({'data':'数据库找不到项目','code':109})
    return  jsonify({'data':str(result),'huanjing':url_list,'code':200})
@app.route('/getyongli',methods=['GET','POST'])
def getyongli():
    id = request.get_data('id')
    project=id.decode('utf-8')
    if not project:
        return jsonify({'msg':'没有发送数据','code':108})
    peoject = Project.query.filter_by(project_name=project).first()
    if not  peoject:
        return jsonify({'msg': '数据库找不到项目', 'code': 109})
    tesatcaelist=InterfaceTest.query.filter_by(projects_id=peoject.id,status=False).all()
    caselit=[]
    for i in tesatcaelist:
        caselit.append(i.id)
    return  jsonify({'code':200,'msg':'成功','data':(caselit)})