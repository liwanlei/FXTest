# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:11
from flask import Blueprint
from flask import redirect, request, \
    render_template, url_for, flash
from app.models import *
from flask.views import MethodView
from flask_login import current_user, login_required
from app import loginManager
from common.mockservermeth import get_token_data
from error_message import MessageEnum
from common.systemlog import logger

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


mock = Blueprint('mock', __name__)


class EditMockServerView(MethodView):  # 编辑mock服务
    @login_required
    def get(self, id):
        mock = Mockserver.query.filter_by(id=id, status=False).first()
        if not mock:
            flash(MessageEnum.use_select_edit.value[1])
            return redirect(url_for('home.mockserver'))
        return render_template('edit/editmock.html', mock=mock)

    def post(self, id):
        mock = Mockserver.query.filter_by(id=id, status=False).first()
        if not mock:
            flash(MessageEnum.mock_check_again.value[1])
            return redirect(url_for('home.mockserver'))
        name = request.form['name']
        desc = request.form['desc']
        path = request.form['path']
        methods = request.form['meth']
        types = request.form['type']
        headers = request.form['headers']
        parm = request.form['parm']
        back = request.form['back']
        is_check = request.form['checkout']
        is_headers = request.form['checkouheaders']
        run_is = request.form['kaiqi']
        if is_check == u'是':
            is_check = True
        else:
            is_check = False
        if is_headers == u'是':
            is_headers = True
        else:
            is_headers = False
        if run_is == u'是':
            is_start = True
        else:
            is_start = False
        mock.make_uers = current_user.id
        mock.path = path
        mock.methods = methods
        mock.headers = headers
        mock.description = desc
        mock.fanhui = back
        mock.name = name
        mock.params = parm
        mock.rebacktype = types
        mock.status = is_start
        mock.ischeck = is_check
        mock.is_headers = is_headers
        mock.update_time = datetime.datetime.now()
        try:
            db.session.commit()
            flash(MessageEnum.success.value[1])
            return redirect(url_for('home.mockserver'))
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.mock_edit_fail.value[1])
            return render_template('edit/editmock.html', mock=mock)


class MakeMockserverView(MethodView):  # 做一个mock服务
    def get(self, path):  # get请求方法
        data = get_token_data(path)
        return data

    def post(self, path):  # post请求方法
        data = get_token_data(path)
        return data

    def put(self, path):  # put请求方法
        data = get_token_data(path)
        return data

    def delete(self, path):  # delete请求方法
        data = get_token_data(path)
        return data


class StartMockView(MethodView):  # 开启mock服务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        start = Mockserver.query.filter_by(id=id, status=False).first()
        if start:
            start.status = True
            try:
                db.session.commit()
                flash(MessageEnum.mock_start_success.value[1])
                return redirect(next or url_for('home.mockserver'))
            except Exception as e:
                logger.exception(e)
                flash(MessageEnum.mock_server_start_failed.value[1])
                return redirect(next or url_for('home.mockserver'))
        flash(MessageEnum.mock_start_error.value[1])
        return redirect(next or url_for('mockserver'))


class CloseMockView(MethodView):  # 关闭mock服务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        start = Mockserver.query.filter_by(id=id).first()
        if start:
            start.status = False
            try:
                db.session.commit()
                flash(MessageEnum.mock_close_success.value[1])
                return redirect(next or url_for('home.mockserver'))
            except Exception as e:
                logger.exception(e)
                flash(MessageEnum.mock_server_close_fail.value[1])
                return redirect(next or url_for('home.mockserver'))
        flash(MessageEnum.mock_stop_fail.value[1])
        return redirect(next or url_for('mockserver'))
