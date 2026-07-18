# -*- coding: utf-8 -*-
"""import_export 视图。"""
from app import db
from app.case.case_operations._shared import *  # noqa: F401,F403

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
                yilai, yilai_ziduan, is_cha_data, data_sql, paser_base = parse_interface_case(filename)
                if len(yilai) > Config_import:
                    flash(MessageEnum.import_max_big.value[1])
                    return redirect(url_for('home.import_case'))
                try:
                    for i in range(len(jiekou_bianhao)):
                        projects_id = Project.query.filter_by(project_name=str(project_nam[i])).first()
                        model_id = Model.query.filter_by(model_name=str(model_nam[i])).first()
                        if projects_id is None:
                            flash(MessageEnum.project_not_exist.value[1])
                            return redirect(url_for('home.import_case'))
                        if model_id is None:
                            flash(MessageEnum.model_not_exist.value[1])
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
            open(file, 'a').close()
        result = create_interface_case(filename=file, caselist=interface_list)
        if result['code'] == 1:
            logger.info('导出接口失败！原因：%s' % result['error'])
            flash(MessageEnum.your_export_interface_fail.value[1])
            return redirect(url_for('home.case'))
        response = make_response(send_from_directory(file_dir, filename=day + '.xls', as_attachment=True))
        return response

