# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:25
from flask import  Blueprint
user = Blueprint('user', __name__)
from  flask import  redirect,request,\
    session,url_for,flash,jsonify
from  app.models import *
from flask.views import View,MethodView
from common.decorators import chckuserpermisson
from flask_login import login_required
from config import OneAdminCount
class SetadView(View):#设置管理员
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if chckuserpermisson() == False:
            return jsonify({'code': 13, 'msg': '权限不足，不能设置管理员','data':''})
        projec = request.get_json()
        try:
            username=projec['username']
            por=projec['url']
            if por=='':
                return jsonify({'code': 14,'msg': '请选择项目','data':''})
            pan_user=User.query.filter_by(username=username).first()
            if not pan_user:
                return  jsonify({'code':15,'msg':'设置的用户不存在','data':''})
            if pan_user.is_sper is True:
                return jsonify({'code': 16,'msg': '超级管理员不用设置项目','data':''})
            pand_por=Project.query.filter_by(project_name=por).first()
            if not  pand_por:
                return jsonify({'code': 17, 'msg': '设置的项目不存在','data':''})
            pro_per=Quanxian.query.filter_by(project=pand_por.id).all()
            oneadmin=[]
            for i in pro_per:
                if i.rose==2:
                    oneadmin.append(i.user.all())
            if  [pan_user] in oneadmin:
                return jsonify({'code': 18,'msg': '你已经是项目管理员了，不需要再次设置'})
            if (len(oneadmin))>OneAdminCount:
                return jsonify({'code': 19, 'msg': '单个项目的管理员已经达到后台设置的个数限制'})
            for roses in pan_user.quanxians:
                if roses.project==pand_por.id:
                    roses.rose=2
            try:
                db.session.commit()
                return jsonify({'code': 200,'msg': '设置管理成功'})
            except:
                db.session.rollback()
                return jsonify({'code': 20,'msg': '设置管理失败','data':''})
        except Exception as e:
            return  jsonify({'code':21,'msg':'设置过程目前存在异常,原因是：%s'%e,'data':''})
class DeladView(View):#取消管理员
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() is False:
            flash('权限不足，不能取消管理员')
            return  redirect(request.headers.get('Referer'))
        new_ad=User.query.filter_by(id=id,status=False).first()
        if not new_ad:
            flash(u'找不到你要设置的管理员的用户')
            return redirect(url_for('home.adminuser'))
        if new_ad==user:
            flash(u'自己不能取消自己的管理员')
            return redirect(url_for('home.adminuser'))
        return redirect(url_for('home.adminuser'))
class FreadView(View):#冻结
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能冻结')
            return  redirect(request.headers.get('Referer'))
        user=User.query.filter_by(username=session.get('username')).first()
        if user.is_sper!=1:
            flash('权限不足，不能冻结')
            return redirect(request.headers.get('Referer'))
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.status==True:
            flash(u'已经冻结,无需再次冻结')
            return redirect( url_for('home.adminuser'))
        if new_ad==user:
            flash(u'自己不能冻结自己')
            return redirect( url_for('home.adminuser'))
        new_ad.status=True
        try:
            db.session.commit()
            flash(u'已经冻结成功')
            return redirect( url_for('home.adminuser'))
        except Exception as  e:
            db.session.rollback()
            flash(u'冻结用户失败！原因：%s'%e)
            return redirect(url_for('home.adminuser'))
class FrereView(View):#解冻
    methods=['GET']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能解冻用户')
            return  redirect(request.headers.get('Referer'))
        user=User.query.filter_by(username=session.get('username')).first()
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.status==False:
            flash(u'用户没有处于冻结状态')
            return redirect(url_for('home.adminuser'))
        if new_ad!=user:
            new_ad.status=False
            try:
                db.session.commit()
                flash(u'解冻成功')
                return redirect(url_for('home.adminuser'))
            except Exception as e:
                db.session.rollback()
                flash(u'解冻失败,原因是：%s'%e)
                return  redirect(url_for('home.adminuser'))
        flash(u'自己不能解冻自己')
        return redirect(url_for('home.adminuser'))
class RedpassView(View):#重置密码
    methods=['GET']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() is False:
            flash('权限不足，不能重置密码')
            return  redirect(request.headers.get('Referer'))
        user=User.query.filter_by(username=session.get('username')).first()
        new_ad=User.query.filter_by(id=id).first()
        if new_ad!=user:
            if user.is_sper ==1:
                new_ad.set_password('111111')
                try:
                    db.session.commit()
                    flash(u'已经重置！密码：111111')
                    return redirect(url_for('home.adminuser'))
                except Exception as e:
                    db.session.rollback()
                    flash('重置密码失败，原因：%s'%e)
                    return  redirect(url_for('home.adminuser'))
            flash(u'不是管理员不能重置')
            return redirect(url_for('home.adminuser'))
        flash(u'自己不能重置自己的密码')
        return redirect(url_for('home.adminuser'))
class ChangePassword(MethodView):
    @login_required
    def post(self):
        password=request.data.decode('utf-8')
        user = User.query.filter_by(username=session.get('username')).first()
        user.set_password(password)
        try:
            db.session.commit()
            return  jsonify({'code':1,'data':'修改密码成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 2, 'data': '修改密码失败'})