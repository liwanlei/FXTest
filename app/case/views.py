""" 
@author: lileilei
@file: view.py 
@time: 2018/1/31 13:20 
"""
from flask import redirect, request, render_template, \
    session, url_for, flash, Blueprint, make_response, \
    send_from_directory
from app.models import *
from app.form import *
from config import Dingtalk_access_token
import os, time, datetime, json
from common.parsingexcel import paser_interface_case
from common.htmltestreport import createHtml
from common.requ_case import Api
from common.judgment import assert_in, pare_result_mysql
from app.test_case.Test_case import ApiTestCase
from common.send_email import send_emails
from flask.views import View, MethodView
from flask_login import current_user, login_required
from common.Dingtalk import send_ding
from common.oparmysqldatabase import *
from config import Config_import, redis_host, \
    redis_port, redis_save_result_db, save_duration, \
    jmeter_data_db, paln_run_url
from common.opearexcel import create_interface_case
from common.mergelist import listmax
from common.packageredis import ConRedisOper
from common.CreateJxmUntil import make
from common.SshTools import Sshtool
from common.systemlog import logger
from error_message import MessageEnum
from common.jsontools import reponse as jsonreponse
from app.test_case.new_unittest_case import TestCase,Parmer
from common.BSTestRunner import BSTestRunner
import unittest
case = Blueprint('case', __name__)


def save_reslut(key, value):
    redis = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    redis.sethash(str(key), str(value), save_duration)


def get_reslut(key):
    redis = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    reslit = redis.getset(key)
    return reslit


def get_project_model():
    projects = Project.query.filter_by(status=False).all()
    model = Model.query.filter_by(status=False).all()
    return projects, model


class AddtestcaseView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        form = Interface_case_Form()
        project, models = get_project_model()
        inrterface_list = Interface.query.filter_by(status=False).all()
        mock_yilai = Mockserver.query.filter_by(delete=False).all()
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).order_by(Project.id.desc()).all()
        else:
            projects = []
            id = []
            for i in current_user.quanxians:
                if (i.projects in id) is False:
                    if i.projects.status is False:
                        projects.append(i.projects)
                        id.append(i.projects)
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
                    flash(MessageEnum.reply_must_be_repy_flied.value[1])
                    return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                                           inrterface_list=inrterface_list, mock_yilai=mock_yilai)
                yilai_dat = yilai_data
            if yongli_nam == '' or mode == '' or interface_header == '' or interface_url == '' or interface_meth == '':
                flash(MessageEnum.must_be_every_parame.value[1])
                return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                                       inrterface_list=inrterface_list, mock_yilai=mock_yilai)
            print(yongli_nam)
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
                                       models=models, inrterface_list=inrterface_list)

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
                    for key, value in dict(eval(interface_can)):
                        if str(value).startswith("#"):
                            if str(value).split(".")[0] == '#action':
                                action = Action.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.action_not_exict.value[1])
                                    return render_template('add/add_test_case.html', form=form, projects=projects,
                                                           models=models,
                                                           inrterface_list=inrterface_list, mock_yilai=mock_yilai)
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
                                                           inrterface_list=inrterface_list, mock_yilai=mock_yilai)
                                caseac = CaseGeneral(case=newcase, general=action, filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            else:
                                pass
                except:
                    flash(MessageEnum.test_feild.value[1])
                    return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                                           inrterface_list=inrterface_list, mock_yilai=mock_yilai)
                flash(MessageEnum.successs.value[1])
                return redirect(url_for('home.case'))
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                flash(MessageEnum.add_case_erro)
                return redirect(url_for('home.case'))
        return render_template('add/add_test_case.html', form=form, projects=projects, models=models,
                               inrterface_list=inrterface_list, mock_yilai=mock_yilai)


