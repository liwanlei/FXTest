# -*- coding: utf-8 -*-
# @Date    : 2017-07-18 13:26:17
# @Author  : lileilei
'''
导入测试接口等封装
'''
import xlrd
def pasre_inter(filename):#导入接口
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
	interface_type=[]
	for i in range(2,nrows):
		jiekou_bianhao.append(me.cell(i,0).value)
		project_name.append(me.cell(i,2).value)
		model_name.append(me.cell(i,3).value)
		interface_name.append(me.cell(i,1).value)
		interface_url.append(me.cell(i,4).value)
		interface_type.append(me.cell(i,5).value)
		interface_header.append(me.cell(i,6).value)
		interface_meth.append(me.cell(i,7).value)
		interface_par.append(me.cell(i,8).value)
		interface_bas.append(me.cell(i,9).value)
		i+=1
	return jiekou_bianhao,interface_name,project_name,model_name,interface_url,\
		   interface_header,interface_meth,interface_par,interface_bas,interface_type
#导入测试用例
def paser_interface_case(filename):
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
	interface_type=[]
	is_save_result=[]
	yilai_is=[]
	yilai=[]
	yilai_ziduan=[]
	is_cha_data=[]
	data_sql=[]
	paser_base=[]
	for i in range(2,nrows):
		jiekou_bianhao.append(me.cell(i,0).value)
		project_name.append(me.cell(i,2).value)
		model_name.append(me.cell(i,3).value)
		interface_name.append(me.cell(i,1).value)
		interface_url.append(me.cell(i,4).value)
		interface_type.append(me.cell(i,5).value)
		interface_header.append(me.cell(i,6).value)
		interface_meth.append(me.cell(i,7).value)
		interface_par.append(me.cell(i,8).value)
		interface_bas.append(me.cell(i,9).value)
		is_save_result.append(me.cell(i,10).value)
		yilai_is.append(me.cell(i,11).value)
		yilai.append(me.cell(i,12).value)
		yilai_ziduan.append(me.cell(i,13).value)
		is_cha_data.append(me.cell(i,14).value)
		data_sql.append(me.cell(i,15).value)
		paser_base.append(me.cell(i,16).value)
		i+=1
	return jiekou_bianhao,interface_name,project_name,model_name,interface_url,\
		   interface_header,interface_meth,interface_par,interface_bas,interface_type,\
		   is_save_result,yilai_is,yilai,yilai_ziduan,is_cha_data,data_sql,paser_base
