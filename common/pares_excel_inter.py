# -*- coding: utf-8 -*-
# @Date    : 2017-07-18 13:26:17
# @Author  : lileilei 
import xlrd
def pasre_inter(filename):
	file=xlrd.open_workbook(filename)
	me=file.sheets()[0]
	nrow=me.nrows
	ncol=me.ncols
	project_name=[]
	model_name=[]
	interface_name=[]
	interface_url=[]
	interface_meth=[]
	interface_par=[]
	interface_bas=[]
	for i in range(1,nrows):
		project_name.append(me.cell(i,0).value)
		model_name.append(me.cell(i,1).value)


