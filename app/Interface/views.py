""" 
@author: lileilei
@file: views.py 
@time: 2018/1/31 13:31 
"""
from flask import redirect, request, \
    render_template, session, url_for, flash, Blueprint, \
    make_response, send_from_directory
from app.models import *
from common.parsingexcel import pasre_inter
from flask.views import MethodView, View
from flask_login import login_required, current_user
import json, os, time
from config import Config_import
from common.opearexcel import create_interface
from common.merge import mergeDict
from error_message import MessageEnum
from common.systemlog import logger
from common.jsontools import reponse

interfaceview = Blueprint('interface', __name__)


def get_project_model():
    projects = Project.query.filter_by(status=False).all()
    model = Model.query.filter_by(status=False).all()
    return projects, model


class EditInterfaceView(MethodView):
    @login_required
    def get(self, id):
        interface = Interface.query.filter_by(id=id, status=False).first()
        if interface is None:
            logger.info(__message=MessageEnum.edit_interface.value[1])
            flash(MessageEnum.edit_interface.value[1])
            return redirect(url_for('home.interface'))
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = []
            project_ids = []
            for i in current_user.quanxians:
                if (i.projects in id) is False:
                    if i.projects.status is False:
                        projects.append(i.projects)
                        project_ids.append(i.projects)
        project, models = get_project_model()
        return render_template('edit/edit_interface.html', interfac=interface,
                               projects=projects, models=models)

    @login_required
    def post(self, id):
        interface = Interface.query.filter_by(id=id, status=False).first()
        if interface is None:
            flash(MessageEnum.edit_interface.value[1])
            return redirect(url_for('home.interface'))
        project, models = get_project_model()
        if current_user.is_sper:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) == False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        projecct = request.form.get('project')
        model = request.form.get('model')
        intername = request.form.get('inter_name')
        url = request.form.get('url')
        interfa_tey = request.form.get('interface_type')
        headers = request.form.get('headers')
        meth = request.form.get('meth')
        if projecct is None or model is None or intername == '' or headers == '' or url == '' or meth == '':
            flash(MessageEnum.edit_interface_null_parame.value[1])
            return render_template('edit/edit_interface.html', interfac=interface, projects=projects, models=models)
        project_id = Project.query.filter_by(project_name=projecct).first().id
        models_id = Model.query.filter_by(model_name=model).first().id
        interface.projects_id = project_id
        interface.model_id = models_id
        interface.Interface_name = intername
        interface.Interface_headers = headers
        interface.Interface_url = url
        interface.Interface_meth = meth
        interface.Interface_user_id = current_user.id
        interface.interfacetype = interfa_tey
        try:
            flash(MessageEnum.Interface_edit.value[1])
            db.session.commit()
            return redirect(url_for('home.interface'))
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            flash(MessageEnum.Interface_edit_fail.value[1])
            return redirect(url_for('home.interface'))


class ImportInterfaceView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        if request.method == 'POST':
            file = request.files['myfile']
            if file and '.' in file.filename and file.filename.split('.')[1] == 'xlsx':
                filename = 'jiekou.xlsx'
                file.save(filename)
                jiekou_bianhao, project_nam, model_nam, interface_name, interface_url, interface_header, \
                interface_meth, interface_par, interface_bas, interface_type = pasre_inter(filename)
                if len(interface_meth) > Config_import:
                    flash(MessageEnum.import_max_big.value[1])
                    return redirect(url_for('interface.import_inter'))
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first()
                        if projects_id is None:
                            logger.info(MessageEnum.import_project_not_exitc.value[1])
                            flash(MessageEnum.import_project_not_exitc.value[1])
                            return redirect(url_for('interface.import_inter'))
                        model_id = Model.query.filter_by(model_name=model_nam[i]).first()
                        if model_id is None:
                            logger.info(MessageEnum.import_model.value[1])
                            flash(MessageEnum.import_model.value[1])
                            return redirect(url_for('interface.import_inter'))
                        new_interface = Interface(projects_id=projects_id.id, model_id=model_id.id,
                                                  Interface_name=str(interface_name[i]),
                                                  Interface_url=str(interface_url[i]),
                                                  Interface_headers=str(interface_header[i]),
                                                  Interface_meth=str(interface_meth[i]),
                                                  Interface_par=(interface_par[i]),
                                                  Interface_back=str(interface_bas[i]),
                                                  Interface_user_id=User.query.filter_by(
                                                      username=session.get('username')).first().id,
                                                  interfacetype=interface_type[i])
                        db.session.add(new_interface)
                        db.session.commit()
                    logger.info(MessageEnum.import_success.value[1])
                    flash(MessageEnum.import_success.value[1])
                    return redirect(url_for('home.interface'))
                except Exception as e:
                    logger.info(e)
                    flash(MessageEnum.import_fail.value[1])
                    return render_template('import.html')
            logger.info(MessageEnum.import_fail_admin.value[1])
            flash(MessageEnum.import_fail_admin.value[1])
            return render_template('import.html')
        return render_template('import.html')


