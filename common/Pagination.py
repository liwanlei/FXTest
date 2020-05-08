""" 
@author: lileilei
@file: Pagination.py
@time: 2018/4/28 9:47 
"""
'''
分页
'''


def fenye_list(Ob_list: list, split: int):
    New_list = []
    if len(Ob_list) <= split:
        New_list.append(Ob_list)
    else:
        me = len(Ob_list) // split
        for i in range(me):
            New_list.append(Ob_list[(i) * split:(i + 1) * split])
        if len(Ob_list[me * split:]) > 0:
            New_list.append(Ob_list[me * split:])
    return New_list
