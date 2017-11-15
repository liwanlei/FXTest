# -*- coding: utf-8 -*-
# @Time    : 2017/6/4 20:35
# @Author  : lileilei
# @File    : makedata.py
from app.common.log  import LOG,logger
@logger('生成数据驱动所用数据')
def makedata(listid, listkey, listconeent, listurl, listfangshi, listqiwang, listname):
    i=0
    make_data=[]
    for i in range(len(listid)):
        make_data.append({'url':listurl[i],'key':listkey[i],'coneent':listconeent[i],'fangshi':listfangshi[i],'qiwang':listqiwang[i]})
        i+=1
    return make_data