class SerinterView(MethodView):
    @login_required
    def post(self):
        data = request.get_data('data')
        project = json.loads(data.decode('utf-8'))
        projec = project['project']
        interfatype = project['interfacetype']
        if interfatype == 'http':
            typeinterface = 'http'
        elif interfatype == 'dubbo':
            typeinterface = 'dubbo'
        else:
            typeinterface = 'none'
        if not project:
            return (
                {'msg': MessageEnum.project_not_exict.value[0],
                 'code': MessageEnum.project_not_exict.value[1],
                 'data': ''})
        project_is = Project.query.filter_by(project_name=str(projec)).first()
        if project_is.status is True:
            return reponse(
                message=MessageEnum.project_delet_free.value[1], code=MessageEnum.project_delet_free.value[0],
                data='')
        interfaclist = Interface.query.filter_by(projects_id=project_is.id, status=False,
                                                 interfacetype=interfatype).all()
        interfaclists = []
        for interface in interfaclist:
            interfaclists.append({'model_id': interface.models.model_name,
                                  'projects_id': interface.projects.project_name,
                                  'id': interface.id, 'Interface_url': interface.Interface_url,
                                  'Interface_meth': interface.Interface_meth,
                                  'Interface_headers': interface.Interface_headers,
                                  'Interface_name': interface.Interface_name})
        data = {}
        data['data'] = interfaclists
        data['typeinter'] = typeinterface
        return reponse(message=MessageEnum.success.value[1],
                       code=MessageEnum.success.value[0],
                       data=data)


class ExportinterfaceInterfceView(MethodView):
    @login_required
    def post(self):
        project = request.form.get('interface_type')
        project_case = Project.query.filter_by(project_name=str(project), status=False).first()
        if project_case is None:
            logger.info(MessageEnum.project_not_exict.value[1])
            flash(MessageEnum.project_not_exict.value[1])
            return redirect(url_for('home.interface'))
        interface_list = Interface.query.filter_by(projects_id=project_case.id, status=False).all()
        pad = os.getcwd()
        day = time.strftime("%Y%m", time.localtime(time.time()))
        file_dir = pad + '/app/upload'
        file = os.path.join(file_dir, (day + '.xls'))
        if os.path.exists(file) is False:
            os.system('touch %s' % file)
        result = create_interface(filename=file, interfacelist=interface_list)
        if result['code'] == 1:
            flash(MessageEnum.export_fail.value[1] + '原因：%s' % result['error'])
            return redirect(url_for('home.interface'))
        response = make_response(send_from_directory(file_dir, filename=day + '.xls', as_attachment=True))
        return response


class DetailView(MethodView):
    @login_required
    def get(self, id):
        interface_one = Interface.query.filter_by(id=id, status=False).first()
        if not interface_one:
            flash(MessageEnum.interface_not_exist.value[1])
            return redirect(url_for('home.interface'))
        parme = Parameter.query.filter_by(interface_id=interface_one.id, status=False).all()
        rucan = []
        sendparame_deft = {}
        parame_deft = {}
        chucan = []
        for i in range(len(parme)):
            try:
                if parme[i].type == 1:
                    chucan.append(parme[i])
                    parame_deft.update(json.loads(parme[i].default))
                else:
                    print(parme[i].default)
                    rucan.append(parme[i])
                    sendparame_deft.update(str(parme[i].default))
            except:
                pass
        return render_template('home/interface_detail.html', id_one=interface_one, chucanlist=chucan,
                               rucanlist=rucan, chucan_def=mergeDict(parame_deft),
                               rucan_def=mergeDict(sendparame_deft))


