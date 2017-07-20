# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 13:07:22
# @Author  : lileilei 
import requests,json
from common.test_case import reques
requ=reques()
liwanlei=[]
class Api():
	def __init__(self,url,fangshi,params):
		self.url=url
		self.fangsh=fangshi
		self.param=params
	def testapi(self):
		global liwanlei
		if self.fangsh=='POST':
			liwanlei=requ.post(self.url,self.param)
		elif self.fangsh=='GET':
			liwanlei=requ.get(self.url)
		return  liwanlei
	def getcode(self):
		code=self.testapi()['code']
		return code
	def getJson(self):
		json_data=self.testapi()
		return json_data
