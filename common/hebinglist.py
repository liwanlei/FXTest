""" 
@author: lileilei
@file: hebinglist.py 
@time: 2018/1/29 13:55 
"""
"""list的合并"""
def hebinglist(list1):
    new=[]
    for m in list1:
        for h in m:
            new.append(h)
    return new