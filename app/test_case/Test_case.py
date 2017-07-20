# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:06:16
# @Author  : lileilei
from common.requ_case import Api
import os,time,datetime 
from common.py_Html import createHtml
from common.log import log_t
from common.dict_com import comp_dict
class ApiTestCase():
    def __init__(self,inteface_url,inteface_meth,inteface_parm,inteface_assert,file):
        self.result_pass=0
        self.result_fail=0
        self.result_toal=0
        self.url=inteface_url
        self.meth=inteface_meth
        self.parm=inteface_parm
        self.assert_test=inteface_assert
        self.bask_list=[]
        self.title = '测试日志'
        self.log_can = log_t(self.title, filename=file)
    def testapi(self):
        for case in range(len(self.url)):
            api=Api(url=self.url[case],fangshi=self.meth[case],params=self.parm[case])
            apijson=api.getJson
            apicode=api.getcode
            self.log_can.info_log('input:接口地址：%s,参数:%s,实际返回:%s,预期:%s'%(self.url[case],self.parm[case],apijson,self.assert_test[case]))
            if apicode!=200:
                self.result_fail+=1
                self.result_toal+=1
                self.bask_list.append(apijson)
                come=comp_dict(apijson,eval(self.assert_test[case]))
                if come== 'True':
                    self.result_pass+=1
                    self.result_toal+=1
                else:
                    self.result_fail+=1
                    self.result_toal+=1
        return self.result_toal ,self.result_pass,self.result_fail





