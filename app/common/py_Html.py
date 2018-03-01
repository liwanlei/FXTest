# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: py_Html.py
@time: 2017/6/5 17:04
"""
import  os
# import sys  
# reload(sys)  
# sys.setdefaultencoding('utf8') 
titles=u'接口测试'
def title(titles):
    title='''<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>%s</title>
		<style type="text/css">
			td{ width:40px; height:50px;}
		</style>
	</head>
	<body>
	'''%(titles)
    return title
connent=u'''
<div style='width: 1170px;margin-left: 15%'>
<h1>FXTest 测试平台接口测试的结果</h1>'''
def time(starttime,endtime,passge,fail,excepts,yuqi,weizhi):
    beijing=u'''
		<p><strong>开始时间:</strong> %s</p>
		<p><strong>结束时间:</strong> %s</p>
		<p><strong>耗时:</strong> %s</p>
		<p><strong>结果:</strong>
			<span >通过: <strong >%s</strong>
			失败: <strong >%s</strong>
			Exception: <strong >%s</strong>
			预期不存在: <strong >%s</strong>
			未知错误: <strong >%s</strong>
			        </span></p>                  
			    <p ><strong>测试详情如下</strong></p>  </div> '''%\
            (starttime,endtime,(endtime-starttime),passge,fail,excepts,yuqi,weizhi)
    return beijing
shanghai=u'''


        <p>&nbsp;</p>
        <table border='2'cellspacing='1' cellpadding='1' width='70%'align="center" >
		<tr >
            <td ><strong>用例ID&nbsp;</strong></td>
            <td><strong>项目</strong></td>
            <td><strong>url</strong></td>
            <td><strong>请求方式</strong></td>
            <td><strong>参数</strong></td>
            <td><strong>headers</strong></td>
            <td><strong>预期</strong></td>
            <td><strong>实际返回</strong></td>  
            <td><strong>结果</strong></td>
        </tr>
    '''
def passfail(tend):
    if tend =='pass':
        htl=' <td bgcolor="green">pass</td>'
    elif tend =='fail':
        htl=' <td bgcolor="fail">fail</td>'
    elif tend=='Exception':
        htl='<td bgcolor="#8b0000">Exception</td>'
    elif tend=='预期不存在':
        htl = '<td bgcolor="#8b0000">预期不存在</td>'
    elif tend=='未知错误':
        htl = '<td bgcolor="#8b0000">未知错误</td>'
    else:
        htl = '<td bgcolor="#8b0000">请查看日志</td>'
    return htl
def ceshixiangqing(id,name,coneent,url,meth,yuqi,json,relust,headers):
    xiangqing='''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
        </tr>
        
    '''%(id,name,coneent,url,meth,headers,yuqi,json,(passfail(relust)))
    return xiangqing
weibu='''
	</table>
    </body>
    </html>'''
def relust(titles,starttime,endtime,passge,fail,id,name,headers,coneent,url,meth,yuqi,json,relust,excepts,yuqis,weizhi):
    if type(name) is list:
        relus=' '
        for i in range(len(name)):
            relus+=(ceshixiangqing(id[i],name[i],coneent=coneent[i],url=url[i],headers=headers[i],meth=meth[i],yuqi=yuqi[i],json=json[i],relust=relust[i]))
        text=title(titles)+connent+time(starttime,endtime,passge,fail,excepts,yuqis,weizhi)+shanghai+relus+weibu
    else:
        text=title(titles)+connent+time(starttime,endtime,passge,fail,excepts,yuqis,weizhi)+shanghai+ceshixiangqing(id=id,name=name,headers=headers,coneent=coneent,url=url,meth=meth,yuqi=int(yuqi),json=json,relust=relust)+weibu
    return text
def createHtml(filepath,titles,starttime,endtime,passge,fail,id,name,headers,coneent,url,meth,yuqi,json,relusts,excepts,yuqis,weizhi):
    texts=relust(titles=titles,starttime=starttime,endtime=endtime,passge=passge,fail=fail,id=id,name=name,headers=headers,coneent=coneent,
                 url=url,meth=meth,yuqi=yuqi,json=json,relust=relusts,excepts=excepts,yuqis=yuqis,weizhi=weizhi)
    with open(filepath,'wb') as f:
        f.write(texts.encode())
