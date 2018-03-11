# -*- coding: utf-8 -*-
# @Date    : 2017-07-18 13:26:17
# @Author  : lileilei
'''这里为导入测试用例的地方'''
import xlrd
def pasre_inter(filename):
	file=xlrd.open_workbook(filename)
	me=file.sheets()[0]
	nrows=me.nrows
	ncol=me.ncols
	project_name=[]
	model_name=[]
	interface_name=[]
	interface_url=[]
	interface_meth=[]
	interface_par=[]
	interface_header=[]
	interface_bas=[]
	jiekou_bianhao=[]
	for i in range(2,nrows):
		jiekou_bianhao.append(me.cell(i,0).value)
		project_name.append(me.cell(i,2).value)
		model_name.append(me.cell(i,3).value)
		interface_name.append(me.cell(i,1).value)
		interface_url.append(me.cell(i,4).value)
		interface_header.append(me.cell(i,5).value)
		interface_meth.append(me.cell(i,6).value)
		interface_par.append(me.cell(i,7).value)
		interface_bas.append(me.cell(i,8).value)
		i+=1
	return jiekou_bianhao,interface_name,project_name,model_name,interface_url,interface_header,interface_meth,interface_par,interface_bas
