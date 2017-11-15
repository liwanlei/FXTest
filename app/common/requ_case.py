# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 13:07:22
# @Author  : lileilei 
import requests,json
from app.common.test_feng import reques
requ=reques()
liwanlei=[]
class Api():
	def __init__(self,url,fangshi,params,headers):
		self.url=url
		self.fangsh=fangshi
		self.param=params
		self.headers=headers
	def testapi(self):
		global liwanlei
		if self.fangsh=='POST' or self.fangsh=='post':
			liwanlei=requ.post(url=self.url,params=self.param,headers=self.headers)
		elif self.fangsh=='GET' or self.fangsh=='get':
			liwanlei=requ.get(url=self.url,headers=self.headers,parms=self.param)
		elif self.fangsh=='PUT' or self.fangsh=='put':
			liwanlei=requ.putfile(url=self.url,params=self.param,headers=self.headers)
		elif self.fangsh=='DELETE' or self.fangsh=='delete':
			liwanlei=requ.delfile(url=self.url,params=self.param,headers=self.headers)
		return  liwanlei
	
	def getJson(self):
		json_data=self.testapi()
		return json_data
