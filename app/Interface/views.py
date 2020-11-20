""" 
@author: lileilei
@file: views.py 
@time: 2018/1/31 13:31 
"""
from flask import redirect, request, \
    render_template, session, url_for, flash, Blueprint, \
    jsonify, make_response, send_from_directory
from app.models import *
from common.parsingexcel import pasre_inter
from flask.views import MethodView, View
from flask_login import login_required, current_user
import json, os, time
from config import Config_daoru_xianzhi
from common.opearexcel import create_interface
from common.merge import hebingDict

interfac = Blueprint('interface', __name__)


def get_pro_mo():
    projects = Project.query.filter_by(status=False).all()
    model = Model.query.filter_by(status=False).all()
    return projects, model


class EditInterfaceView(MethodView):
    @login_required
    def get(self, id):
        interface = Interface.query.filter_by(id=id, status=False).first()
        if interface is None:
            flash(u'要编辑的测试用例不存在')
            return redirect(url_for('home.interface'))
        if current_user.is_sper == True:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) == False:
                    if i.projects.status == False:
                        projects.append(i.projects)
                        id.append(i.projects)
        project, models = get_pro_mo()
        return render_template('edit/edit_inter.html', interfac=interface, projects=projects, models=models)

    @login_required
    def post(self, id):
        interface = Interface.query.filter_by(id=id, status=False).first()
        if interface is None:
            flash(u'要编辑的测试用例不存在')
            return redirect(url_for('home.interface'))
        project, models = get_pro_mo()
        if current_user.is_sper == True:
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
            flash(u'请确定各项参数都正常填写')
            return render_template('edit/edit_inter.html', interfac=interface, projects=projects, models=models)
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
            flash(u'编辑成功')
            db.session.commit()
            return redirect(url_for('home.interface'))
        except:
            db.session.rollback()
            flash(u'编辑失败')
            return redirect(url_for('home.interface'))


class DaoruinterView(View):
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
                if len(interface_meth) > Config_daoru_xianzhi:
                    flash(u'系统目前支持的导入有限制，请分开导入')
                    return redirect(url_for('interface.daoru_inter'))
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=project_nam[i]).first()
                        if projects_id is None:
                            flash(u'找不到项目，请确定导入的项目是否存在')
                            return redirect(url_for('interface.daoru_inter'))
                        model_id = Model.query.filter_by(model_name=model_nam[i]).first()
                        if model_id is None:
                            flash(u'找不到模块不存在！，请确定导入的项目是否存在')
                            return redirect(url_for('interface.daoru_inter'))
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
                    flash(u'导入成功')
                    return redirect(url_for('home.interface'))
                except Exception as e:
                    flash(u'导入失败，请检查')
                    return render_template('daoru.html')
            flash(u'导入失败')
            return render_template('daoru.html')
        return render_template('daoru.html')


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
            return jsonify({'msg': u'没有发送数据', 'code': 31, 'data': ''})
        project_is = Project.query.filter_by(project_name=str(projec)).first()
        if project_is.status is True:
            return jsonify({'msg': u'项目已经删除', 'code': 32, 'data': ''})
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
        return jsonify(({'msg': u'成功', 'code': 200, 'data': interfaclists, 'typeinter': typeinterface}))


class DaochuInterfa(MethodView):
    @login_required
    def post(self):
        project = request.form.get('interface_type')
        project_case = Project.query.filter_by(project_name=str(project), status=False).first()
        if project_case is None:
            flash(u'你选择导出接口的项目不存在')
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
            flash(u'导出失败！原因：%s' % result['error'])
            return redirect(url_for('home.interface'))
        response = make_response(send_from_directory(file_dir, filename=day + '.xls', as_attachment=True))
        return response


class XiangqingView(MethodView):
    @login_required
    def get(self, id):
        interface_one = Interface.query.filter_by(id=id, status=False).first()
        if not interface_one:
            flash('要查看的接口不存在')
            return redirect(url_for('home.interface'))
        parme = Parameter.query.filter_by(interface_id=interface_one.id, status=False).all()
        rucan = []
        rucan_deft = []
        chucan_deft = []
        chucan = []
        for i in range(len(parme)):
            if parme[i].type == 1:
                chucan.append(parme[i])
                chucan_deft.append(str(parme[i].default))
            else:
                rucan.append(parme[i])
                rucan_deft.append(str(parme[i].default))
        return render_template('home/interface_one.html', id_one=interface_one, chucanlist=chucan,
                               rucanlist=rucan, chucan_def=hebingDict(chucan_deft),
                               rucan_def=hebingDict(rucan_deft))


