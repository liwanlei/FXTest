""" 
@author: lileilei
@file: views.py 
@time: 2018/1/31 13:31 
"""
from  flask import  redirect,request,render_template,session,url_for,flash,Blueprint
from  app.models import *
from app.form import  *
from app.common.pares_excel_inter import pasre_inter
from flask.views import MethodView,View
from flask_login import login_required,current_user
interfac = Blueprint('interface', __name__)
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
class InterfaceaddView(MethodView):
    @login_required
    def get(self):
        form=InterForm()
        project,models=get_pro_mo()
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
        form=InterForm()
        project,models=get_pro_mo()
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
                return render_template('add/add_interface.html', form=form, projects=projects, models=models)
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
                return redirect(url_for('home.interface'))
        return render_template('add/add_interface.html', form=form, projects=projects, models=models)
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
        if request.method=='POST':
            projecct=request.form.get('project')
            model=request.form.get('model')
            intername=request.form.get('inter_name')
            url=request.form.get('url')
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
            try:
                flash('编辑成功')
                db.session.commit()
                return redirect(url_for('home.interface'))
            except:
                db.session.rollback()
                flash(u'编辑失败')
                return redirect(url_for('home.interface'))
        return render_template('edit/edit_inter.html', interfac=interface, projects=projects, models=models)
class DeleinterView(MethodView):
    @login_required
    def get(self,id):
        interface=Interface.query.filter_by(id=id).first()
        interface.status=True
        db.session.commit()
        flash(u'删除成功')
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