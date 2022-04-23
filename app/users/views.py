# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:25
from flask import Blueprint

user = Blueprint('user', __name__)
from flask import redirect, request, \
    session, url_for, flash
from app.models import *
from flask.views import View, MethodView
from common.decorators import chckuserpermisson
from flask_login import login_required
from config import OneAdminCount
from error_message import MessageEnum
from flask_mail import Message, Mail
from common.jsontools import reponse
from  common.systemlog import logger


class SetAdminView(View):  # 设置管理员
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self):
        if chckuserpermisson() is False:
            return reponse(
                code= MessageEnum.permiss_is_ness.value[0],
                message= MessageEnum.permiss_is_ness.value[1], data='')
        projec = request.get_json()
        try:
            username = projec['username']
            por = projec['url']
            if por == '':
                return reponse(
                    code= MessageEnum.select_project_not.value[0],
                    message= MessageEnum.select_project_not.value[1],
                     data= '')
            pan_user = User.query.filter_by(username=username).first()
            if not pan_user:
                return reponse(code= MessageEnum.login_user_not_exict_message.value[0],
                                message= MessageEnum.login_user_not_exict_message.value[1], data= '')
            if pan_user.is_sper is True:
                return reponse(code= MessageEnum.super_admin_not_set_project.value[0],
                                message= MessageEnum.super_admin_not_set_project.value[1], data= '')
            pand_por = Project.query.filter_by(project_name=por).first()
            if not pand_por:
                return reponse(code= MessageEnum.set_project_bot_exict.value[0],
                                message= MessageEnum.set_project_bot_exict.value[1], data= '')
            pro_per = Quanxian.query.filter_by(project=pand_por.id).all()
            oneadmin = []
            for i in pro_per:
                if i.rose == 2:
                    oneadmin.append(i.user.all())
            if [pan_user] in oneadmin:
                return reponse(code= MessageEnum.set_is_admin.value[0], message= MessageEnum.set_is_admin.value[1])
            if (len(oneadmin)) > OneAdminCount:
                return reponse(
                    code= MessageEnum.project_admin_many.value[0], message= MessageEnum.project_admin_many.value[1])
            for roses in pan_user.quanxians:
                if roses.project == pand_por.id:
                    roses.rose = 2
            try:
                db.session.commit()
                return reponse(code= MessageEnum.successs.value[0],
                               message= MessageEnum.successs.value[1])
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                return reponse(
                    code= MessageEnum.set_fail.value[0],
                    message= MessageEnum.set_fail.value[1], data= '')
        except Exception as e:
            logger.exception(e)
            return reponse(code= MessageEnum.set_project_admin_exception.value[0],
                            message= MessageEnum.set_project_admin_exception.value[1] + '原因是：%s' % e, data= '')


class CancelAdminView(View):  # 取消管理员
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() is False:
            flash(MessageEnum.permiss_is_ness.value[1])
            return redirect(request.headers.get('Referer'))
        new_ad = User.query.filter_by(id=id, status=False).first()
        if not new_ad:
            flash(MessageEnum.login_user_not_exict_message.value[1])
            return redirect(url_for('home.adminuser'))
        if new_ad == user:
            flash(MessageEnum.admin_cannot_use.value[1])
            return redirect(url_for('home.adminuser'))
        return redirect(url_for('home.adminuser'))


class FreezeUserView(View):  # 冻结
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() is False:
            flash(MessageEnum.permiss_is_ness.value[1])
            return redirect(request.headers.get('Referer'))
        user = User.query.filter_by(username=session.get('username')).first()
        if user.is_sper != 1:
            flash(MessageEnum.permiss_is_ness.value[1])
            return redirect(request.headers.get('Referer'))
        new_ad = User.query.filter_by(id=id).first()
        if new_ad.status is True:
            flash(MessageEnum.free_is_again.value[1])
            return redirect(url_for('home.adminuser'))
        if new_ad == user:
            flash(MessageEnum.ower_cannot_free_me.value[1])
            return redirect(url_for('home.adminuser'))
        new_ad.status = True
        try:
            db.session.commit()
            flash(MessageEnum.free_is_success.value[1])
            return redirect(url_for('home.adminuser'))
        except Exception as  e:
            logger.exception(e)
            db.session.rollback()
            flash(MessageEnum.free_user_error.value[1])
            return redirect(url_for('home.adminuser'))


