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
from common.mockservermeth import get_to_data


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


mock = Blueprint('mock', __name__)


class EditmockserView(MethodView):  # 编辑mack服务
    @login_required
    def get(self, id):
        mock = Mockserver.query.filter_by(id=id, status=False).first()
        if not mock:
            flash(u'请重新选择编辑的mock')
            return redirect(url_for('home.mockserver'))
        return render_template('edit/editmock.html', mock=mock)

    def post(self, id):
        mock = Mockserver.query.filter_by(id=id, status=False).first()
        if not mock:
            flash(u'请重新选择编辑的mock')
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
        kaiqi_is = request.form['kaiqi']
        if is_check == u'是':
            is_check = True
        else:
            is_check = False
        if is_headers == u'是':
            is_headers = True
        else:
            is_headers = False
        if kaiqi_is == u'是':
            is_kaiqi = True
        else:
            is_kaiqi = False
        mock.make_uers = current_user.id
        mock.path = path
        mock.methods = methods
        mock.headers = headers
        mock.description = desc
        mock.fanhui = back
        mock.name = name
        mock.params = parm
        mock.rebacktype = types
        mock.status = is_kaiqi
        mock.ischeck = is_check
        mock.is_headers = is_headers
        mock.update_time = datetime.datetime.now()
        try:
            db.session.commit()
            flash(u'编辑成功！')
            return redirect(url_for('home.mockserver'))
        except Exception as e:
            db.session.rollback()
            flash(u'编辑出现状况，请你看看,原因：%s' % e)
            return render_template('edit/editmock.html', mock=mock)


class MakemockserverView(MethodView):  # 做一个mock服务
    def get(self, path):  # get请求方法
        data = get_to_data(path)
        return data

    def post(self, path):  # post请求方法
        data = get_to_data(path)
        return data

    def put(self, path):  # put请求方法
        data = get_to_data(path)
        return data

    def delete(self, path):  # delete请求方法
        data = get_to_data(path)
        return data


class StartmockView(MethodView):  # 开启mock服务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        start = Mockserver.query.filter_by(id=id, status=False).first()
        if start:
            start.status = True
            try:
                db.session.commit()
                flash(u'mock开启成功，可以正常使用')
                return redirect(next or url_for('home.mockserver'))
            except:
                flash(u'mock开启失败，疑似库存遭到打击！！')
                return redirect(next or url_for('home.mockserver'))
        flash(u'mock的服务开启失败，因为不存在')
        return redirect(next or url_for('mockserver'))


class ClosemockView(MethodView):  # 关闭mock服务
    @login_required
    def get(self, id):
        next = request.headers.get('Referer')
        start = Mockserver.query.filter_by(id=id).first()
        if start:
            start.status = False
            try:
                db.session.commit()
                flash(u'mock关闭成功,停止访问')
                return redirect(next or url_for('home.mockserver'))
            except:
                flash(u'mock关闭失败，疑似库存遭到打击！！')
                return redirect(next or url_for('home.mockserver'))
        flash(u'mock的服务关闭失败，因为不存在')
        return redirect(next or url_for('mockserver'))