class EditcaseView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self, id):
        project, models = get_project_model()
        inrterface_list = Interface.query.filter_by(status=False).all()
        mock_yilai = Mockserver.query.filter_by(delete=False).all()
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
        edit_case = InterfaceTest.query.filter_by(id=id, status=False).first()
        if not edit_case:
            flash(MessageEnum.case_not_exict.value[1])
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
                    flash(MessageEnum.reply_must_be_repy_flied.value[1])
                    return render_template('edit/edit_case.html', edit=edit_case,
                                           projects=projects, models=models,
                                           inerfacelist=inrterface_list, mock_yilai=mock_yilai)
                yilai_dat = yilai_data
            if yongli_nam == None or mode == None or url == '' or headers == '' or meth == '' or reque == '':
                flash(MessageEnum.edit_interface_null_parame.value[1])
                return render_template('edit/edit_case.html', edit=edit_case, projects=projects,
                                       models=models,
                                       inerfacelist=inrterface_list, mock_yilai=mock_yilai)
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
                                       inerfacelist=inrterface_list, mock_yilai=mock_yilai)
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
                    for key, value in dict(eval(parme)):
                        if str(value).startswith("#"):
                            if str(value).split(".")[0] == '#action':
                                action = Action.query.filter_by(name=str(value).split(".")[1]).first()
                                if not action:
                                    flash(MessageEnum.action_not_exict.value[1])
                                    return render_template('edit/edit_case.html', edit=edit_case,
                                                           projects=projects, models=models,
                                                           inerfacelist=inrterface_list, mock_yilai=mock_yilai)
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
                                                           inerfacelist=inrterface_list, mock_yilai=mock_yilai)
                                caseac = CaseGeneral(case=edit_case, general=action, filed=key)
                                db.session.add(caseac)
                                db.session.commit()
                            else:
                                pass
                except:
                    flash(MessageEnum.test_feild.value[1])
                    return render_template('edit/edit_case.html', edit=edit_case,
                                           projects=projects, models=models,
                                           inerfacelist=inrterface_list, mock_yilai=mock_yilai)

                db.session.commit()
                flash(MessageEnum.successs.value[1])
                return redirect(url_for('home.case'))
            except Exception as e:
                print(e)
                db.session.rollback()
                flash(MessageEnum.case_edit_error.value[1])
                return render_template('edit/edit_case.html',
                                       edit=edit_case, projects=projects, models=models,
                                       inerfacelist=inrterface_list, mock_yilai=mock_yilai)
        return render_template('edit/edit_case.html', edit=edit_case, projects=projects,
                               models=models, inerfacelist=inrterface_list, mock_yilai=mock_yilai)


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
        return jsonreponse(message=MessageEnum.successs.value[1],
                           code=MessageEnum.successs.value[0],
                           data=data)


class ImportCaseView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        if request.method == 'POST':
            file = request.files['myfile']
            if file and '.' in file.filename and file.filename.split('.')[1] == 'xlsx':
                filename = 'jiekoucase.xlsx'
                file.save(filename)
                jiekou_bianhao, interface_name, project_nam, model_nam, interface_url, interfac_header, \
                interface_meth, interface_par, interface_bas, interface_type, is_save_result, yilai_is, \
                yilai, yilai_ziduan, is_cha_data, data_sql, paser_base = paser_interface_case(filename)
                if len(yilai) > Config_import:
                    flash(MessageEnum.import_max_big.value[1])
                    return redirect(url_for('home.import_case'))
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=str(project_nam[i])).first()
                        model_id = Model.query.filter_by(model_name=str(model_nam[i])).first()
                        if projects_id is None:
                            flash(MessageEnum.project_not_exict.value[1])
                            return redirect(url_for('home.import_case'))
                        if model_id is None:
                            flash(MessageEnum.model_not_exict.value[1])
                            return redirect(url_for('home.import_case'))
                        if is_save_result[i] == '是':
                            save_reslt = True
                        elif is_save_result[i] == '否':
                            save_reslt = False
                        else:
                            save_reslt = False
                        if is_cha_data[i] == '是':
                            chaxun = True
                        elif is_cha_data[i] == '否':
                            chaxun = False
                        else:
                            chaxun = False
                        if yilai_is[i] == '是':
                            yilai_case = yilai[i]
                            ziduan_case = yilai_ziduan[i]
                        else:
                            yilai_case = None
                            ziduan_case = None
                        new_interface = InterfaceTest(projects_id=projects_id.id,
                                                      model_id=model_id.id,
                                                      Interface_name=str(interface_name[i]),
                                                      Interface_url=str(interface_url[i]),
                                                      Interface_headers=interfac_header[i],
                                                      Interface_meth=str(interface_meth[i]),
                                                      interface_type=str(interface_type[i]),
                                                      Interface_pase=(interface_par[i]),
                                                      Interface_assert=str(interface_bas[i]),
                                                      saveresult=save_reslt,
                                                      is_database=chaxun,
                                                      chaxunshujuku=data_sql[i],
                                                      databaseziduan=paser_base[i],
                                                      pid=yilai_case,
                                                      getattr_p=ziduan_case,
                                                      Interface_user_id=User.query.filter_by(
                                                          username=session.get('username')).first().id)
                        db.session.add(new_interface)
                        db.session.commit()
                    flash(MessageEnum.import_success.value[1])
                    return redirect(url_for('home.case'))
                except Exception as e:
                    logger.exception(e)
                    db.session.rollback()
                    flash(MessageEnum.import_fail.value[1])
                    return render_template('import_case.html')
            flash(MessageEnum.import_fail.value[1])
            return render_template('import_case.html')
        return render_template('import_case.html')