class ADdparmsView(MethodView):
    @login_required
    def get(self, id):
        self.interface = Interface.query.filter_by(id=str(id), status=False).first()
        if self.interface is None:
            flash('添加参数的接口不存在')
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
        shili = request.form.get('shili')
        if name is None or name == '':
            flash('参数的名字不能为空')
            return render_template('add/addparmes.html', interface=self.interface)
        if type is None or type == '':
            flash('参数格式类型必须填写进去')
            return render_template('add/addparmes.html', interface=self.interface)
        old_name = Parameter.query.filter_by(interface_id=self.interface.id, status=False, parameter_name=name).first()
        if old_name:
            flash('参数名称已经存在于该接口')
            return render_template('add/addparmes.html', interface=self.interface)
        if nuss == '是':
            if_nuss = True
        else:
            if_nuss = False
        if typec == '出参':
            is_chu = 1
        else:
            is_chu = 0
        new = Parameter(interface_id=self.interface.id, parameter_name=name, parameter_type=type,
                        necessary=if_nuss, type=is_chu, default=shili, desc=desec, user_id=current_user.id)
        db.session.add(new)
        try:
            db.session.commit()
            return redirect(url_for('interface.interface_one', id=self.interface.id))
        except Exception as  e:
            db.session.rollback()
            flash('添加失败！原因：%s' % e)
            return render_template('add/addparmes.html', interface=self.interface)


class DeleteParmsView(MethodView):
    @login_required
    def get(self, id):
        passem = Parameter.query.filter_by(id=id, status=False).first()
        if not passem:
            flash('不存在的参数')
            return redirect(url_for('interface.interface_one', id=passem.interfaces.id))
        passem.status = True
        try:
            db.session.commit()
            flash('删除参数成功')
            return redirect(url_for('interface.interface_one', id=passem.interfaces.id))
        except Exception as e:
            db.session.rollback()
            flash('删除失败！原因：%s' % e)
            return redirect(url_for('interface.interface_one', id=passem.interfaces.id))


class EditParmsView(MethodView):
    @login_required
    def get(self, id, inte_id):
        pasrm = Parameter.query.filter_by(id=id).first()
        interface_one = Interface.query.filter_by(id=inte_id, status=False).first()
        if interface_one is None:
            flash('要查看的接口不存在')
            return redirect(url_for('home.interface'))
        if pasrm is None:
            flash('参数无法编辑，请确定是否存在')
            return redirect(url_for('interface.interface_one', id=inte_id))
        return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)

    @login_required
    def post(self, id, inte_id):
        pasrm = Parameter.query.filter_by(id=int(id)).first()
        interface_one = Interface.query.filter_by(id=inte_id, status=False).first()
        if interface_one is None:
            flash('要查看的参数的接口不存在')
            return redirect(url_for('home.interface'))
        if pasrm is None:
            flash('参数无法编辑，请确定是否存在')
            return redirect(url_for('interface.interface_one', id=inte_id))
        type = request.form.get('type')
        nuss = request.form.get('nussu')
        typec = request.form.get('typechu')
        desec = request.form.get('desec')
        shili = request.form.get('shili')
        name = request.form.get('name')
        if name is None or name == '':
            flash('参数的名字不能为空')
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
            flash('参数格式类型必须填写进去')
            return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)
        pasrm.type = is_chu
        pasrm.necessary = if_nuss
        pasrm.desc = desec
        pasrm.default = shili
        try:
            flash('编辑参数成功')
            db.session.commit()
            return redirect(url_for('interface.interface_one', id=inte_id))
        except Exception as e:
            flash('编辑出错，原因：%s' % e)
            return render_template('edit/edtiparmes.html', pasrm=pasrm, interface_one=interface_one)


class AddGroupInterface(MethodView):
    # 黑名单添加接口
    @login_required
    def get(self, interfaceid):
        interface_one = Interface.query.filter_by(id=interfaceid, status=False).first()
        if not interface_one:
            return jsonify({"data": '接口不存在', 'code': 2})

        return jsonify({"data": '添加成功', 'code': 0})


class GetGroupInterface(MethodView):
    '''获取黑名单接口'''

    @login_required
    def get(self, interfaceid):
        interface_one = Interface.query.filter_by(id=interfaceid, status=False).first()
        if not interface_one:
            return jsonify({"data": '接口不存在', 'code': 2})

        return jsonify({"data": '获取成功', 'code': 0})
