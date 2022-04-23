'''
  @Description      
  @auther         leizi
'''

import unittest

from common.requ_case import Api
from common.judgment import pare_result_mysql
from common.oparmysqldatabase import *
from config import redis_host, redis_port, \
    redis_save_result_db, save_duration
from app.models import *
from common.packageredis import ConRedisOper
from common.caselog import filelogpath
from common.packeagedictry import getdictvalue


def save_reslut(key, value):
    m = ConRedisOper(host=redis_host, port=redis_port,
                     db=redis_save_result_db)
    m.sethash(key, value, save_duration)


def get_reslut(key):
    m = ConRedisOper(host=redis_host, port=redis_port,
                     db=redis_save_result_db)
    reslit = m.getset(key)
    return reslit


class Parmer(unittest.TestCase):
    '''
    根据入参进行拆分
    '''

    def __init__(self, methodName='runTest', parme=None):
        super(Parmer, self).__init__(methodName)
        self.parme = parme

    @classmethod
    def parametrize(cls, testcase_klass, parame):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            for param in parame:
                suite.addTest(testcase_klass(methodName=name, parm=param))
        return suite


def save_case_result(result, caseid, by, testevent, spend=None):
    '''
    保存测试结果
    :param result:  结果
    :param caseid: 测试用例id
    :param by:  通过
    :param testevent: 测试环境
    :param spend:  耗时
    :return:
    '''
    new_case = TestcaseResult(result=str(result),
                              case_id=caseid,
                              by=by, testevir=testevent, spend=spend)
    db.session.add(new_case)
    try:
        db.session.commit()
    except Exception as e:
        logger.exception(e)
        db.session.rollback()


class TestCase(Parmer):
    def __init__(self, parm, methodName='runTest'):
        super(TestCase, self).__init__(methodName)
        self.parm = parm
        self.is_run = True
        filelogpath(self.parm['caselog'])
        logger.info("caselog完成初始化")
        self.fail_log = ''

    def setUp(self) -> None:
        logger.info("{}测试用例开始执行".format(str(self.parm['id'])))
        logger.info("{} 用例开始查询测试环境是否存在".format(str(self.parm['id'])))

        self.url = self.parm['testevent'].url
        self.testevent = Interfacehuan.query.filter_by(url=str(self.url)).first()
        if self.testevent is None:
            self.is_run = False
            logger.info("测试环境不存在")
            self.fail_log = "测试环境不存在"
            save_reslut(key=str(self.parm['id']) + '&'+ self.testevent.url, value='测试环境不存在')
        self.baseurl = self.testevent.url
        self.testcase = InterfaceTest.query.filter_by(id=self.parm['id'].id,
                                                      status=False).first()
        if self.testcase is None:
            self.is_run = False
            self.fail_log = "测试用例不存在"
            logger.info("测试用例不存在")
            save_reslut(key=str(self.parm['id']) + '&'+ self.testevent.url, value='测试用例不存在')
        try:
            self.parame = eval(self.testcase.Interface_pase)
        except Exception as e:
            logger.exception(e)
            self.is_run = False
            self.fail_log = "测试用例参数转化失败"
            logger.info("测试用例参数转化失败")
            save_reslut(key=str(self.parm['id']) + '&'+ self.testevent.url, value='测试用例参数转化失败')
        self.interface_url = self.testevent.url+self.testcase.interfaces.Interface_url
        try:
            self.headers = eval(self.testcase.Interface_headers)
        except Exception as e:
            logger.exception(e)
            self.is_run = False
            logger.info("测试用例headers转化失败")
            self.fail_log = "测试用例headers转化失败"
            save_reslut(key=str(self.parm['id']) + '&'+ self.testevent.url, value='测试用例headers转化失败')
        if self.testcase.pid !="" or self.testcase.pid is not None:
            logger.info("测试用例获取以来case数据")
            testrepycase = TestcaseResult.query.filter_by(case_id=int(self.testcase.pid)).first()
            if testrepycase is not None:
                if testrepycase.by is False:
                    logger.info("依赖的测试用例未通过")
                    self.fail_log = "依赖的测试用例未通过"
                    self.is_run = False
                    save_reslut(key=str(self.parm['id']) +  '&' + self.testevent.url, value=str('依赖用例失败'))
                else:
                    try:
                        replydata = eval(testrepycase.result)[self.testcase.getattr_p]
                        self.parame.update({self.testcase.getattr_p: replydata})
                    except Exception as e:
                        logger.exception(e)
                        logger.info("以来用例获取以来字段失败")
                        self.fail_log = "以来用例获取以来字段失败"
                        self.is_run = False

            else:
                logger.info("依赖的测试用例未执行")
                self.fail_log = "依赖的测试用例未执行"
                self.is_run = False

    def tearDown(self) -> None:

        pass

    def testcase(self):
        if self.is_run is True:
            api = Api(url=self.interface_url,
                      method=self.testcase.Interface_meth,
                      params=self.parame,
                      headers=self.headers)
            apijson = api.getJson()
            spend = api.spend()

            if self.testcase.is_database is True:
                if self.testcase.chaxunshujuku is None or self.testcase.databaseziduan is None:
                    logger.error("测试用例查询数据库不存在")
                if self.testevent.database is None:
                    logger.info("数据库没有配置")
                if self.testevent.dbport is None or self.testevent.dbhost is None:
                    logger.info("检查数据库的地址和端口！")
                if self.testevent.databaseuser is None or self.testevent.databasepassword is None:
                    logger.info("数据库登录账户没有找到")
                else:
                    conncts = cursemsql(host=self.testevent.dbhost,
                                        port=self.testevent.dbport,
                                        user=self.testevent.databaseuser,
                                        password=self.testevent.databasepassword,
                                        database=self.testevent.database)
                    if conncts['code'] == 0:
                        logger.info("连接数据库异常")
                    else:
                        result_myql = excemysql(conne=conncts['conne'], Sqlmy=self.testcase.chaxunshujuku)
                        mysql_result = result_myql['result']
                        return_mysql = pare_result_mysql(mysqlresult=mysql_result,
                                                         return_result=apijson,
                                                         paseziduan=self.testcase.databaseziduan)
                        self.assertEqual(return_mysql['result'],"pass",msg=return_mysql['result'])

            logger.info(u'测试的:接口地址：%s,请求头：%s,参数:%s,实际返回:%s,预期:%s' % (
                self.interface_url, self.headers, self.parame,
                apijson, self.testcase.Interface_assert))
            data = self.testcase.Interface_assert.split('&')
            result = dict([(item.split('=')) for item in data])
            logger.info(result)
            value1 = [(str(getdictvalue(apijson, key)[0])) for key in result.keys()]
            logger.info(value1)
            value2 = [(str(value)) for value in result.values()]
            logger.info(value2)
            save_reslut(key=str(self.parm['id']) + '&' + self.interface_url, value=str(apijson))
            self.assertEqual(value1, value2, msg="断言与预期不符合")
        else:
            self.assertTrue(False, msg=self.fail_log)
