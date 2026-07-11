# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:34:12
# @Author  : lileilei
"""字典比较、合并与取值工具。"""
from ast import literal_eval


def comp_dict(dict1, dict2):
    try:
        for k, v in dict1.items():
            for k2, v2 in dict2.items():
                if k == k2 and v == v2:
                    return True
                else:
                    return False
    except Exception:
        return False


def compare_dict_keys(doct1, dict2):
    """比较两个字典的键是否一致。"""
    h = []
    l = []
    for k, v in doct1.items():
        h.append(k)
    for key, value in dict2.items():
        l.append(key)
    if h == l:
        return True
    else:
        return False


def merge_dict(dict_list: dict):
    """合并多个字典（字符串形式）为一个字典。"""
    dictMerged = {}
    for item in dict_list:
        try:
            dictMerged.update(literal_eval(item))
        except Exception:
            pass
    return dictMerged


def get_dict_value(d, code):
    """递归地从嵌套字典/列表中取出指定 key 的所有值。"""
    result = []
    if isinstance(d, dict) and code in d.keys():
        value = d[code]
        result.append(value)
        return result
    elif isinstance(d, (list, tuple)):
        for item in d:
            value = get_dict_value(item, code)
            if value == "None" or value is None:
                pass
            elif len(value) == 0:
                pass
            else:
                result.append(value)
        return result
    else:
        if isinstance(d, dict):
            for k in d:
                value = get_dict_value(d[k], code)
                if value == "None" or value is None:
                    pass
                elif len(value) == 0:
                    pass
                else:
                    for item in value:
                        result.append(item)
            return result


# 向后兼容别名
dict_par = compare_dict_keys
mergeDict = merge_dict
getdictvalue = get_dict_value
