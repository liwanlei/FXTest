# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:34:12
# @Author  : lileilei
'''字典比较判断'''
def comp_dict(dict1,dict2):
    try:
        for k,v in dict1.items():
            for k2,v2 in dict2.items():
                if k==k2 and v==v2:
                    return True
                else:
                    return False
    except:
        return False
'''
断言封装,断言切割根据&切割
'''
def assert_in(asserqiwang,fanhuijson):
    if len(asserqiwang.split('=')) > 1:
        try:
            data = asserqiwang.split('&')
            result = dict([(item.split('=')) for item in data])
            value1=([(str(fanhuijson[key])) for key in result.keys()])
            value2=([(str(value)) for value in result.values()])
            if value1==value2:
                return  'pass'
            else:
                return 'fail'
        except Exception as e:
            return '异常！原因：%s'%e
    else:
        return '预期不存在'
def dict_par(doct1,dict2):
    h=[]
    l=[]
    for k, v in doct1.items():
        h.append(k)
    for k2,v2 in dict2.items():
        l.append(k2)
    if h==l:
        return True
    else:
        return False