class MuliteCaseLiView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        next = request.headers.get('Referer')
        starttime = datetime.datetime.now()
        star = time.time()
        day = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        pad = os.getcwd()
        file_dir = pad + '/app/upload'
        file = os.path.join(file_dir, (day + '.log'))
        if os.path.exists(file) is False:
            os.system('touch %s' % file)
        filepath = os.path.join(file_dir, (day + '.html'))
        if os.path.exists(filepath) is False:
            os.system(r'touch %s' % filepath)
        if request.method == 'POST':
            f_dingding = request.form.get('dingding')
            allcase = request.form.getlist('yongli')
            testurl = request.form.get('urltest')
            if len(allcase) <= 1:
                flash(MessageEnum.case_many_to_select.value[1])
                return redirect(next or url_for('yongli'))
            if testurl is None:
                flash(MessageEnum.select_event.value[1])
                return redirect(next or url_for('yongli'))
            testcase_list=[]
            projecct_list=[]
            for case in allcase:
                run_case_item={}
                case_one = InterfaceTest.query.filter_by(id=case).first()
                run_case_item['caselog']=file
                run_case_item['id']=case_one
                run_case_item['project']=case_one.projects
                projecct_list.append(case_one.projects)
                run_case_item['testevent']=Interfacehuan.query.filter_by(url=testurl).first()
                testcase_list.append(run_case_item)
            if (len(set(projecct_list))) > 1:
                flash(MessageEnum.run_only_one_project.value[1])
                return redirect(next or url_for('mulitecase'))
            test_suit = unittest.TestSuite()
            test_suit.addTest(Parmer.parametrize(TestCase, parame=testcase_list))  # 扩展的其他的测试用例均这样添加
            re_open = open(filepath, 'wb')
            runner = BSTestRunner(stream=re_open,
                                  title=u'自动化测试平台自动生成',
                                  description=u'自动化测试结果')
            n = runner.run(test_suit)
            success = n.success_count
            faill = n.failure_count
            error = n.error_count
            end = time.time()
            hour = end - star
            new_reust = TestResult(Test_user_id=current_user.id,
                                   test_num=success+faill+error,
                                   pass_num=success,
                                           fail_num=faill,
                                   test_time=starttime,
                                   hour_time=hour,
                                           test_rep=day + '.html',
                                   test_log=day + '.log',
                                           Exception_num=error, can_num=0,
                                           wei_num=0, projects_id=projecct_list[0].id)
            db.session.add(new_reust)
            db.session.commit()
            if f_dingding == 'email':
                email = EmailReport.query.filter_by(email_re_user_id=int(current_user.id),
                                                            default_set=True).first()
                if email:
                    m = send_emails(sender=email.send_email, receivers=email.to_email,
                                            password=email.send_email_password,
                                            smtp=email.stmp_email, port=email.port, annexone=file,
                                            annextwo=filepath,
                                            subject=u'%s用例执行测试报告' % day,
                                            url=paln_run_url + '/test_result')
                    if m == False:
                        flash(MessageEnum.send_email_fali.value[1])
                        return redirect(url_for('home.test_result'))
                    flash(MessageEnum.send_email_success.value[1])
                    return redirect(url_for('home.test_result'))
            flash(MessageEnum.send_email_success.value[1])
            return redirect(url_for('home.test_result'))


