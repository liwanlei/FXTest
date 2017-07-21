# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 21:34:12
# @Author  : lileilei
def comp_dict(dict1,dict2):
    for k,v in dict1.items():
        for k2,v2 in dict2.items():
            if k==k2 and v==v2:
                return True
            else:
                return False
                