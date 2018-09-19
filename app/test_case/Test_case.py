# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:06:16
# @Author  : lileilei
'''封装多用例执行'''
from common.requ_case import Api
from common.panduan import assert_in
from common.panduan import pare_result_mysql
from common.log import log_t
from app.models import InterfaceTest, TestcaseResult,Interfacehuan,mockforcase,Mockserver
from common.mysqldatabasecur import *
from config import  redis_host,redis_port,redis_save_result_db,save_duration,xitong_request_toke
from app import db
from common.pyredis import ConRedisOper
def save_reslut(key,value):
    m = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    m.sethase(key,value,save_duration)
def get_reslut(key):
    m = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    reslit=m.getset(key)
    return reslit
class ApiTestCase():
    def __init__(self, inteface_url, inteface_meth, inteface_parm,
                 inteface_assert, file, headers, pid, yilaidata, saveresult,
                 id_list, is_database, data_mysql, data_ziduan, urltest):
        self.result_pass =0
        self.result_fail =0
        self.result_toal =0
        self.result_except=0
        self.result_cashu=0
        self.result_wei=0
        self.url =inteface_url
        self.meth =inteface_meth
        self.parm =inteface_parm
        self.assert_test =inteface_assert
        self.bask_list =[]
        self.result_pf =[]
        self.headers =headers
        self.pid = pid
        self.yilaidata =yilaidata
        self.saveresult =saveresult
        self.id = id_list
        self.is_database =is_database
        self.data_mysql =data_mysql
        self.data_ziduan =data_ziduan
        self.title=u'测试日志'
        self.log_can=log_t(self.title, filename=file)
        self.urltest=urltest
        self.spendlist=[]
    def testapi(self):
        for case in range(len(self.url)):
            self.log_can.info_log('%s：测试用例开始执行' % self.id[case])
            testevent=Interfacehuan.query.filter_by(url=self.urltest,status=False).first()
            if not testevent:
                self.log_can.error_log('用例：%s执行失败！测试环境不存在' % (self.id[case]))
                self.result_toal += 1
                self.result_fail += 1
                self.bask_list.append('用例：%s执行失败！测试环境不存在' % (self.id[case]) )
                self.result_pf.append('fail')
                self.spendlist.append('0')
                save_reslut(key=str(self.id[case])+'&',value='测试环境不存在')
                continue
            testcase = InterfaceTest.query.filter_by(id=self.id[case]).first()
            try:
                yuanlai = eval(self.parm[case])
            except Exception as e:
                self.log_can.error_log('用例：%s转化参数！原因：%s' % (self.id[case], e))
                self.result_toal += 1
                self.result_except += 1
                self.spendlist.append('0')
                self.bask_list.append('转化参数，%s' % e)
                self.result_pf.append('Exception')
                save_reslut(key=str(self.id[case]) + '&' + testevent.url, value='转换参数失败')
                continue
            mysql_result = []
            if testcase.pid != "None":
                try:
                    testret = TestcaseResult.query.filter_by(case_id=int(testcase.pid)).first()
                    data = testret.result
                    if data:
                        if data.by is False:
                            self.result_fail += 1
                            self.result_toal += 1
                            self.bask_list.append('依赖用例失败')
                            self.spendlist.append('0')
                            self.result_pf.append('fail')
                            save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str('依赖用例失败'))
                        else:
                            try:
                                huoqudata = eval(data)[testcase.getattr_p]
                                yuanlai.update({testcase.getattr_p: huoqudata})
                            except Exception as e:
                                self.spendlist.append('0')
                                self.log_can.error_log('用例：%s 提出依赖数据出错！原因：%s' % (self.id[case], e))
                                self.result_toal += 1
                                self.result_except += 1
                                self.bask_list.append('获取依赖的字段异常，%s' % e)
                                self.result_pf.append('Exception')
                                save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str('获取依赖的字段异常'))
                                continue
                    else:
                        self.log_can.info_log('用例：%s接口依赖结果没有保存!' % self.id[case])
                        self.result_toal += 1
                        self.result_wei += 1
                        self.bask_list.append('依赖的测试结果没有保存')
                        self.result_pf.append(u'Exception')
                        self.spendlist.append('0')
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                        continue
                except Exception as e:
                    self.log_can.error_log('用例：%s 测试出错了' % e)
                    self.result_toal += 1
                    self.result_wei += 1
                    self.bask_list.append('测试出错了，原因：%s' % e)
                    self.result_pf.append(u'error')
                    self.spendlist.append('0')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    continue
            if self.is_database[case] is True:
                if self.urltest is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.spendlist.append('0')
                    self.bask_list.append('None')
                    self.result_pf.append(u'测试环境不存在')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                if testcase.chaxunshujuku is None or testcase.databaseziduan is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.spendlist.append('0')
                    self.bask_list.append('None')
                    self.result_pf.append(u'用例找不到查询数据库或者断言参数')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                if self.urltest.database is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.spendlist.append('0')
                    self.bask_list.append('None')
                    self.result_pf.append(u'数据库没有配置！')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                if self.urltest.dbport is None or self.urltest.dbhost is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.spendlist.append('0')
                    self.bask_list.append('检查数据库的地址和端口！')
                    self.result_pf.append(u'检查数据库的地址和端口！')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                if self.urltest.databaseuser is None or self.urltest.databasepassword is None:
                    self.result_toal += 1
                    self.result_cashu += 1
                    self.spendlist.append('0')
                    self.bask_list.append('数据库登录账户没有找到')
                    self.result_pf.append(u'数据库登录账户没有找到')
                    save_reslut(key=str(self.id[case])+ '&' + testevent.url, value=str(apijson))
                conncts = cursemsql(host=self.urltest.dbhost, port=self.urltest.dbport,
                                    user=self.urltest.databaseuser,
                                    password=self.urltest.databasepassword,
                                    database=self.urltest.database)
                if conncts['code'] == 0:
                    self.result_toal += 1
                    self.result_except += 1
                    self.spendlist.append('0')
                    self.bask_list.append('链接数据库异常')
                    self.result_pf.append('Exception')
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                else:
                    result_myql = excemysql(conne=conncts['conne'], Sqlmy=self.data_mysql[case])
                    if result_myql['code'] == 0:
                        self.spendlist.append('0')
                        self.result_toal += 1
                        self.result_except += 1
                        self.bask_list.append(conncts['e'])
                        self.result_pf.append('Exception')
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    mysql_result = result_myql['result']
            else:
                try:
                    if testcase.rely_mock == True:
                        m_case = mockforcase.query.filter_by(case=testcase.id).first()
                        if not m_case:
                            testcase.Interface_is_tiaoshi = True
                            testcase.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            self.spendlist.append('0')
                            self.bask_list.append('None')
                            self.result_pf.append(u'找不到mock依赖的')
                        me = Mockserver.query.filter_by(id=m_case.mock, delete=False).first()
                        if not me:
                            testcase.Interface_is_tiaoshi = True
                            testcase.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            self.spendlist.append('0')
                            self.bask_list.append('None')
                            self.result_pf.append(u'mock不存在或者已删除')
                        try:
                            me = Api(url=me.path, fangshi=me.methods,
                                     params=eval(me.params), headers={'token': xitong_request_toke})
                            result = me.getJson()
                            da_ta = result[m_case.filed]
                            yuanlai[m_case.filed] = da_ta
                        except Exception as e:
                            case.Interface_is_tiaoshi = True
                            case.Interface_tiaoshi_shifou = True
                            db.session.commit()
                            self.spendlist.append('0')
                            self.bask_list.append('None')
                            self.result_pf.append(u'请求mock接口，失败原因：%s' % e)
                    api = Api(url=self.url[case], fangshi=self.meth[case], params=yuanlai,
                              headers=self.headers[case])
                    apijson = api.getJson()
                    spend=api.spend()
                    self.log_can.info_log(u'测试的:接口地址：%s,请求头：%s,参数:%s,实际返回:%s,预期:%s' % (
                        self.url[case], self.headers[case], self.parm[case], apijson, self.assert_test[case]))
                    come = assert_in(self.assert_test[case], apijson)
                    return_mysql = pare_result_mysql(mysqlresult=mysql_result, return_result=come,
                                                     paseziduan=self.data_ziduan[case])
                    if come == 'pass' and return_mysql['result'] == 'pass':
                        self.result_pass += 1
                        self.result_toal += 1
                        self.spendlist.append(spend)
                        self.bask_list.append(apijson)
                        self.result_pf.append('pass')
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    elif come == 'fail' or return_mysql['result'] == 'fail':
                        self.result_fail += 1
                        self.result_toal += 1
                        self.bask_list.append(apijson)
                        self.result_pf.append('fail')
                        self.spendlist.append(spend)
                        self.save_case_result(result=str(apijson), by=False, caseid=self.id[case], testevir=testevent,
                                              spend=spend)
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    elif come == '预期不存在':
                        self.result_toal += 1
                        self.result_cashu += 1
                        self.spendlist.append(spend)
                        self.bask_list.append(apijson)
                        self.result_pf.append(u'预期不存在')
                        self.save_case_result(result=str(apijson), by=False, caseid=self.id[case],testevir=testevent,spend=spend)
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    elif '异常' in come or return_mysql['code'] == 1:
                        self.result_toal += 1
                        self.spendlist.append(spend)
                        self.result_except += 1
                        self.bask_list.append((apijson, return_mysql['result']))
                        self.result_pf.append('Exception')
                        self.save_case_result(result=str(apijson), by=False, caseid=self.id[case],testevir=testevent,spend=spend)
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    else:
                        self.result_toal += 1
                        self.result_wei += 1
                        self.spendlist.append(spend)
                        self.bask_list.append(apijson)
                        self.result_pf.append(u'未知错误')
                        self.save_case_result(result=str(apijson), by=False, caseid=self.id[case],testevir=testevent,spend=spend)
                        save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                except Exception as e:
                    self.spendlist.append(0)
                    self.log_can.info_log('用例：%s执行失败!原因：%s' % (self.id[case], e))
                    self.result_toal += 1
                    self.result_except += 1
                    self.bask_list.append(e)
                    self.result_pf.append('Exception')
                    self.save_case_result(result=str(apijson), by=False, caseid=self.id[case],testevir=testevent,spend=spend)
                    save_reslut(key=str(self.id[case]) + '&' + testevent.url, value=str(apijson))
                    continue
        return self.result_toal, self.result_pass, self.result_fail, self.result_pf, self.bask_list, \
               self.result_cashu, self.result_wei, self.result_except,self.spendlist
    def save_case_result(self, result, caseid, by, testevir, spend=None):
        new_case = TestcaseResult(result=str(result), case_id=caseid, by=by, testevir=testevir, spend=spend)
        db.session.add(new_case)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            self.log_can.info_log('用例：%s保存测试结果失败!原因：%s' % (caseid, e))