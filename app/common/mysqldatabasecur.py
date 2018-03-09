""" 
@author: lileilei
@file: mysqldatabasecur.py 
@time: 2018/3/9 15:46 
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
            result=conn.execute(Sqlmy).fetchone()
        return {'code':1,'result':result}
    except Exception as e:
        return {'code':0,'error':e}
