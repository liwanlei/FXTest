# -*- coding: utf-8 -*-
"""jmx 视图。"""
from app import db
from app.case.case_operations._shared import *  # noqa: F401,F403

class CaseToJmxView(MethodView):
    def post(self):
        try:
            data_jmx = json.loads(request.get_data().decode('utf-8'))
        except Exception as e:
            logger.exception(e)
            return jsonreponse(code=MessageEnum.incorrect_format.value[0],
                               message=MessageEnum.incorrect_format.value[1])
        interfacecaseid = data_jmx["interfaceid"]
        testid = data_jmx["testeventid"]
        runcount = data_jmx["runcount"]
        loopcount = data_jmx["loopcount"]
        dbname = jmeter_data_db
        testserverid = data_jmx["testserverid"]
        case_one = InterfaceTest.query.filter_by(id=int(interfacecaseid)).first()
        if not case_one:
            return jsonreponse(code=MessageEnum.case_not_exist.value[0],
                               message=MessageEnum.case_not_exist.value[1])
        testvents = Interfacehuan.query.filter_by(id=int(testid)).first()
        if not testvents:
            return jsonreponse(code=MessageEnum.test_environment_not_exist.value[0],
                               message=MessageEnum.test_environment_not_exist.value[1])
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
                data = literal_eval(case_one.Interface_pase)
                for key, value in data.items():
                    parame += '''' <elementProp name="password" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">%s</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
                <stringProp name="Argument.name">%s</stringProp>
              </elementProp>''' % (value, key)
            except Exception as e:
                logger.exception(e)
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
            return jsonreponse(code=MessageEnum.case_jmx_not_exist.value[0],
                               message=MessageEnum.case_jmx_not_exist.value[1])
        if testjmx.serverid is None:
            return jsonreponse(code=MessageEnum.case_jmx_not_select_server.value[0],
                               message=MessageEnum.case_jmx_not_select_server.value[1])
        testserver = Testerver.query.filter_by(id=int(testjmx.serverid), status=0).first()
        if not testserver:
            return jsonreponse(code=MessageEnum.case_test_sever_not_exit.value[0],
                               message=MessageEnum.case_test_sever_not_exit.value[1])
        subprocess.run([
            'sshpass', '-p', testserver.loginpassword,
            'scp', '-P', str(testserver.port),
            testjmx.jmxpath,
            f'{testserver.loginuser}@{testserver.ip}:/home'
        ], check=False)
        commentc = Sshtool(testserver.ip, int(testserver.port), testserver.loginuser, testserver.loginpassword)
        cmd = "./jmeter -n -t /home/" + testjmx.name + '  -l name.htl'
        commentc.command(cmd)
        testserver.is_run = 1
        db.session.add(testserver)
        db.session.commit()
        return jsonreponse(code=MessageEnum.case_jmx_run_seccess.value[0],
                           message=MessageEnum.case_jmx_run_seccess.value[1])