class MakeOnlyOneCaseView(MethodView):
    @login_required
    def post(self):
        projec = request.get_json()
        case_id = projec['caseid']
        url = projec['url']
        testevent = Interfacehuan.query.filter_by(url=str(url)).first()
        if not testevent:
            return jsonreponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
        case = InterfaceTest.query.filter_by(id=int(case_id), status=False).first()
        if not case:
            return jsonreponse(code=MessageEnum.test_case.value[0],
                               message=MessageEnum.test_case.value[1])
        try:
            if case.interface_type == 'http':
                if case.pid is not None and case.pid != 'None' and case.pid != '':
                    tesyi = get_reslut(key=case.id + "&" + url)
                    if tesyi is not None:
                        canshu = case.getattr_p
                        try:
                            testres = eval(tesyi.decode('utf-8'))
                            yilaidata = eval(testres)[canshu]
                        except Exception as e:
                            logger.exception(e)
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.get_reply_data_fail.value[0],
                                               message=MessageEnum.get_reply_data_fail.value[1])
                        try:
                            pasrms = eval(case.Interface_pase)
                            pasrms.update({canshu: yilaidata})
                        except:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_feild.value[0],
                                               message=MessageEnum.test_feild.value[1])
                    else:
                        try:
                            pasrms = eval(case.Interface_pase)
                        except:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_feild.value[0],
                                               message=MessageEnum.test_feild.value[1])
                else:
                    if case.Interface_pase is None or case.Interface_pase == "null":
                        pasrms = {}
                    else:
                        try:
                            pasrms = json.loads(case.Interface_pase)
                        except Exception as e:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_feild.value[0],
                                               message=MessageEnum.test_feild.value[1])
                new_headers = case.Interface_headers
                if new_headers == 'None':
                    new_header = {'host': url}
                elif new_headers is None:
                    new_header = {'host': url}
                else:
                    try:
                        new_header = eval(new_headers)
                        new_header['host'] = url
                    except:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_feild.value[0],
                                           message=MessageEnum.test_feild.value[1])
                if case.is_database is True:

                    if case.chaxunshujuku is None or case.databaseziduan is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.assert_not_in_or_sql_not_in.value[0],
                                           message=MessageEnum.assert_not_in_or_sql_not_in.value[1])
                    if testevent.database is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_url_not_in.value[0],
                                           message=MessageEnum.test_sql_url_not_in.value[1])
                    if testevent.dbport is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_port_not_in.value[0],
                                           message=MessageEnum.test_sql_port_not_in.value[1])
                    if testevent.dbhost is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_host_not_in.value[0],
                                           message=MessageEnum.test_sql_host_not_in.value[1])
                    if testevent.databaseuser is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_login_user_not_in.value[0],
                                           message=MessageEnum.test_sql_login_user_not_in.value[1])
                    if testevent.databasepassword is None:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_login_user_password_not_in.value[0],
                                           message=MessageEnum.test_sql_login_user_password_not_in.value[1])
                    if case.databaseziduan == "" or case.chaxunshujuku == "":
                        return jsonreponse(code=MessageEnum.test_sql_repy_sql_feild.value[0],
                                           message=MessageEnum.test_sql_repy_sql_feild.value[1])
                    conncts = cursemsql(host=testevent.dbhost, port=testevent.dbport,
                                        user=testevent.databaseuser, password=testevent.databasepassword,
                                        database=testevent.database)
                    if conncts['code'] == 0:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_connect_sql_error.value[0],
                                           message=MessageEnum.test_sql_connect_sql_error.value[1])
                    else:
                        result_myql = excemysql(conne=conncts['conne'], Sqlmy=case.chaxunshujuku)
                        if result_myql['code'] == 0:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            logger.error(result_myql)
                            return jsonreponse(code=MessageEnum.test_sql_query_error.value[0],
                                               message=MessageEnum.test_sql_query_error.value[1])
                        mysql_result = result_myql['result']
                else:
                    mysql_result = []
                try:
                    data = json.dumps(pasrms)
                except Exception as e:
                    logger.exception(e)
                    case.Interface_is_tiaoshi = True
                    case.Interface_tiaoshi_shifou = True
                    db.session.commit()
                    return jsonreponse(code=MessageEnum.change_parames_faild.value[0],
                                       message=MessageEnum.change_parames_faild.value[1])

                response = Api(url=testevent.url + case.Interface_url,
                               method=case.Interface_meth,
                               params=data, headers=new_header)
                result = response.getJson()
                if result == "请求出错了":
                    return jsonreponse(code=MessageEnum.test_case_run_error.value[0],
                                       message=MessageEnum.test_case_run_error.value[1])
                spend = response.spend()
                if case.databaseziduan is not None:
                    return_mysql = pare_result_mysql(mysqlresult=mysql_result,
                                                     return_result=result, paseziduan=case.databaseziduan)

                print(result)
                retur_re = assert_in(case.Interface_assert, result)
                try:
                    if case.is_database is True:
                        if retur_re == 'pass' and return_mysql['result'] == 'pass':
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = False
                            save_reslut(key=str(case.id) + "&" + url, value=str(result))
                            return jsonreponse(code=MessageEnum.test_case_run_pass.value[0],
                                               message=MessageEnum.test_case_run_pass.value[1]
                                               )
                        elif retur_re == 'fail' or return_mysql['result'] == 'fail':
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            save_reslut(key=str(case.id) + "&" + url, value=str(result))
                            return jsonreponse(code=MessageEnum.test_case_run_fail.value[0],
                                               message=MessageEnum.test_case_run_fail.value[1])
                        else:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            save_reslut(key=str(case.id) + "&" + url, value=str(result))
                            return jsonreponse(code=MessageEnum.test_case_requesst_exception.value[0],
                                               message=MessageEnum.test_case_requesst_exception.value[1])

                    if retur_re == 'pass':
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = False
                        save_reslut(key=str(case.id) + "&" + url, value=str(result))
                        return jsonreponse(code=MessageEnum.test_case_run_pass.value[0],
                                           message=MessageEnum.test_case_run_pass.value[1])
                    else:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        key = str(case.id) + "&" + url

                        save_reslut(key=key, value=str(result))
                        return jsonreponse(code=MessageEnum.test_case_run_fail.value[0],
                                           message=MessageEnum.test_case_run_fail.value[1])
                except Exception as e:
                    logger.error(e)
                    case.Interface_is_tiaoshi = True
                    case.Interface_tiaoshi_shifou = True
                    save_reslut(key=str(case.id) + "&" + url, value=str(result))
                    return jsonreponse(code=MessageEnum.test_case_run_fail.value[0],
                                       message=MessageEnum.test_case_run_fail.value[1])
            else:
                return jsonreponse(code=MessageEnum.test_run_fail_not_support.value[0],
                                   message=MessageEnum.test_run_fail_not_support.value[1])
        except Exception as e:
            logger.exception(e)
            case.Interface_is_tiaoshi = True
            case.Interface_tiaoshi_shifou = True
            db.session.commit()
            return jsonreponse(code=MessageEnum.test_case_run_fail.value[0],
                               message=MessageEnum.test_case_run_fail.value[1])


