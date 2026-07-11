# -*- coding: utf-8 -*-
"""batch_run 视图。"""
from app.case.case_operations._shared import *  # noqa: F401,F403

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
            open(file, 'a').close()
        filepath = os.path.join(file_dir, (day + '.html'))
        if os.path.exists(filepath) is False:
            open(filepath, 'a').close()
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
            testcase_list = []
            projecct_list = []
            for case in allcase:
                run_case_item = {}
                case_one = InterfaceTest.query.filter_by(id=case).first()
                run_case_item['caselog'] = file
                run_case_item['id'] = case_one
                run_case_item['project'] = case_one.projects
                projecct_list.append(case_one.projects)
                run_case_item['testevent'] = Interfacehuan.query.filter_by(url=testurl).first()
                testcase_list.append(run_case_item)
            if (len(set(projecct_list))) > 1:
                flash(MessageEnum.run_only_one_project.value[1])
                return redirect(next or url_for('mulitecase'))
            test_suit = unittest.TestSuite()
            test_suit.addTest(Parmer.parametrize(TestCase, parame=testcase_list))
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
                                   test_num=success + faill + error,
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
                    if m is False:
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
            return jsonreponse(code=MessageEnum.test_environment_not_exist.value[0],
                               message=MessageEnum.test_environment_not_exist.value[1])
        case = InterfaceTest.query.filter_by(id=int(case_id), status=False).first()
        if not case:
            return jsonreponse(code=MessageEnum.test_case.value[0],
                               message=MessageEnum.test_case.value[1])
        try:
            if case.interface_type == 'http':
                if case.pid is not None and case.pid != 'None' and case.pid != '':
                    tesyi = get_result(key=case.id + "&" + url)
                    if tesyi is not None:
                        canshu = case.getattr_p
                        try:
                            testres = literal_eval(tesyi.decode('utf-8'))
                            yilaidata = testres[canshu]
                        except Exception as e:
                            logger.exception(e)
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.get_reply_data_fail.value[0],
                                               message=MessageEnum.get_reply_data_fail.value[1])
                        try:
                            pasrms = literal_eval(case.Interface_pase)
                            pasrms.update({canshu: yilaidata})
                        except Exception:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_field_should_be_dict.value[0],
                                               message=MessageEnum.test_field_should_be_dict.value[1])
                    else:
                        try:
                            pasrms = literal_eval(case.Interface_pase)
                        except Exception:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_field_should_be_dict.value[0],
                                               message=MessageEnum.test_field_should_be_dict.value[1])
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
                            return jsonreponse(code=MessageEnum.test_field_should_be_dict.value[0],
                                               message=MessageEnum.test_field_should_be_dict.value[1])
                new_headers = case.Interface_headers
                if new_headers == 'None':
                    new_header = {'host': url}
                elif new_headers is None:
                    new_header = {'host': url}
                else:
                    try:
                        new_header = literal_eval(new_headers)
                        new_header['host'] = url
                    except Exception:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_field_should_be_dict.value[0],
                                           message=MessageEnum.test_field_should_be_dict.value[1])
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
                        return jsonreponse(code=MessageEnum.test_sql_reply_sql_field.value[0],
                                           message=MessageEnum.test_sql_reply_sql_field.value[1])
                    conncts = create_mysql_conn(host=testevent.dbhost, port=testevent.dbport,
                                        user=testevent.databaseuser, password=testevent.databasepassword,
                                        database=testevent.database)
                    if conncts['code'] == 0:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_sql_connect_sql_error.value[0],
                                           message=MessageEnum.test_sql_connect_sql_error.value[1])
                    else:
                        result_myql = execute_sql(conne=conncts['conne'], Sqlmy=case.chaxunshujuku)
                        if result_myql['code'] == 0:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            return jsonreponse(code=MessageEnum.test_sql_connect_sql_error.value[0],
                                               message=MessageEnum.test_sql_connect_sql_error.value[1])
                if case.Interface_meth == 'POST':
                    try:
                        case.Interface_headers = literal_eval(case.Interface_headers)
                    except Exception as e:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_field_should_be_dict.value[0],
                                           message=MessageEnum.test_field_should_be_dict.value[1])
                new_api = Api(url=testevent.url, method=case.Interface_meth,
                              params=pasrms, headers=new_header)
                if case.is_database:
                    result = pare_result_mysql(api=new_api, case=case, conncts=conncts['conne'],
                                               mysqlziduan=case.databaseziduan,
                                               sql=case.chaxunshujuku)
                    if result:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = True
                        db.session.commit()
                        return jsonreponse(code=MessageEnum.test_case_run_success.value[0],
                                           message=MessageEnum.test_case_run_success.value[1])
                    else:
                        case.Interface_is_tiaoshi = True
                        case.Interface_tiaoshi_shifou = False
                        db.session.commit()
                        save_result(key=str(case.id) + "&" + url, value=str(result))
                        return jsonreponse(
                            code=MessageEnum.test_case_run_fail.value[0],
                            message=MessageEnum.test_case_run_fail.value[1])
                result = assert_in(case.Interface_assert, new_api.getJson())
                if result:
                    case.Interface_is_tiaoshi = True
                    case.Interface_tiaoshi_shifou = True
                    db.session.commit()
                    return jsonreponse(code=MessageEnum.test_case_run_success.value[0],
                                       message=MessageEnum.test_case_run_success.value[1])
                else:
                    case.Interface_is_tiaoshi = True
                    case.Interface_tiaoshi_shifou = False
                    db.session.commit()
                    save_result(key=str(case.id) + "&" + url, value=str(result))
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