class AddParameterView(MethodView):
    @login_required
    def get(self, id):
        self.interface = Interface.query.filter_by(id=str(id), status=False).first()
        if self.interface is None:
            flash(MessageEnum.add_parame_interface.value[1])
            return redirect(url_for('home.interface'))
        return render_template('add/addparmes.html', interface=self.interface)

    @login_required
    def post(self, id):
        self.interface = Interface.query.filter_by(id=str(id), status=False).first()
        name = request.form.get('name')
        type = request.form.get('type')
        nuss = request.form.get('nussu')
        typec = request.form.get('typechu')
        desec = request.form.get('desec')
        demo = request.form.get('shili')
        if name is None or name == '':
            flash(MessageEnum.parame_name_not_empty.value[1])
            return render_template('add/addparmes.html', interface=self.interface)
        if type is None or type == '':
            flash(MessageEnum.parame_error.value[1])
            return render_template('add/addparmes.html', interface=self.interface)
        old_name = Parameter.query.filter_by(interface_id=self.interface.id, status=False, parameter_name=name).first()
        if old_name:
            flash(MessageEnum.parame_is_exict.value[1])
            return render_template('add/addparmes.html', interface=self.interface)
        if nuss == '是':
            if_nuss = True
        else:
            if_nuss = False
        if typec == '出参':
            is_return = 1
        else:
            is_return = 0
        new = Parameter(interface_id=self.interface.id,
                        parameter_name=name, parameter_type=type,
                        necessary=if_nuss, type=is_return,
                        default=demo, desc=desec,
                        user_id=current_user.id)
        db.session.add(new)
        try:
            db.session.commit()
            return redirect(url_for('interface.interface_detail', id=self.interface.id))
        except Exception as  e:
            db.session.rollback()
            flash('添加失败！原因：%s' % e)
            return render_template('add/addparmes.html',
                                   interface=self.interface)


class DeleteParameterView(MethodView):
    @login_required
    def get(self, id):
        passem = Parameter.query.filter_by(id=id, status=False).first()
        if not passem:
            flash(MessageEnum.parame_is_not_exict.value[1])
            return redirect(url_for('interface.interface_detail',
                                    id=passem.interfaces.id))
        passem.status = True
        try:
            db.session.commit()
            flash(MessageEnum.success.value[1])
            return redirect(url_for('interface.interface_detail',
                                    id=passem.interfaces.id))
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.delete_fail.value[1])
            return redirect(url_for('interface.interface_detail',
                                    id=passem.interfaces.id))


class EditPParameterView(MethodView):
    @login_required
    def get(self, id, inte_id):
        pasrm = Parameter.query.filter_by(id=id).first()
        interface_one = Interface.query.filter_by(id=inte_id,
                                                  status=False).first()
        if interface_one is None:
            flash(MessageEnum.interface_not_exist.value[1])
            return redirect(url_for('home.interface'))
        if pasrm is None:
            flash(MessageEnum.parame_is_not_exict.value[1])
            return redirect(url_for('interface.interface_detail', id=inte_id))
        return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)

    @login_required
    def post(self, id, inte_id):
        pasrm = Parameter.query.filter_by(id=int(id)).first()
        interface_one = Interface.query.filter_by(id=inte_id, status=False).first()
        if interface_one is None:
            flash(MessageEnum.interface_not_exist.value[1])
            return redirect(url_for('home.interface'))
        if pasrm is None:
            flash(MessageEnum.parame_is_not_exict.value[1])
            return redirect(url_for('interface.interface_detail', id=inte_id))
        type = request.form.get('type')
        nuss = request.form.get('nussu')
        typec = request.form.get('typechu')
        desec = request.form.get('desec')
        shili = request.form.get('shili')
        name = request.form.get('name')
        if name is None or name == '':
            flash(MessageEnum.parame_name_not_empty.value[1])
            return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)
        if nuss == '是':
            if_nuss = True
        else:
            if_nuss = False
        if typec == '出参':
            is_chu = 1
        else:
            is_chu = 0
        if type is None or type == '':
            flash(MessageEnum.parame_type_is_not_empty.value[1])
            return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)
        pasrm.type = is_chu
        pasrm.necessary = if_nuss
        pasrm.desc = desec
        pasrm.default = shili
        try:
            flash(MessageEnum.success.value[1])
            db.session.commit()
            return redirect(url_for('interface.interface_detail', id=inte_id))
        except Exception as e:
            logger.exception(e)
            flash(MessageEnum.edit_fail.value[1])
            return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)


class AddGroupInterface(MethodView):
    # 黑名单添加接口
    @login_required
    def get(self, interfaceid):
        interface_one = Interface.query.filter_by(id=interfaceid, status=False).first()
        if not interface_one:
            return reponse(message=MessageEnum.interface_not_exist.value[1],
                           code=MessageEnum.interface_not_exist.value[0])

        return reponse(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])


class GetGroupInterface(MethodView):
    '''获取黑名单接口'''

    @login_required
    def get(self, interfaceid):
        interface_one = Interface.query.filter_by(id=interfaceid, status=False).first()
        if not interface_one:
            return reponse(message=MessageEnum.interface_not_exist.value[1],
                           code=MessageEnum.interface_not_exist.value[0])

        return reponse(message=MessageEnum.success.value[1],
                       code=MessageEnum.success.value[0])
