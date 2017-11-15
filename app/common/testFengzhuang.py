# -*- coding: utf-8 -*-
# @Time    : 2017/6/4 20:36
# @Author  : lileilei
# @File    : testFengzhuang.py
from app.common.test_requests import requ
reques=requ()
class TestApi(object):
	def __init__(self,url,headers,connent,fangshi):
		self.url=url
		self.headers=headers
		self.connent=connent
		self.fangshi=fangshi
	def testapi(self):
		if self.fangshi=='POST':
			self.parem = { 'info': self.connent}
			response=reques.post(self.url,self.parem,headers=self.headers)
		elif self.fangshi=="GET":
			self.parem = {'info': self.connent}
			response = reques.get(self.url,self.parem,headers=self.headers)
		return response
	def getcode(self):
		code=self.testapi()['code']
		return code
	def getJson(self):
		json_data = self.testapi()
		return json_data
