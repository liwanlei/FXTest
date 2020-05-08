# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:25
from flask import Blueprint

user = Blueprint('user', __name__)
from flask import redirect, request, \
    session, url_for, flash, jsonify
from app.models import *
from flask.views import View, MethodView
from common.decorators import chckuserpermisson
from flask_login import login_required
from config import OneAdminCount
from error_message import *
from flask_mail import Message, Mail


class SetadView(View):  # 设置管理员
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self):
        if chckuserpermisson() == False:
            return jsonify({'code': 13, 'msg': permiss_is_ness, 'data': ''})
        projec = request.get_json()
        try:
            username = projec['username']
            por = projec['url']
            if por == '':
                return jsonify({'code': 14, 'msg': '请选择项目', 'data': ''})
            pan_user = User.query.filter_by(username=username).first()
            if not pan_user:
                return jsonify({'code': 15, 'msg': login_user_not_exict_message, 'data': ''})
            if pan_user.is_sper is True:
                return jsonify({'code': 16, 'msg': '超级管理员不用设置项目', 'data': ''})
            pand_por = Project.query.filter_by(project_name=por).first()
            if not pand_por:
                return jsonify({'code': 17, 'msg': '设置的项目不存在', 'data': ''})
            pro_per = Quanxian.query.filter_by(project=pand_por.id).all()
            oneadmin = []
            for i in pro_per:
                if i.rose == 2:
                    oneadmin.append(i.user.all())
            if [pan_user] in oneadmin:
                return jsonify({'code': 18, 'msg': '你已经是项目管理员了，不需要再次设置'})
            if (len(oneadmin)) > OneAdminCount:
                return jsonify({'code': 19, 'msg': '单个项目的管理员已经达到后台设置的个数限制'})
            for roses in pan_user.quanxians:
                if roses.project == pand_por.id:
                    roses.rose = 2
            try:
                db.session.commit()
                return jsonify({'code': 200, 'msg': '设置管理成功'})
            except:
                db.session.rollback()
                return jsonify({'code': 20, 'msg': '设置管理失败', 'data': ''})
        except Exception as e:
            return jsonify({'code': 21, 'msg': '设置过程目前存在异常,原因是：%s' % e, 'data': ''})


class DeladView(View):  # 取消管理员
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() is False:
            flash(permiss_is_ness)
            return redirect(request.headers.get('Referer'))
        new_ad = User.query.filter_by(id=id, status=False).first()
        if not new_ad:
            flash(login_user_not_exict_message)
            return redirect(url_for('home.adminuser'))
        if new_ad == user:
            flash(admin_cannot_use)
            return redirect(url_for('home.adminuser'))
        return redirect(url_for('home.adminuser'))


class FreadView(View):  # 冻结
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() == False:
            flash(permiss_is_ness)
            return redirect(request.headers.get('Referer'))
        user = User.query.filter_by(username=session.get('username')).first()
        if user.is_sper != 1:
            flash(permiss_is_ness)
            return redirect(request.headers.get('Referer'))
        new_ad = User.query.filter_by(id=id).first()
        if new_ad.status == True:
            flash(free_is_again)
            return redirect(url_for('home.adminuser'))
        if new_ad == user:
            flash(ower_cannot_free_me)
            return redirect(url_for('home.adminuser'))
        new_ad.status = True
        try:
            db.session.commit()
            flash(free_is_success)
            return redirect(url_for('home.adminuser'))
        except Exception as  e:
            db.session.rollback()
            flash(free_user_error)
            return redirect(url_for('home.adminuser'))


class FrereView(View):  # 解冻
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() == False:
            flash(permiss_is_ness)
            return redirect(request.headers.get('Referer'))
        user = User.query.filter_by(username=session.get('username')).first()
        new_ad = User.query.filter_by(id=id).first()
        if new_ad.status == False:
            flash(user_is_not_free)
            return redirect(url_for('home.adminuser'))
        if new_ad != user:
            new_ad.status = False
            try:
                db.session.commit()
                flash(user_is_un_free)
                return redirect(url_for('home.adminuser'))
            except Exception as e:
                db.session.rollback()
                flash(user_is_unfree_success)
                return redirect(url_for('home.adminuser'))
        flash(ower_not_free_me)
        return redirect(url_for('home.adminuser'))


class Acivauserview(View):
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self):
        if chckuserpermisson() == False:
            return jsonify({'code': 13, 'msg': permiss_is_ness, 'data': ''})
        userjobnum = request.get_json()
        try:
            id = int(userjobnum['id'])
            job_num = int(userjobnum['jobnum'])
        except Exception as e:
            return jsonify({'code': 13, 'msg': activ_is_int})
        user = User.query.filter_by(id=id, status=False).first()
        if not user:
            return jsonify({'code': 13, 'msg': login_user_not_exict_message})
        try:
            user_job = User.query.filter_by(jobnum=job_num).first()
            if user_job:
                return jsonify({'code': 13, 'msg': activi_user_jobnum})
        except Exception as e:
            pass
        if (user.jobnum == None or user.jobnum == "None"):
            user.jobnum = job_num
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 20, 'msg': '激活成功', 'data': ''})
        return jsonify({'code': 13, 'msg': '激活失败', 'data': activi_user_jobnum_is})


class RedpassView(View):  # 重置密码
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() is False:
            flash(permiss_is_ness)
            return redirect(request.headers.get('Referer'))
        user = User.query.filter_by(username=session.get('username')).first()
        new_ad = User.query.filter_by(id=id).first()
        if new_ad != user:
            if user.is_sper == 1:
                new_ad.set_password('111111')
                try:
                    db.session.commit()
                    msg = Message(u"密码修改通知", sender=user.email, recipients=user.email)
                    msg.body = u"密码修改成功, 你的用户名：%s，你的密码是：%s" % (user.username, "111111")
                    msg.html = '<a href="http://127.0.0.1:5000/login">去登录</a>'
                    Mail.send(msg)
                    flash(reset_success_message)
                    return redirect(url_for('home.adminuser'))
                except Exception as e:
                    db.session.rollback()
                    flash(user_reset_error)
                    return redirect(url_for('home.adminuser'))
            flash(user_reset_isnot_amin)
            return redirect(url_for('home.adminuser'))
        flash(user_reset_owner)
        return redirect(url_for('home.adminuser'))


class ChangePassword(MethodView):
    @login_required
    def post(self):
        password = request.data.decode('utf-8')
        user = User.query.filter_by(username=session.get('username')).first()
        user.set_password(password)
        try:
            db.session.commit()
            return jsonify({'code': 1, 'data': change_password_success})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 2, 'data': change_password_error})
