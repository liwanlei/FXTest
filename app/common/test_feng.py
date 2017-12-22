# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 15:13:25
# @Author  : lileilei 
import requests,json
class reques():
    def get(self, url,headers,parms):#get消息
        try:
            r = requests.get(url, headers=headers,params=parms)
            r.encoding = 'UTF-8'
            json_response = json.loads(r.text)
            return json_response
        except Exception as e:
            return {'get请求出错':"错误原因:%s"%e}
    def post(self, url, params,headers):#post消息
        data = json.dumps(params)
        try:
            r =requests.post(url,params=params,headers=headers)
            json_response = json.loads(r.text)
            return json_response
        except Exception as e:
            return {'post请求出错': "错误原因:%s" % e}
    def delfile(self,url,params,headers):#删除的请求
        try:
            del_word=requests.delete(url,params,headers=headers)
            json_response=json.loads(del_word.text)
            return json_response
        except Exception as e:
            return {'del请求出错': "错误原因:%s" % e}
    def putfile(self,url,params,headers):#put请求
        try:
            data=json.dumps(params)
            me=requests.put(url,data,headers=headers)
            json_response=json.loads(me.text)
            return json_response
        except Exception as e:
            return {'put请求出错': "错误原因:%s" % e}
