""" 
@author: lileilei
@file: urls.py 
@time: 2018/1/31 13:20 
"""
from app.case.views import *
from app.case import case

case.add_url_rule('/addtestcase', view_func=AddtestcaseView.as_view('addtestcase'))
case.add_url_rule('/edit_case/<int:id>', view_func=EditcaseView.as_view('edit_case'))
case.add_url_rule('/import_case', view_func=ImportCaseView.as_view('import_case'))
case.add_url_rule('/ser_case', view_func=SerCaseView.as_view('ser_case'))
case.add_url_rule('/makeonlyonecase', view_func=MakeOnlyOneCaseView.as_view('makeonlyonecase'))
case.add_url_rule('/mulitecase', view_func=MuliteCaseLiView.as_view('mulitecase'))
case.add_url_rule('/exportcase', view_func=ExportCaseView.as_view('exportcase'))
case.add_url_rule("/casetojmx", view_func=CaseToJmxView.as_view("casetojmx"))
case.add_url_rule("/jmxtoserver", view_func=JmxToServerView.as_view("jmxtoserver"))
case.add_url_rule('/caseonedeteil', view_func=OneCaseDetialView.as_view('caseonedeteil'))



case.add_url_rule("/getprojectinterfacecase",view_func=GetProjectInterfaceCase.as_view("getprojectinterfacecase"))
