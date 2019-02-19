"""
@author: lileilei
@file: views.py
@time: 2017/7/13 16:42
"""
from app import  app
from  flask import  request,render_template,\
    make_response,send_from_directory,jsonify
from  app.models import *
import os
from flask.views import MethodView
from flask_login import login_required,current_user
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
class GeneraConfig(MethodView):
    '''通用配置添加编辑'''
    @login_required
    def post(self):
        data = request.get_json()
        config=GeneralConfiguration.query.filter_by(name=data['name']).first()
        if config:
            return jsonify({'code': 11, 'msg': '通用配置的名称必须唯一', 'data': ''})
        if data['type']=="key-value":
            newconfig=GeneralConfiguration(user=current_user,style=0,
                                           key=data["key"],name=data['name'])
            db.session.add(newconfig)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '成功'})
        elif data['type']=='token':
            newconfig=GeneralConfiguration(user=current_user,style=1,
                                           name=data['name'],token_method=data['method'],
                                           token_parame=data['parame'],token_url=data['url'])
            db.session.add(newconfig)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '成功'})
        elif data['type']=='sql':
            testevnet=Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not  testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            newconfig = GeneralConfiguration(user=current_user, style=1,
                                             name=data['name'], testevent=testevnet,
                                             sqlurl=data['sql'])
            db.session.add(newconfig)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '成功'})
        elif data['type']=='http请求':
            newconfig = GeneralConfiguration(user=current_user, style=1,
                                             name=data['name'],request_method=data['method'],
                                             request_parame=data['parame'],request_url=data['url'])
            db.session.add(newconfig)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '成功'})
        else:
            return jsonify({'code': 11, 'msg': '通用配置的类型暂时不支持', 'data': ''})
    @login_required
    def put(self):
        data = request.get_json()
        config_is=GeneralConfiguration.query.filter_by(id=int(data['id'])).first()
        if not  config_is:
            return jsonify({'code': 11, 'msg': '编辑的通用配置不存在，请确定', 'data': ''})
        if data['type']=="key-value":
            config_is.user=current_user
            config_is.style=0
            config_is.key=data["key"]
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：通用配置编辑成功'%config_is.name})
        elif data['type']=='token':
            config_is.user=current_user
            config_is.style=1,
            config_is.name=data['name']
            config_is.token_method=data['method'],
            config_is.token_parame=data['parame'],
            config_is.token_url=data['url']
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：通用配置编辑成功'%config_is.name})
        elif data['type']=='sql':
            testevnet=Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not  testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            config_is.user=current_user
            config_is.style=1
            config_is.name=data['name']
            config_is.testevent=testevnet
            config_is.sqlurl=data['sql']
            db.session.commit()
            return jsonify({'code': 200,'msg': '%s：通用配置编辑成功'%config_is.name})
        elif data['type']=='http请求':
            config_is.user=current_user
            config_is.style=1
            config_is.name=data['name']
            config_is.request_method=data['method']
            config_is.request_parame=data['parame']
            config_is.request_url=data['url']
            db.session.commit()
            return jsonify({'code': 200,'msg': '%s：通用配置编辑成功'%config_is.name})
        else:
            return jsonify({'code': 11, 'msg': '通用配置的类型暂时不支持', 'data': ''})
class ActionViews(MethodView):
    '''操作添加编辑'''
    @login_required
    def post(self):
        data = request.get_json()
        name_is=Action.query.filter_by(name=data['name']).first()
        if name_is:
            return jsonify({'code': 2, 'msg': '操作的名称必须唯一' })
        action = Action(name = data['name'],user = current_user)
        if data['catepy'] == '前置':
            action.category = 0
        else:
            action.category = 1
        if data['type']=="0":
            action.sleepnum=int(data['num'])
            action.style = 0
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '操作添加成功' })
        elif data['type']=="1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            action.testevent=testevnet
            action.style = 1
            action.sql=data['sql']
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '操作添加成功'})
        elif data['type']=="2":
            action.style=2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            case_is=InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not  case_is:
                return jsonify({'code': 11, 'msg': '选择的测试用例不存在'})
            action.testevent = testevnet
            action.caseid = int(data['caseid'])
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '操作添加成功'})
        elif data['type']=="3":
            action.style = 3
            action.requestsurl=data['url']
            action.requestmethod=data['method']
            action.requestsparame=data['parame']
            db.session.add(action)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '操作添加成功'})
        else:
            return jsonify({'code': 11, 'msg': '操作的类型不支持', 'data': ''})
    @login_required
    def put(self):
        data = request.get_json()
        id = Action.query.filter_by(id=data['id']).first()
        if not id:
            return jsonify({'code': 2, 'msg': '编辑操作不存在'})

        if data['type']=="0":
            id.sleepnum=int(data['num'])
            id.style = 0
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：操作成功'%id.name })
        elif data['type']=="1":
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            id.testevent=testevnet
            id.style = 1
            id.sql=data['sql']
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：操作成功' % id.name})
        elif data['type']=="2":
            id.style=2
            testevnet = Interfacehuan.query.filter_by(id=int(data['eventid'])).first()
            if not testevnet:
                return jsonify({'code': 11, 'msg': '选择的测试环境不存在'})
            case_is=InterfaceTest.query.filter_by(id=int(data['caseid'])).first()
            if not  case_is:
                return jsonify({'code': 11, 'msg': '选择的测试用例不存在'})
            id.testevent = testevnet
            id.caseid = case_is.id
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：操作成功' % id.name})
        elif data['type']=="3":
            id.style = 3
            id.requestsurl=data['url']
            id.requestmethod=data['method']
            id.requestsparame=data['parame']
            db.session.commit()
            return jsonify({'code': 200, 'msg': '%s：操作成功' % id.name})
        else:
            return jsonify({'code': 11, 'msg': '操作的类型不支持', 'data': ''})