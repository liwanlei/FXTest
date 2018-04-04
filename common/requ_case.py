# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 13:07:22
# @Author  : lileilei
'''
接口请求封装后的使用模块
'''
from common.test_feng import reques
requ=reques()
response=[]
class Api():
	def __init__(self,url,fangshi,params,headers):
		self.url=url
		self.fangsh=fangshi
		self.param=params
		self.headers=headers
	def testapi(self):
		global response
		if self.fangsh=='POST' or self.fangsh=='post':
			response=requ.post(url=self.url,params=self.param,headers=self.headers)
		elif self.fangsh=='GET' or self.fangsh=='get':
			response=requ.get(url=self.url,headers=self.headers,parms=self.param)
		elif self.fangsh=='PUT' or self.fangsh=='put':
			response=requ.putfile(url=self.url,params=self.param,headers=self.headers)
		elif self.fangsh=='DELETE' or self.fangsh=='delete':
			response=requ.delfile(url=self.url,params=self.param,headers=self.headers)
		return  response
	def getJson(self):
		json_data=self.testapi()
		return json_data
	def getCode(self):
		return self.testapi().status_code