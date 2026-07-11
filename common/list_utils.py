""" 
@author: lileilei
@file: list_utils.py
@time: 2018/1/29 13:55 
"""
"""
list的合并
"""


def flatten_list(list1: list):
    new = []
    for m in list1:
        for h in m:
            new.append(h)
    return new


def list_stats(list2: list):
    list_int = []
    for i in list2:
        try:
            list_int.append(float(i))
        except Exception:
            list_int.append(0)
    nsm = 0
    for j in range(len(list_int)):
        nsm += float(list_int[j])
    ma = max(list_int)
    minx = min(list_int)
    pingjun = nsm / (len(list_int))
    return ma, minx, pingjun

# 向后兼容别名
hebinglist = flatten_list
listmax = list_stats