class ExportCaseView(MethodView):
    @login_required
    def post(self):
        project = request.form.get('interface_type')
        project_case = Project.query.filter_by(project_name=str(project), status=False).first()
        if project_case is None:
            flash(MessageEnum.your_change_export_project_not_exict.value[1])
            return redirect(url_for('home.interface'))
        interface_list = InterfaceTest.query.filter_by(projects_id=project_case.id, status=False).all()
        pad = os.getcwd()
        day = time.strftime("%Y%m%d", time.localtime(time.time()))
        file_dir = pad + '/app/upload'
        file = os.path.join(file_dir, (day + '.xls'))
        if os.path.exists(file) is False:
            os.system('touch %s' % file)
        result = create_interface_case(filename=file, caselist=interface_list)
        if result['code'] == 1:
            logger.info('导出接口失败！原因：%s' % result['error'])
            flash(MessageEnum.your_export_interface_fail.value[1])
            return redirect(url_for('home.case'))
        response = make_response(send_from_directory(file_dir, filename=day + '.xls', as_attachment=True))
        return response


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
        return jsonreponse(code=MessageEnum.successs.value[0],
                           message=MessageEnum.successs.value[1], data=result_all)




class CaseToJmxView(MethodView):
    def post(self):
        try:
            data_jmx = eval(request.get_data().decode('utf-8'))
        except Exception as e:
            logger.exception(e)
            return jsonreponse(code=MessageEnum.Incorrect_format.value[0],
                               message=MessageEnum.Incorrect_format.value[1])
        interfacecaseid = data_jmx["interfaceid"]
        testid = data_jmx["testeventid"]
        runcount = data_jmx["runcount"]
        loopcount = data_jmx["loopcount"]
        dbname = jmeter_data_db
        testserverid = data_jmx["testserverid"]
        case_one = InterfaceTest.query.filter_by(id=int(interfacecaseid)).first()
        if not case_one:
            return jsonreponse(code=MessageEnum.case_not_exict.value[0],
                               message=MessageEnum.case_not_exict.value[1])
        testvents = Interfacehuan.query.filter_by(id=int(testid)).first()
        if not testvents:
            return jsonreponse(code=MessageEnum.testeveirment_not_exict.value[0],
                               message=MessageEnum.testeveirment_not_exict.value[1])
        tetserver = Testerver.query.filter_by(id=int(testserverid), status=0).first()
        if not tetserver:
            return jsonreponse(code=MessageEnum.test_server_not_exict.value[0],
                               message=MessageEnum.test_server_not_exict.value[1])
        all = str(testvents.url).split("://")[1].split(":")
        if len(all) == 1:
            port = 80
        else:
            port = int(all[1])

        parame = ""
        if case_one.Interface_pase is not None:
            try:
                data = eval(case_one.Interface_pase)
                for key, value in data.items():
                    parame += '''' <elementProp name="password" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">%s</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
                <stringProp name="Argument.name">%s</stringProp>
              </elementProp>''' % (value, key)
            except Exception as e:
                print(e)
                return jsonreponse(code=MessageEnum.case_to_jmx_case_fail.value[0],
                                   message=MessageEnum.case_to_jmx_case_fail.value[1])
        all = make(runcount, loopcount, all[0], port, case_one.interfaces.Interface_url,
                   case_one.Interface_meth, dbname, case_one.projects.project_name, parame)
        path = os.getcwd()
        filepath = path + "/jxmpath/"
        name = str(case_one.projects.project_name) + "_" + str(testvents.id) + "_" + str(case_one.id) + ".jmx"
        filepathname = filepath + name
        with open(filepathname, 'wb') as f:
            f.write(all.encode())
        testjmx = TestJmx(intefaceid=case_one.interfaces.id, runcounttest=runcount, loopcount=loopcount,
                          jmxpath=filepathname, serverid=tetserver.id, name=name)
        db.session.add(testjmx)
        db.session.commit()
        return jsonreponse(code=MessageEnum.case_to_jmx_success.value[0],
                           message=MessageEnum.case_to_jmx_success.value[1],
                           data=testjmx.id)


