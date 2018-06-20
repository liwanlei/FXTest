"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app
from  flask import  redirect,request,render_template,url_for,flash,make_response,send_from_directory,jsonify
from  app.models import *
from app.form import  *
import os
from flask.views import MethodView,View
from flask_login import current_user,login_required
from common.decorators import chckuserpermisson
def get_pro_mo():
    projects=Project.query.filter_by(status=False).all()
    model=Model.query.filter_by(status=False).all()
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
class LoadView(MethodView):
    @login_required
    def get(self,filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir=os.path.join(basedir,'upload')
        response=make_response(send_from_directory(file_dir,filename,as_attachment=True))
        return response
class DeleteResultView(View):#删除测试报告
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能删除测试报告')
            return  redirect(request.headers.get('Referer'))
        delTest=TestResult.query.filter_by(id=id,status=False).first()
        if not  delTest:
            flash('要删除的测试报告不存在')
            return  redirect(url_for('home.test_rep'))
        delTest.status=True
        try:
            db.session.commit()
            flash(u'删除成功')
            return redirect( url_for('home.test_rep'))
        except Exception as e:
            db.session.rollback()
            flash('删除测试报告失败，原因：%s'%e)
            return  redirect(url_for('home.test_rep'))
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
        if i.status==True:
            continue
        else:
            testyong_list.append({'name':i.Interface_name,'id':i.id})
    return   jsonify({'data':testyong_list})
@app.route('/getprojects',methods=['GET','POST'])
@login_required
def getprojects():#获取项目
    id = request.get_data('id')
    if not id:
        return jsonify({'msg':'没有发送数据','code':108})
    peoject=InterfaceTest.query.filter_by(id=int(id)).first()
    result=peoject.projects
    projetc=Project.query.filter_by(project_name=str(result.project_name)).first()
    testhuanjing=Interfacehuan.query.filter_by(projects=projetc,status=False).all()
    if len(testhuanjing)<=0:
        return jsonify({'msg': '没有找到测试环境','code':107,'data':str(result)})
    url_list=[]
    for huanjing in testhuanjing:
        url_list.append(huanjing.url)
    if not  peoject:
        return jsonify({'msg':'数据库找不到项目','code':109,'data':''})
    return  jsonify({'data':str(result),'huanjing':url_list,'code':200,'msg':u'请求成功'})
class Getyongli(MethodView):#获取用例
    @login_required
    def post(self):
        id = request.get_data('id')
        project=id.decode('utf-8')
        if not project:
            return jsonify({'msg':'没有发送数据','code':8,'data':''})
        peoject = Project.query.filter_by(project_name=project,status=False).first()
        if not  peoject:
            return jsonify({'msg': '数据库找不到项目', 'code': 9,'data':''})
        tesatcaelist=InterfaceTest.query.filter_by(projects_id=peoject.id,status=False).all()
        caselit=[]
        for i in tesatcaelist:
            caselit.append(i.id)
        return  jsonify({'code':200,'msg':'成功','data':(caselit)})
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')