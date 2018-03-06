# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:06:16
# @Author  : lileilei
from app.common.requ_case import Api
from app.common.dict_com import assert_in
from app.common.log import log_t
from app.models import InterfaceTest,TestcaseResult
from  app import db
class ApiTestCase():
    def __init__(self,inteface_url,inteface_meth,inteface_parm,inteface_assert,file,headers,pid,yilaidata,saveresult,id_list):
        self.result_pass=0
        self.result_fail=0
        self.result_toal=0
        self.result_except=0
        self.result_cashu=0
        self.result_wei=0
        self.url=inteface_url
        self.meth=inteface_meth
        self.parm=inteface_parm
        self.assert_test=inteface_assert
        self.bask_list=[]
        self.result_pf=[]
        self.headers=headers
        self.pid=pid
        self.yilaidata=yilaidata
        self.saveresult=saveresult
        self.id=id_list
        self.title = u'测试日志'
        self.log_can = log_t(self.title, filename=file)
    def testapi(self):
        for case in range(len(self.url)):
            testcase=InterfaceTest.query.filter_by(id=self.id[case]).first()
            if testcase.pid !="None":
                testret=TestcaseResult.query.filter_by(case_id=int(testcase.pid)).first()
                if testret:
                    data=testret.result
                    if data:
                        try:
                            huoqudata=eval(data)[testcase.getattr_p]
                        except Exception as e:
                            self.result_toal += 1
                            self.result_except += 1
                            self.bask_list.append('获取依赖的字段异常，%s'%e)
                            self.result_pf.append('Exception')

                    else:
                        self.result_toal += 1
                        self.result_wei += 1
                        self.bask_list.append('依赖的测试结果没有保存')
                        self.result_pf.append(u'Exception')
                else:
                    self.result_toal += 1
                    self.result_wei += 1
                    self.bask_list.append('依赖的测试用例没有保存')
                    self.result_pf.append(u'Exception')
            else:
                try:
                    yuanlai=eval(self.parm[case])
                    yuanlai.update({testcase.getattr_p:huoqudata})
                    api = Api(url=self.url[case], fangshi=self.meth[case], params=self.parm[case],
                              headers=self.headers[case])
                    apijson = api.getJson()
                    if self.saveresult[case] is True:
                        new_case = TestcaseResult(result=str(apijson), case_id=testcase.id)
                        db.session.add(new_case)
                        try:
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                    self.log_can.info_log(u'测试的:接口地址：%s,请求头：%s,参数:%s,实际返回:%s,预期:%s' % (
                    self.url[case], self.headers[case], self.parm[case], apijson, self.assert_test[case]))
                    come = assert_in(self.assert_test[case], apijson)
                    if come == 'pass':
                        self.result_pass += 1
                        self.result_toal += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append('pass')
                    elif come == 'fail':
                        self.result_fail += 1
                        self.result_toal += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append('fail')
                    elif come == '预期不存在':
                        self.result_toal += 1
                        self.result_cashu += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append(u'预期不存在')
                    elif '异常' in come:
                        self.result_toal += 1
                        self.result_except += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append('Exception')
                    else:
                        self.result_toal += 1
                        self.result_wei += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append(u'未知错误')
                except:
                    self.result_toal += 1
                    self.result_wei += 1
                    self.bask_list.append('参数必须是json格式')
                    self.result_pf.append(u'Exception')
            print(self.result_toal ,self.result_pass,self.result_fail,self.result_pf,self.bask_list,self.result_cashu,self.result_wei,self.result_except)
        return self.result_toal ,self.result_pass,self.result_fail,self.result_pf,self.bask_list,self.result_cashu,self.result_wei,self.result_except