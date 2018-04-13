""" 
@author: lileilei
@file: ddd.py 
@time: 2018/4/13 13:24 
"""
'''字典的合并'''
def hebingDict(dict_list:list):
    dictMerged ={}
    for item in dict_list:
        try:
            dictMerged.update(eval(item))
        except:
            continue
    return dictMerged