# -*- coding: utf-8 -*-
"""资源视图公共导入。"""
# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : resource_views.py
# @Time    : 2017/12/7 9:23
import json
import datetime
from common.list_utils import flatten_list
from flask import redirect, request, render_template, url_for, session
from sqlalchemy.orm import joinedload

from common.json_tools import response
from app.models import *
from app.forms import *
from flask.views import MethodView
from flask_login import login_required, login_user, \
    logout_user, current_user
from app import sched
from common.list_paging import Pagination, fenye_list
from error_message import *
from app.helpers import get_user_projects
from config import *
from common.system_log import logger


