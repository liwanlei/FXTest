""" 
@author: lileilei
@file: opearexcel.py
@time: 2018/4/4 16:10 
"""
'''
写入Excel,导入接口的可以用到
'''
import xlwt
from xlwt import *


def yangshi1():
    style = XFStyle()
    fnt = Font()
    fnt.name = u'微软雅黑'
    fnt.bold = True
    style.font = fnt
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment  # 给样式添加文字居中属性
    style.font.height = 350  # 设置字体大小
    return style


def yangshi2():
    style1 = XFStyle()
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style1.alignment = alignment  # 给样式添加文字居中属性
    style1.font.height = 330  # 设置字体大小
    return style1


def create_interface(filename: str, interfacelist: list):
    try:
        file = Workbook(filename)
        table = file.add_sheet('接口', cell_overwrite_ok=True)
        for i in range(1, 9):
            table.col(i).width = 300 * 25
        style = yangshi1()
        table.write(0, 0, '编号', style=style)
        table.write(0, 1, '项目名字', style=style)
        table.write(0, 2, '模块名字', style=style)
        table.write(0, 3, '接口名字', style=style)
        table.write(0, 4, '接口url', style=style)
        table.write(0, 5, '接口协议', style=style)
        table.write(0, 6, '请求头', style=style)
        table.write(0, 7, '请求方式', style=style)
        # table.write(0, 8, '请求示例', style=style)
        # table.write(0, 9, '请求返回示例', style=style)
        table.write(0, 8, '添加人', style=style)
        stylen = yangshi2()
        for i in range(len(interfacelist)):
            table.write(i + 1, 0, str(interfacelist[i].id), style=stylen)
            table.write(i + 1, 1, str(interfacelist[i].projects), style=stylen)
            table.write(i + 1, 2, str(interfacelist[i].models), style=stylen)
            table.write(i + 1, 3, interfacelist[i].Interface_name, style=stylen)
            table.write(i + 1, 4, interfacelist[i].Interface_url, style=stylen)
            table.write(i + 1, 5, interfacelist[i].interfacetype, style=stylen)
            table.write(i + 1, 6, interfacelist[i].Interface_headers, style=stylen)
            table.write(i + 1, 7, interfacelist[i].Interface_meth, style=stylen)
            # table.write(i + 1, 8, interfacelist[i].Interface_par, style=stylen)
            # table.write(i + 1, 9, interfacelist[i].Interface_back, style=stylen)
            table.write(i + 1, 8, str(interfacelist[i].users), style=stylen)
            i += 1
        file.save(filename)
        return {'code': 0, 'message': filename}
    except Exception as e:
        return {'code': 1, 'error': e}


def create_interface_case(filename: str, caselist: list):
    try:
        file = Workbook(filename)
        table = file.add_sheet('接口测试用例', cell_overwrite_ok=True)
        style = yangshi1()
        for i in range(1, 17):
            table.col(i).width = 300 * 30
        table.write(0, 0, '编号', style=style)
        table.write(0, 1, '项目名字', style=style)
        table.write(0, 2, '模块名字', style=style)
        table.write(0, 3, '接口名字', style=style)
        table.write(0, 4, '接口url', style=style)
        table.write(0, 5, '接口协议', style=style)
        table.write(0, 6, '请求头', style=style)
        table.write(0, 7, '请求方式', style=style)
        table.write(0, 8, '参数', style=style)
        table.write(0, 9, '断言', style=style)
        table.write(0, 10, '是否保存测试结果', style=style)
        table.write(0, 11, '是否依赖', style=style)
        table.write(0, 12, '依赖接口', style=style)
        table.write(0, 13, '依赖接口的参数', style=style)
        table.write(0, 14, '是否查询数据库', style=style)
        table.write(0, 15, '数据库查询语句', style=style)
        table.write(0, 16, '数据库比较字段', style=style)
        table.write(0, 17, '添加人', style=style)
        stylen = yangshi2()
        for i in range(len(caselist)):
            if caselist[i].pid is None:
                shifao = '否'
            else:
                shifao = '是'
            if caselist[i].pid is None:
                shi_pid = ''
            else:
                shi_pid = caselist[i].pid
            table.write(i + 1, 0, caselist[i].id, style=stylen)
            table.write(i + 1, 1, str(caselist[i].projects), style=stylen)
            table.write(i + 1, 2, str(caselist[i].models), style=stylen)
            table.write(i + 1, 3, caselist[i].Interface_name, style=stylen)
            table.write(i + 1, 4, caselist[i].Interface_url, style=stylen)
            table.write(i + 1, 5, caselist[i].interface_type, style=stylen)
            table.write(i + 1, 6, caselist[i].Interface_headers, style=stylen)
            table.write(i + 1, 7, caselist[i].Interface_meth, style=stylen)
            table.write(i + 1, 8, caselist[i].Interface_pase, style=stylen)
            table.write(i + 1, 9, caselist[i].Interface_assert, style=stylen)
            table.write(i + 1, 10, caselist[i].saveresult, style=stylen)
            table.write(i + 1, 11, shifao, style=stylen)
            table.write(i + 1, 12, shi_pid, style=stylen)
            table.write(i + 1, 13, caselist[i].getattr_p, style=stylen)
            table.write(i + 1, 14, caselist[i].is_database, style=stylen)
            table.write(i + 1, 15, caselist[i].chaxunshujuku, style=stylen)
            table.write(i + 1, 16, caselist[i].databaseziduan, style=stylen)
            table.write(i + 1, 17, str(caselist[i].users), style=stylen)
            i += 1
        file.save(filename)
        return {'code': 0, 'message': filename}
    except Exception as e:
        return {'code': 1, 'error': e}
