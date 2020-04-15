""" 
@author: lileilei
@file: python_dict.py 
@time: 2018/6/15 13:54 
"""
'''
解析字典的最新封装，可以解决大部分字典类型的数据的读取
'''
def getdictvalue(d,code):
    result=[]
    if isinstance(d, dict) and code in d.keys():
        value = d[code]
        result.append(value)
        return result
    elif isinstance(d, (list, tuple)):
            for item in d:
                value=getdictvalue(item,code)
                if value =="None" or value is None:
                    pass
                elif len(value)==0:
                    pass
                else:
                    result.append(value)
            return result
    else:
        if isinstance(d, dict):
            for k in d:
                value=getdictvalue(d[k], code)
                if value =="None" or value is None :
                    pass
                elif len(value)==0:
                    pass
                else:
                    for item in value:
                        result.append(item)
            return result