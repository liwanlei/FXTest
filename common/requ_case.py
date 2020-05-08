# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 13:07:22
# @Author  : lileilei
'''
接口请求封装后的使用模块
调用类，传入url，请求方法，参数，请求headers，就可以进行请求，
目前只支持dict格式的参数，和请求headers。
'''
from common.PackageRequest import reques


class Api():
    def __init__(self, url, fangshi, params, headers):
        self.url = url
        self.fangsh = fangshi
        self.param = params
        self.headers = headers
        self.requ = reques()
        self.response = []

    def testapi(self):
        global response, spend
        if self.fangsh == 'POST' or self.fangsh == 'post':
            response, spend = self.requ.post(url=self.url, params=self.param, headers=self.headers)
        elif self.fangsh == 'GET' or self.fangsh == 'get':
            response, spend = self.requ.get(url=self.url, headers=self.headers, parms=self.param)
        elif self.fangsh == 'PUT' or self.fangsh == 'put':
            response, spend = self.requ.putfile(url=self.url, params=self.param, headers=self.headers)
        elif self.fangsh == 'DELETE' or self.fangsh == 'delete':
            response, spend = self.requ.delfile(url=self.url, params=self.param, headers=self.headers)
        return response, spend

    def getJson(self):
        json_data, spend = self.testapi()
        return json_data

    def spend(self):
        json_data, spend = self.testapi()
        return spend