class JmxToServerView(MethodView):
    def get(self, id):
        '''
        todo
            1.服务器执行压测脚本开始后设置为正在运行
            2.如何压测执行完毕怎么修改这个服务器的状态
            3.执行完A压测需求，执行B压测需求，需要有先后，如何加入队列处理
            4.应该是一个公用的方法，内部也需要调用，这里需要抽离下
        '''
        testjmx = TestJmx.query.filter_by(id=int(id)).first()
        if not testjmx:
            return jsonreponse(code=MessageEnum.case_jmx_not_excit.value[0],
                               message=MessageEnum.case_jmx_not_excit.value[1])
        if testjmx.serverid is None:
            return jsonreponse(code=MessageEnum.case_jmx_not_select_server.value[0],
                               message=MessageEnum.case_jmx_not_select_server.value[1])
        testserver = Testerver.query.filter_by(id=int(testjmx.serverid), status=0).first()
        if not testserver:
            return jsonreponse(code=MessageEnum.case_test_sever_not_exict.value[0],
                               message=MessageEnum.case_test_sever_not_exict.value[1])
        cmd = "sshpass -p " + testserver.loginpassword + " scp -P " + testserver.port + "  " + testjmx.jmxpath + " " + testserver.loginuser + "@" + testserver.ip + ":/home"
        os.system(cmd)
        commentc = Sshtool(testserver.ip, testserver.port, testserver.loginuser, testserver.loginpassword)
        cmd = "./jmeter -n -t /home/" + testjmx.name + '  -l name.htl'
        commentc.command(cmd)
        testserver.is_run = 1
        db.session.add(testserver)
        db.session.commit()
        return jsonreponse(code=MessageEnum.case_jmx_run_seccess.value[0],
                           message=MessageEnum.case_jmx_run_seccess.value[1])


class GetProjectInterfaceCase(MethodView):
    def post(self,project:str=None,interface:str=None):
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

            interfacetestcaselist=InterfaceTest.query.filter_by(projects_id=projectis.id,
                                                                interface_id=interfaceis.id).all()
            if len(interfacetestcaselist)>0:
                reslutcaselit=[]
                for item in interfacetestcaselist:
                    caseitem={}
                    caseitem['id']=item.id
                    caseitem['name']=item.bian_num
                    reslutcaselit.append(caseitem)
                return jsonreponse(code=MessageEnum.successs.value[0],
                                   message=MessageEnum.successs.value[1],
                                   data=reslutcaselit)
            return jsonreponse(code=MessageEnum.successs.value[0],
                               message=MessageEnum.successs.value[1],
                               data=[])