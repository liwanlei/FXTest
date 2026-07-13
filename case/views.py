"""
@author: lileilei
@file: views.py
@time: 2018/1/31 13:20
"""
from flask import redirect, request, render_template, \
    session, url_for, flash, Blueprint
from app.models import *
from app.forms import *
import os, time, datetime, json
from common.json_tools import response as jsonreponse
from common.system_log import logger
from error_message import MessageEnum
from flask.views import View, MethodView
from flask_login import current_user, login_required
from ast import literal_eval
from app.helpers import get_user_projects, get_project_model

case = Blueprint('case', __name__)


class AddtestcaseView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        form = InterfaceCaseForm()
        project, models = get_project_model()
        interface_list = Interface.query.filter_by(status=False).all()
        mock_yilai = Mockserver.query.filter_by(delete=False).all()
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = get_user_projects()
        if request.method == 'POST' and form.validate_on_submit:
            ci = request.form.get("ci")
            if ci == "是":
                is_ci = True
            else:
                is_ci = False
            save = request.form.get('save')
            yongli_nam = request.form.get('project')
            mode = request.form.get('mode')
            interface_name = request.form.get('interface_name')
            interface_url = request.form.get('interface_url')
            interface_header = request.form.get('interface_headers')
            interface_meth = request.form.get('interface_meth')
            interface_can = request.form.get('interface_can')
            interface_re = request.form.get('interface_rest')
            yilai_data = request.values.get("yilaicanshu")
            yilai_test = request.values.get("jiekou")
            shifoujiaoyan = request.values.get("database")
            interface_type = request.values.get('interface_type')
            if shifoujiaoyan == 'on':
                databasesql = request.values.get('databasesql')
                databijiao = request.values.get('databijiao')
                is_database = True
            else:
                databasesql = None
                databijiao = None
                is_database = False
            if yilai_test is None or yilai_test == '请选择依赖接口':
                yilai_dat = None
                yilai_tes = None
            else:
                yilai_tes = yilai_test
                if yilai_data is None or yilai_data == '':
                    flash(MessageEnum.reply_must_be_reply_field.value[1])
                    return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                                           interface_list=interface_list, mock_yilai=mock_yilai)
                yilai_dat = yilai_data
            if yongli_nam == '' or mode == '' or interface_header == '' or interface_url == '' or interface_meth == '':
                flash(MessageEnum.must_be_every_parame.value[1])
                return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                                       interface_list=interface_list, mock_yilai=mock_yilai)
            project_id = Project.query.filter_by(project_name=yongli_nam).first().id
            models_id = Model.query.filter_by(model_name=mode).first().id
            interface = Interface.query.filter_by(Interface_name=interface_name).first()
            if save == 1 or save == '1':
                saves = False
            elif save == 2 or save == '2':
                saves = True
            else:
                flash(MessageEnum.save_test_result_error.value[1])
                return render_template('add/add_test_case.html', form=form, projects=projects, mock_yilai=mock_yilai,
                                       models=models, interface_list=interface_list)

            try:
                newcase = InterfaceTest(projects_id=project_id, model_id=models_id, interface_id=interface.id,
                                        Interface_headers=interface_header, bian_num=interface_url,
                                        Interface_meth=interface_meth, Interface_pase=interface_can,
                                        Interface_assert=interface_re, Interface_user_id=current_user.id,
                                        saveresult=saves, pid=(yilai_tes), getattr_p=yilai_dat,
                                        is_database=is_database, chaxunshujuku=databasesql,
                                        databaseziduan=databijiao,
                                        Interface_name=interface_name, Interface_url=interface.Interface_url,
                                        interface_type=interface_type, is_ci=is_ci)
                db.session.add(newcase)
                db.session.commit()
                try:
                    for key, value in dict(literal_eval(interface_can)):
                        if str(value).startswith("#"):
                            if str(value).split(".")[0] == '#action':
                                action = Action.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.action_not_exit.value[1])
                                    return render_template('add/add_test_case.html', form=form, projects=projects,
                                                           models=models,
                                                           interface_list=interface_list, mock_yilai=mock_yilai)
                                caseac = CaseAction(case=newcase, action=action, actiontype=action.category,
                                                    filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            elif str(value).split(".")[0] == '#conf':
                                action = GeneralConfiguration.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.config_not_exict.value[1])
                                    return render_template('add/add_test_case.html', form=form, projects=projects,
                                                           models=models,
                                                           interface_list=interface_list, mock_yilai=mock_yilai)
                                caseac = CaseGeneral(case=newcase,
                                                     general=action, filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            else:
                                pass
                except Exception:
                    flash(MessageEnum.test_field_should_be_dict.value[1])
                    return render_template('add/add_test_case.html',
                                           form=form, projects=projects,
                                           models=models,
                                           interface_list=interface_list,
                                           mock_yilai=mock_yilai)
                flash(MessageEnum.success.value[1])
                return redirect(url_for('home.case'))
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                flash(MessageEnum.add_case_error.value[1])
                return redirect(url_for('home.case'))
        return render_template('add/add_test_case.html',
                               form=form,
                               projects=projects,
                               models=models,
                               interface_list=interface_list,
                               mock_yilai=mock_yilai)


class EditcaseView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self, id):
        project, models = get_project_model()
        interface_list = Interface.query.filter_by(status=False).all()
        mock_yilai = Mockserver.query.filter_by(delete=False).all()
        if current_user.is_sper:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = get_user_projects()
        edit_case = InterfaceTest.query.filter_by(id=id, status=False).first()
        if not edit_case:
            flash(MessageEnum.case_not_exist.value[1])
            return redirect(url_for('home.case'))
        if request.method == 'POST':
            save = request.form.get('save')
            yongli_nam = request.form.get('project')
            mode = request.form.get('model')
            url = request.form.get('url')
            meth = request.form.get('meth')
            headers = request.form.get('headers')
            parme = request.form.get('parme')
            reque = request.form.get('reque')
            ci = request.form.get("ci")
            yilai_data = request.values.get("yilaicanshu")
            yilai_test = request.values.get("jiekou")
            inerfa = request.form.get('inerfa')
            shifoujiaoyan = request.values.get("database")
            interface_type = request.values.get('interface_type')
            if ci == "是":
                is_ci = True
            else:
                is_ci = False
            if shifoujiaoyan == 'on':
                databasesql = request.values.get('databasesql')
                databijiao = request.values.get('databijiao')
                is_database = True
            else:
                databasesql = None
                databijiao = None
                is_database = False
            if yilai_test is None or yilai_test == '请选择依赖接口' or yilai_test == '':
                yilai_dat = None
                yilai_tes = None
            else:
                yilai_tes = yilai_test
                if yilai_data is None or yilai_data == '':
                    flash(MessageEnum.reply_must_be_reply_field.value[1])
                    return render_template('edit/edit_case.html', edit=edit_case,
                                           projects=projects, models=models,
                                           inerfacelist=interface_list, mock_yilai=mock_yilai)
                yilai_dat = yilai_data
            if yongli_nam == None or mode == None or url == '' or headers == '' or meth == '' or reque == '':
                flash(MessageEnum.edit_interface_null_parame.value[1])
                return render_template('edit/edit_case.html', edit=edit_case, projects=projects,
                                       models=models,
                                       inerfacelist=interface_list, mock_yilai=mock_yilai)
            projects_id = Project.query.filter_by(id=(yongli_nam)).first().id
            model_id = Model.query.filter_by(model_name=mode).first().id
            interface = Interface.query.filter_by(Interface_name=inerfa).first().id
            if save is None:
                saves = False
            elif save == '是':
                saves = True
            else:
                flash(MessageEnum.save_test_result_error.value[1])
                return render_template('edit/edit_case.html',
                                       edit=edit_case, projects=projects, models=models,
                                       inerfacelist=interface_list, mock_yilai=mock_yilai)
            edit_case.projects_id = projects_id
            edit_case.model_id = model_id
            edit_case.interface_id = interface
            edit_case.bianhao = url
            edit_case.Interface_headers = headers
            edit_case.Interface_meth = meth
            edit_case.Interface_pase = parme
            edit_case.Interface_assert = reque
            edit_case.Interface_user_id = current_user.id
            edit_case.saveresult = saves
            edit_case.pid = yilai_tes
            edit_case.getattr_p = yilai_dat
            edit_case.is_database = is_database
            edit_case.chaxunshujuku = databasesql
            edit_case.databaseziduan = databijiao
            edit_case.interface_type = interface_type
            edit_case.is_ci = is_ci
            db.session.commit()
            try:
                actioncase = CaseAction.query.filter_by(case=edit_case.id).all()
                configcase = CaseGeneral.query.filter_by(case=edit_case.id).all()
                for i in actioncase:
                    db.session.delete(i)
                for m in configcase:
                    db.session.delete(m)
                db.session.commit()
                try:
                    for key, value in dict(literal_eval(parme)):
                        if str(value).startswith("#"):
                            if str(value).split(".")[0] == '#action':
                                action = Action.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.action_not_exit.value[1])
                                    return render_template('edit/edit_case.html', edit=edit_case,
                                                           projects=projects, models=models,
                                                           inerfacelist=interface_list, mock_yilai=mock_yilai)
                                caseac = CaseAction(case=edit_case, action=action, actiontype=action.category,
                                                    filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            elif str(value).split(".")[0] == '#conf':
                                action = GeneralConfiguration.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.config_not_exict.value[1])
                                    return render_template('edit/edit_case.html', edit=edit_case,
                                                           projects=projects, models=models,
                                                           inerfacelist=interface_list, mock_yilai=mock_yilai)
                                caseac = CaseGeneral(case=edit_case, general=action, filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            else:
                                pass
                except Exception:
                    flash(MessageEnum.test_field_should_be_dict.value[1])
                    return render_template('edit/edit_case.html', edit=edit_case,
                                           projects=projects, models=models,
                                           inerfacelist=interface_list, mock_yilai=mock_yilai)

                db.session.commit()
                flash(MessageEnum.success.value[1])
                return redirect(url_for('home.case'))
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                flash(MessageEnum.case_edit_error.value[1])
                return render_template('edit/edit_case.html',
                                       edit=edit_case, projects=projects, models=models,
                                       inerfacelist=interface_list, mock_yilai=mock_yilai)
        return render_template('edit/edit_case.html', edit=edit_case, projects=projects,
                               models=models, inerfacelist=interface_list, mock_yilai=mock_yilai)


class SerCaseView(MethodView):
    @login_required
    def post(self):
        id = request.get_data('id')
        project = json.loads(id.decode('utf-8'))
        if not project:
            return jsonreponse(message=MessageEnum.error_send_message.value[1],
                               code=MessageEnum.error_send_message.value[0])
        project_name = str(project['project'])
        project_is = Project.query.filter_by(project_name=project_name, status=False).first()
        if not project_is:
            return jsonreponse(message=MessageEnum.error_send_message.value[1],
                               code=MessageEnum.error_send_message.value[0])
        testevent = Interfacehuan.query.filter_by(projects=project_is, status=False).all()
        interfatype = project['interface_type']
        if interfatype == 'http':
            typeinterface = 'http'
        elif interfatype == 'dubbo':
            typeinterface = 'dubbo'
        else:
            typeinterface = 'none'
        if project_is.status is True:
            return jsonreponse(message=MessageEnum.project_delet_free.value[1],
                               code=MessageEnum.project_delet_free.value[0])
        intertestcases = InterfaceTest.query.filter_by(projects_id=project_is.id, status=False,
                                                       interface_type=str(interfatype)).order_by(
            InterfaceTest.id.desc()).all()
        interfacelist = []
        testeventlist = []
        for testeven in testevent:
            testeventlist.append({'url': testeven.url, 'id': testeven.id})
        for interface in intertestcases:
            interfacelist.append({'id': interface.id, 'model': interface.models.model_name,
                                  "project": interface.projects.project_name,
                                  'bianhao': interface.bian_num,
                                  'interface': interface.interfaces.Interface_name,
                                  'Interface_name': interface.Interface_name,
                                  'Interface_headers': interface.Interface_headers,
                                  'Interface_url': interface.Interface_url,
                                  'Interface_meth': interface.Interface_meth,
                                  'Interface_pase': interface.Interface_pase,
                                  'Interface_assert': interface.Interface_assert,
                                  'Interface_is_tiaoshi': interface.Interface_is_tiaoshi,
                                  'Interface_tiaoshi_shifou': interface.Interface_tiaoshi_shifou})

        data = {}
        data['data'] = interfacelist
        data['url'] = testeventlist
        data['typeinter'] = typeinterface
        return jsonreponse(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0],
                           data=data)


