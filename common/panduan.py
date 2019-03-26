# -*- coding: utf-8 -*-
# @Date    : 2017-08-02 21:54:08
# @Author  : lileilei
'''
判断
'''
from  common.fengzhuang_dict import getdictvalue
def assert_in(asserqiwang,fanhuijson):
    if len(asserqiwang.split('=')) > 1:
        data = asserqiwang.split('&')
        result = dict([(item.split('=')) for item in data])
        try:
            value1=[(str(getdictvalue(fanhuijson,key)[0])) for key in result.keys()]
            value2=[(str(value)) for value in result.values()]
            if value1==value2:
                return  'pass'
            else:
                return 'fail'
        except :
            return 'exception '
    else:
        return '请检查断言'
def assertre(asserqingwang):
    if len(asserqingwang.split('=')) > 1:
        data = asserqingwang.split('&')
        result = dict([(item.split('=')) for item in data])
        return result
    else:
        return u'请填写期望值'
def pare_result_mysql(mysqlresult,paseziduan,return_result):
    mysql_list=[]
    for i in mysqlresult:
        mysql_list.append(i)
    test_result=[]
    ziduanlist=[]
    if paseziduan is None:
        return {'code':0,'result':'pass'}
    try:
        for ziduan in paseziduan:
            ziduanlist.append(ziduan[0].split(','))
    except Exception as e:
        return {'code':1,'result':e}
    try:
        for ziduan in ziduanlist:
            test_result.append(return_result[ziduan])
    except Exception as e:
        return {'code': 1, 'result': e}
    if test_result==mysql_list:
        return {'code': 2, 'result': 'pass'}
    else:
        return {'code': 3, 'result': 'fail'}