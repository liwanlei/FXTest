'''
@author: lileilei
@file: views.py
@time: 2018/8/17 14:50
'''
from flask import  Blueprint
from  flask import  render_template
from app.models import *
from flask.views import MethodView
from flask_login import current_user,login_required
jenkin = Blueprint('jenki', __name__)
