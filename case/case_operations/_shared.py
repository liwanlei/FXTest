# -*- coding: utf-8 -*-
"""用例操作公共导入。"""
"""
@author: lileilei
@file: case_operations.py
@time: 2018/1/31 13:20
用例导入导出、JMX 转换、批量执行等操作
"""
import os, time, datetime, json, subprocess
from flask import redirect, request, render_template, \
    session, url_for, flash, make_response, \
    send_from_directory
from flask.views import View, MethodView
from flask_login import current_user, login_required
from app.models import *
from common.excel_parser import parse_interface_case
from common.api_client import Api
from common.assertions import assert_in, pare_result_mysql
from common.send_email import send_emails
from common.dingtalk import send_ding
from common.redis_client import ConRedisOper, save_result, get_result
from common.jmx_builder import make
from common.ssh_tools import Sshtool
from common.json_tools import response as jsonreponse
from common.system_log import logger
from error_message import MessageEnum
from ast import literal_eval
import unittest
from app.test_case.new_unittest_case import TestCase, Parmer
from common.bs_test_runner import BSTestRunner
from config import Config_import, paln_run_url, jmeter_data_db
from common.excel_utils import create_interface_case


