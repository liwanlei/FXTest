# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:06:16
# @Author  : lileilei
from app.common.requ_case import Api
from app.common.dict_com import assert_in
from app.common.panduan import pare_result_mysql
from app.common.log import log_t
from app.models import InterfaceTest,TestcaseResult
from app.common.mysqldatabasecur import *
from  app import db
class ApiTestCase():
    def __init__(self,inteface_url,inteface_meth,inteface_parm,inteface_assert,file,headers,pid,yilaidata,saveresult,id_list,
                 is_database,data_mysql,data_ziduan,urltest):
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
        self.is_database=is_database
        self.data_mysql=data_mysql
        self.data_ziduan=data_ziduan
        self.title = u'测试日志'
        self.log_can = log_t(self.title, filename=file)
        self.urltest=urltest
    def testapi(self):
        for case in range(len(self.url)):
            self.log_can.info_log('%s：测试用例开始执行'%self.id[case])
            testcase=InterfaceTest.query.filter_by(id=self.id[case]).first()
            try:
                yuanlai = eval(self.parm[case])
            except Exception as e:
                self.log_can.error_log('用例：%s转化参数！原因：%s' % (self.id[case], e))
                self.result_toal += 1
                self.result_except += 1
                self.bask_list.append('转化参数，%s' % e)
                self.result_pf.append('Exception')
                continue
            mysql_result=[]
            if testcase.pid !="None":
                testret=TestcaseResult.query.filter_by(case_id=int(testcase.pid)).first()
                if testret:
                    data=testret.result
                    if data:
                        try:
                            huoqudata=eval(data)[testcase.getattr_p]
                            yuanlai.update({testcase.getattr_p: huoqudata})
                        except Exception as e:
                            self.log_can.error_log('用例：%s 提出依赖数据出错！原因：%s'%(self.id[case],e))
                            self.result_toal += 1
                            self.result_except += 1
                            self.bask_list.append('获取依赖的字段异常，%s'%e)
                            self.result_pf.append('Exception')
                    else:
                        self.log_can.info_log('用例：%s接口依赖结果没有保存!'%self.id[case] )
                        self.result_toal += 1
                        self.result_wei += 1
                        self.bask_list.append('依赖的测试结果没有保存')
                        self.result_pf.append(u'Exception')
                else:
                    self.log_can.info_log('用例：%s 依赖接口找不到!' % self.id[case])
                    self.result_toal += 1
                    self.result_wei += 1
                    self.bask_list.append('依赖的测试用例找不到')
                    self.result_pf.append(u'error')
            if self.is_database[case] is True:
                if self.urltest is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append('None')
                    self.result_pf.append(u'测试环境不存在')
                if testcase.chaxunshujuku is None or testcase.databaseziduan is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append('None')
                    self.result_pf.append(u'用例找不到查询数据库或者断言参数')
                if self.urltest.database is None :
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append('None')
                    self.result_pf.append(u'数据库没有配置！')
                if self.urltest.dbport is None or self.urltest.dbhost is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append('检查数据库的地址和端口！')
                    self.result_pf.append(u'检查数据库的地址和端口！')
                if self.urltest.databaseuser is None or self.urltest.databasepassword is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append('数据库登录账户没有找到')
                    self.result_pf.append(u'数据库登录账户没有找到')
                conncts=cursemsql(host=self.urltest.dbhost,port=self.urltest.dbport,user=self.urltest.databaseuser,password=self.urltest.databasepassword,database=self.urltest.database)
                if conncts['code']==0:
                    self.result_toal += 1
                    self.result_except += 1
                    self.bask_list.append('链接数据库异常')
                    self.result_pf.append('Exception')
                else:
                    result_myql=excemysql(conne=conncts['conne'],Sqlmy=self.data_mysql[case])
                    if result_myql['code']==0:
                        self.result_toal += 1
                        self.result_except += 1
                        self.bask_list.append(conncts['e'])
                        self.result_pf.append('Exception')
                    mysql_result=result_myql['result']
            try:
                api = Api(url=self.url[case], fangshi=self.meth[case], params=yuanlai,
                              headers=self.headers[case])
                apijson = api.getJson()
                if self.saveresult[case] is True:
                    new_case = TestcaseResult(result=str(apijson), case_id=testcase.id)
                    db.session.add(new_case)
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        self.log_can.info_log('用例：%s保存测试结果失败!原因：%s' % (self.id[case],e))
                self.log_can.info_log(u'测试的:接口地址：%s,请求头：%s,参数:%s,实际返回:%s,预期:%s' % (
                self.url[case], self.headers[case], self.parm[case], apijson, self.assert_test[case]))
                come = assert_in(self.assert_test[case], apijson)
                return_mysql = pare_result_mysql(mysqlresult=mysql_result, return_result=come,
                                                 paseziduan=self.data_ziduan[case])
                if come == 'pass' and return_mysql['result']=='pass':
                    self.result_pass += 1
                    self.result_toal += 1
                    self.bask_list.append(apijson)
                    self.result_pf.append('pass')
                elif come == 'fail' or return_mysql['result']=='fail':
                    self.result_fail += 1
                    self.result_toal += 1
                    self.bask_list.append(apijson)
                    self.result_pf.append('fail')
                elif come == '预期不存在':
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.bask_list.append(apijson)
                    self.result_pf.append(u'预期不存在')
                elif '异常' in come or return_mysql['code']== 1 :
                    self.result_toal += 1
                    self.result_except += 1
                    self.bask_list.append((apijson,return_mysql['result']))
                    self.result_pf.append('Exception')
                else:
                    self.result_toal += 1
                    self.result_wei += 1
                    self.bask_list.append(apijson)
                    self.result_pf.append(u'未知错误')
            except Exception as e:
                self.log_can.info_log('用例：%s执行失败!原因：%s' % (self.id[case], e))
                self.result_toal += 1
                self.result_except += 1
                self.bask_list.append(e)
                self.result_pf.append('Exception')
                continue
        return self.result_toal ,self.result_pass,self.result_fail,self.result_pf,self.bask_list,self.result_cashu,self.result_wei,self.result_except