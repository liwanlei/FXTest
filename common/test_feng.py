# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 15:13:25
# @Author  : lileilei
'''
requets模块的简单的封装
'''
import requests,json
class reques():
    def get(self, url,headers,parms):#get消息
        try:
            r = requests.get(url, headers=headers,params=parms)
            r.encoding = 'UTF-8'
            spend=r.elapsed.total_seconds()
            json_response = json.loads(r.text)
            return json_response,spend
        except Exception as e:
            return {'get请求出错':"错误原因:%s"%e}
    def post(self, url, params,headers):#post消息
        data = json.dumps(params)
        try:
            r =requests.post(url,params=data,headers=headers)
            json_response = json.loads(r.text)
            spend=r.elapsed.total_seconds()
            return json_response,spend
        except Exception as e:
            return {'post请求出错': "错误原因:%s" % e}
    def delfile(self,url,params,headers):#删除的请求
        try:
            del_word=requests.delete(url,data=params,headers=headers)
            json_response=json.loads(del_word.text)
            spend=del_word.elapsed.total_seconds()
            return json_response,spend
        except Exception as e:
            return {'del请求出错': "错误原因:%s" % e}
    def putfile(self,url,params,headers):#put请求
        try:
            data=json.dumps(params)
            me=requests.put(url,data,headers=headers)
            json_response=json.loads(me.text)
            spend=me.elapsed.total_seconds()
            return json_response,spend
        except Exception as e:
            return {'put请求出错': "错误原因:%s" % e}