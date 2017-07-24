# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 13:07:22
# @Author  : lileilei 
import requests,json
from app.common.test_feng import reques
requ=reques()
liwanlei=[]
class Api():
	def __init__(self,url,fangshi,params):
		self.url=url
		self.fangsh=fangshi
		self.param=params
	def testapi(self):
		global liwanlei
		if self.fangsh=='POST' or self.fangsh=='post':
			liwanlei=requ.post(self.url,self.param)
		elif self.fangsh=='GET' or self.fangsh=='get':
			liwanlei=requ.get(self.url)
		elif self.fangsh=='PUT' or self.fangsh=='put':
			liwanlei=requ.putfile(self.url,self.param)
		elif self.fangsh=='DELETE' or self.fangsh=='delete':
			liwanlei=requ.delfile(self.url,self.param)
		return  liwanlei
	# def getcode(self):
	# 	print(self.testapi())
	# 	code=self.testapi()['error_code']
	# 	return code
	def getJson(self):
		json_data=self.testapi()
		return json_data
