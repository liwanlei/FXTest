""" 
@author: lileilei
@file: mysqldatabasecur.py 
@time: 2018/3/9 15:46 
"""
"""接口用例测试查询测试数据库测试结果对比，
现在支持的是mysql查询数据库进行对比
"""
from pymysql import *
def cursemsql(host,port,user,password,database):
    try:
        conne = connect(host=host, port=port, user=user, password=password, db=database)
        return {'code':1,'conne':conne}
    except Exception as e:
        return {'code':0,'error':e}
def excemysql(conne,Sqlmy):
    try:
        with conne.cursor() as conn:
            conn.execute(Sqlmy)
            result=conn.fetchall()
        return {'code':1,'result':result}
    except Exception as e:
        return {'code':0,'error':e}