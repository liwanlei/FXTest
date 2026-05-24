""" 
@author: lileilei
@file: ddd.py 
@time: 2018/4/13 13:24 
"""
'''
字典的合并
'''
from ast import literal_eval


def mergeDict(dict_list: dict):
    dictMerged = {}
    for item in dict_list:
        try:
            dictMerged.update(literal_eval(item))
        except Exception as e:
            pass
    return dictMerged