class UnFreezeUserView(View):  # 解冻
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() == False:
            flash(MessageEnum.permiss_is_ness.value[1])
            return redirect(request.headers.get('Referer'))
        user = User.query.filter_by(username=session.get('username')).first()
        new_ad = User.query.filter_by(id=id).first()
        if new_ad.status is False:
            flash(MessageEnum.user_is_not_free.value[1])
            return redirect(url_for('home.adminuser'))
        if new_ad != user:
            new_ad.status = False
            try:
                db.session.commit()
                flash(MessageEnum.user_is_un_free.value[1])
                return redirect(url_for('home.adminuser'))
            except Exception as e:
                print(e)
                db.session.rollback()
                flash(MessageEnum.user_is_unfree_success.value[1])
                return redirect(url_for('home.adminuser'))
        flash(MessageEnum.ower_not_free_me.value[1])
        return redirect(url_for('home.adminuser'))


class ActivationUserview(View):
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self):
        if chckuserpermisson() is False:
            return reponse(
                code= MessageEnum.permiss_is_ness.value[0], message= MessageEnum.permiss_is_ness.value[1], data= '')
        userjobnum = request.get_json()
        try:
            id = int(userjobnum['id'])
            job_num = int(userjobnum['jobnum'])
        except Exception as e:
            logger.exception(e)
            return reponse(code= MessageEnum.activ_is_int.value[0], message= MessageEnum.activ_is_int.value[1])
        user = User.query.filter_by(id=id, status=False).first()
        if not user:
            return reponse(code= MessageEnum.login_user_not_exict_message.value[0],
                            message= MessageEnum.login_user_not_exict_message.value[1])
        try:
            user_job = User.query.filter_by(jobnum=job_num).first()
            if user_job:
                return reponse(
                    code= MessageEnum.activi_user_jobnum.value[0], message= MessageEnum.activi_user_jobnum.value[1])
        except Exception as e:
            logger.exception(e)
            pass
        if (user.jobnum is None or user.jobnum == "None"):
            user.jobnum = job_num
            db.session.add(user)
            db.session.commit()
            return reponse(code= MessageEnum.successs.value[0], message= MessageEnum.successs.value[1], data= '')
        return reponse(code= MessageEnum.activi_user_jobnum_is.value[0],
                        message= MessageEnum.activi_user_jobnum_is.value[1])


class ResetPasswordView(View):  # 重置密码
    methods = ['GET', "POST"]

    @login_required
    def dispatch_request(self, id):
        if chckuserpermisson() is False:
            flash(MessageEnum.permiss_is_ness.value[1])
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
                    mail = Mail()
                    mail.send(msg)
                    flash(MessageEnum.reset_success_message.value[1])
                    return redirect(url_for('home.adminuser'))
                except Exception as e:
                    logger.exception(e)
                    db.session.rollback()
                    flash(MessageEnum.user_reset_error.value[1])
                    return redirect(url_for('home.adminuser'))
            flash(MessageEnum.user_reset_isnot_amin.value[1])
            return redirect(url_for('home.adminuser'))
        flash(MessageEnum.user_reset_owner.value[1])
        return redirect(url_for('home.adminuser'))


class ChangePassword(MethodView):
    @login_required
    def post(self):
        password = request.data.decode('utf-8')
        user = User.query.filter_by(username=session.get('username')).first()
        user.set_password(password)
        try:
            db.session.commit()
            return reponse(code= MessageEnum.change_password_success.value[0],
                            data= MessageEnum.change_password_success.value[1])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return reponse(code= MessageEnum.change_password_error.value[0],
                            data= MessageEnum.change_password_error.value[1])
