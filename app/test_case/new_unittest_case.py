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
            save_reslut(key=str(self.parm['id']) + '&', value='测试环境不存在')
        self.baseurl = self.testevent.url
        self.testcase = InterfaceTest.query.filter_by(id=self.parm['id'].id,
                                                      status=False).first()
        if self.testcase is None:
            self.is_run = False
            self.fail_log = "测试用例不存在"
            logger.info("测试用例不存在")
            save_reslut(key=str(self.parm['id']) + '&', value='测试用例不存在')
        try:
            self.parame = eval(self.testcase.Interface_pase)
        except Exception as e:
            logger.exception(e)
            self.is_run = False
            self.fail_log = "测试用例参数转化失败"
            logger.info("测试用例参数转化失败")
            save_reslut(key=str(self.parm['id']) + '&', value='测试用例参数转化失败')
        self.interface_url = self.testevent.url+self.testcase.interfaces.Interface_url
        try:
            self.headers = eval(self.testcase.Interface_headers)
        except Exception as e:
            logger.exception(e)
            self.is_run = False
            logger.info("测试用例headers转化失败")
            self.fail_log = "测试用例headers转化失败"
            save_reslut(key=str(self.parm['id']) + '&', value='测试用例headers转化失败')

    def tearDown(self) -> None:

        pass

    def testcase(self):
        if self.is_run is True:
            ##todo
            ##1.接口依赖未实现
            ##2.数据库查询未实现
            api = Api(url=self.interface_url,
                      method=self.testcase.Interface_meth,
                      params=self.parame,
                      headers=self.headers)
            apijson = api.getJson()

            spend = api.spend()
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
            self.assertEqual(value1, value2, msg="断言与预期不符合")
            save_reslut(key=str(self.parm['id']) + '&' + self.interface_url, value=str(apijson))
        else:
            self.assertTrue(False, msg=self.fail_log)
