""" 
@author: lileilei
@file: mergelist.py
@time: 2018/1/29 13:55 
"""
"""
list的合并
"""


def hebinglist(list1: list):
    new = []
    for m in list1:
        for h in m:
            new.append(h)
    return new


def listmax(list2: list):
    list_int = []
    for i in list2:
        try:
            list_int.append(float(i))
        except:
            list_int.append(0)
    nsm = 0
    for j in range(len(list_int)):
        nsm += float(list_int[j])
    ma = max(list_int)
    minx = min(list_int)
    pingjun = nsm / (len(list_int))
    return ma, minx, pingjun
