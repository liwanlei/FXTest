""" 
@author: lileilei
@file: views.py 
@time: 2018/1/31 13:31 
"""
from  flask import  redirect,request,render_template,session,url_for,flash,Blueprint,jsonify
from  app.models import *
from app.form import  *
from common.pares_excel_inter import pasre_inter
from flask.views import MethodView,View
from flask_login import login_required,current_user
import json
interfac = Blueprint('interface', __name__)
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.filter_by(status=False).all()
    return  projects,model
class InterfaceaddView(MethodView):
    @login_required
    def get(self):
        form=InterForm()
        models=Model.query.filter_by(status=False).first()
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        return render_template('add/add_interface.html', form=form, projects=projects, models=models)
    @login_required
    def post(self):
        data=request.get_json()
        project_id=Project.query.filter_by(project_name=data['project']).first().id
        models_id=Model.query.filter_by(model_name=data['model']).first().id
        try:
            new_interface=Interface(model_id=models_id,projects_id=project_id,Interface_name=data['interfacename'],Interface_url=data['interface_url'],
                                    Interface_meth=data['interface_meth'],Interface_par=data['interface_par'],Interface_back=data['interface_bas'],
                                    Interface_user_id=current_user.id,Interface_headers=data['interface_headers'],interfacetype=data['interface_type'])
            db.session.add(new_interface)
            db.session.commit()
            return jsonify({'msg': '成功', 'code': 200})
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': '添加接口失败，原因:%s'%e, 'code': 236})
class EditInterfaceView(MethodView):
    @login_required
    def get(self,id):
        interface=Interface.query.filter_by(id=id).first()
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        project, models = get_pro_mo()

        return render_template('edit/edit_inter.html', interfac=interface, projects=projects, models=models)
    @login_required
    def post(self,id):
        interface=Interface.query.filter_by(id=id).first()
        project, models = get_pro_mo()
        if current_user.is_sper == True:
            projects=Project.query.filter_by(status=False).order_by('-id').all()
        else:
            projects=[]
            id=[]
            for i in current_user.quanxians:
                if  (i.projects in id)==False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        projecct=request.form.get('project')
        model=request.form.get('model')
        intername=request.form.get('inter_name')
        url=request.form.get('url')
        interfa_tey=request.form.get('interface_type')
        headers=request.form.get('headers')
        meth=request.form.get('meth')
        reques=request.form.get('reque')
        back=request.form.get('back')
        if projecct is None or model is None or intername=='' or headers =='' or url=='' or meth=='' or back=='':
            flash(u'请确定各项参数都正常填写')
            return render_template('edit/edit_inter.html', interfac=interface, projects=projects, models=models)
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
        interface.Interface_user_id=current_user.id
        interface.interfacetype=interfa_tey
        try:
            flash('编辑成功')
            db.session.commit()
            return redirect(url_for('home.interface'))
        except:
            db.session.rollback()
            flash(u'编辑失败')
            return redirect(url_for('home.interface'))
class DeleinterView(MethodView):
    @login_required
    def get(self,id):
        interface=Interface.query.filter_by(id=id).first()
        if not  interface:
            flash(u'删除失败，没有获到你要删除的接口，请重新选择要删除的接口重试')
            return redirect(url_for('home.interface'))
        interface.status=True
        try:
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('home.interface'))
        except Exception as e:
            db.session.rollback()
            flash(u'删除失败！原因：%s'%e)
            return redirect(url_for('home.interface'))
class DaoruinterView(View):
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
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
class SerinterView(MethodView):
    @login_required
    def post(self):
        data = request.get_data('data')
        project = json.loads(data.decode('utf-8'))
        projec=project['project']
        interfatype=project['interfacetype']
        if interfatype=='http':
            typeinterface='http'
        elif interfatype=='dubbo':
            typeinterface='dubbo'
        else:
            typeinterface='none'
        if not project:
            return jsonify({'msg': '没有发送数据', 'code': 108})
        project_is = Project.query.filter_by(project_name=str(projec)).first()
        if project_is.status is True:
            return jsonify({'msg': '项目已经删除', 'code': 220})
        interfaclist = Interface.query.filter_by(projects_id=project_is.id, status=False,interfacetype=interfatype).all()
        interfaclists=[]
        for interface in interfaclist:
            interfaclists.append({'model_id':interface.models.model_name,'projects_id':interface.projects.project_name,
                                  'id':interface.id,'Interface_url':interface.Interface_url,'Interface_meth':interface.Interface_meth,
                                  'Interface_headers':interface.Interface_headers,'Interface_par':interface.Interface_par,'Interface_back':interface.Interface_back,
                                  'Interface_name':interface.Interface_name})
        return  jsonify(({'msg': '成功', 'code':200,'data':interfaclists,'typeinter':typeinterface}))