class OneCaseDetialView(MethodView):
    @login_required
    def post(self):
        case_id = request.get_data().decode('utf-8')
        case_one = InterfaceTest.query.filter_by(id=int(case_id)).first()
        if not case_one:
            return jsonreponse(code=MessageEnum.not_find_your_case.value[0],
                               message=MessageEnum.not_find_your_case.value[1])
        test_result = TestcaseResult.query.filter_by(case_id=case_one.id).all()
        if not test_result or len(test_result) <= 0:
            return jsonreponse(code=MessageEnum.you_case_not_try.value[0],
                               message=MessageEnum.you_case_not_try.value[1])
        result_all = []
        for rest_one in test_result:
            if rest_one.spend == None:
                spend_ed = 0
            else:
                spend_ed = rest_one.spend
            if rest_one.ceshihuanjing is None:
                ceshihuanjing = ''
            else:
                ceshihuanjing = rest_one.ceshihuanjing
            result_all.append({'result': rest_one.result,
                               'date': rest_one.date.strftime('%Y-%m-%d %H:%M:%S'),
                               'event': ceshihuanjing,
                               'spend': spend_ed})
        return jsonreponse(code=MessageEnum.success.value[0],
                           message=MessageEnum.success.value[1], data=result_all)


class GetProjectInterfaceCase(MethodView):
    def post(self, project: str = None, interface: str = None):
        if project and interface:
            projectis = Project.query.filter_by(project_name=project).first()
            if projectis is None:
                return jsonreponse(code=MessageEnum.requests_case_project_not_exit.value[0],
                                   message=MessageEnum.requests_case_project_not_exit.value[1],
                                   data=[])
            interfaceis = Interface.query.filter_by(Interface_url=interface,
                                                    projects_id=projectis.id).first()
            if interfaceis is None:
                return jsonreponse(code=MessageEnum.requests_case_interface_not_exit.value[0],
                                   message=MessageEnum.requests_case_interface_not_exit.value[1],
                                   data=[])

            interfacetestcaselist = InterfaceTest.query.filter_by(projects_id=projectis.id,
                                                                  interface_id=interfaceis.id).all()
            if len(interfacetestcaselist) > 0:
                reslutcaselit = []
                for item in interfacetestcaselist:
                    caseitem = {}
                    caseitem['id'] = item.id
                    caseitem['name'] = item.bian_num
                    reslutcaselit.append(caseitem)
                return jsonreponse(code=MessageEnum.success.value[0],
                                   message=MessageEnum.success.value[1],
                                   data=reslutcaselit)
            return jsonreponse(code=MessageEnum.success.value[0],
                               message=MessageEnum.success.value[1],
                               data=[])