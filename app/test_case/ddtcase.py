""" 
@author: lileilei
@license: Apache Licence  
@file: ddtcase.py 
@time: 2017/12/22 17:12 
"""
import ddt,unittest
from  app.common.panduan import assertre
from app.common.requ_case import Api
from app.common.lognew import logger,LOG

class Mytest(unittest.TestCase):
    def setUp(self):
        LOG.info('测试用例开始执行')
    def tearDown(self):
        LOG.info('测试用例执行完毕')
    @ddt.data()
    def testapi(self):
        api=Api()
        apijson=api.getJson()
        LOG.info('返回结果:%s' % apijson)
