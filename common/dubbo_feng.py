""" 
@author: lileilei
@file: dubbo_feng.py 
@time: 2018/3/29 12:26 
"""
from  pyhessian.client import  HessianProxy
from  pyhessian import protocol
class DubboInterface:
    def __init__(self,url,interface,method,param,**kwargs):
        self.url=url
        self.interface=interface
        self.method=method
        self.param=param
        self.interfaceparam=protocol.object_factory(self.param,**kwargs)
    def getresult(self):
        try:
            result=HessianProxy(self.url+self.interface)
            return_result=getattr(result,self.method)(self.interfaceparam)
            res={'code':0,'result':return_result}
        except Exception as e:
            res={'code':1,'result':e}
        return  res