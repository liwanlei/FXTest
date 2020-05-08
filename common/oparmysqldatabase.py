""" 
@author: lileilei
@file: oparmysqldatabase.py
@time: 2018/3/9 15:46 
"""
"""
接口用例测试查询测试数据库测试结果对比，
现在支持查询mysql，进行对比
"""
from pymysql import *

'''链接数据库，code为1即链接成功，error为错误信息，conne为返回的链接的实例'''


def cursemsql(host, port, user, password, database):
    try:
        conne = connect(host=host, port=port, user=user, password=password, db=database)
        return {'code': 1, 'conne': conne}
    except Exception as e:
        return {'code': 0, 'error': e}


'''执行数据库的sql，code为1即执行sql成功，result为返回结果'''


def excemysql(conne, Sqlmy):
    try:
        with conne.cursor() as conn:
            conn.execute(Sqlmy)
            result = conn.fetchall()
        return {'code': 1, 'result': result}
    except Exception as e:
        return {'code': 0, 'error': e}
