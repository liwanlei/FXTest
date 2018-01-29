# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:25
from flask import  Blueprint
user = Blueprint('user', __name__)
from  flask import  redirect,request,render_template,session,url_for,flash,jsonify
from  app.models import *
from app.form import  *
from flask.views import MethodView,View
from  app.common.decorators import chckuserpermisson
from flask_login import current_user,login_required
from config import OneAdminCount
def get_pro_mo():
    projects=Project.query.all()
    model=Model.query.all()
    return  projects,model
class AdduserView(View):#添加用户
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if chckuserpermisson() == False:
            flash('权限不足，不能为项目添加用户')
            return  redirect(request.headers.get('Referer'))
        wrok=Work.query.all()
        projects=[]
        for pri in current_user.quanxians:
            if pri.rose==2 or pri.rose==3 or current_user.is_sper ==1:
                projects.append(pri.projects)
        if request.method =='POST':
            user=request.form.get('user')
            password=request.form.get('password')
            password1=request.form.get('password1')
            email=request.form.get('email')
            work=request.form.get('work')
            usertype=request.form.getlist('usertype')
            if email =='' or user =='' :
                flash(u'请准确填写用户信息')
                return render_template('add/add_user.html', wroks=wrok,projects=projects)
            if len(usertype)<=0 :
                flash(u'添加用户的时候必须选择项目，项目可以是多个')
                return render_template('add/add_user.html', wroks=wrok, projects=projects)
            if password!= password1:
                flash(u'请确定两次密码是否一致')
                return render_template('add/add_user.html', wroks=wrok,projects=projects)
            use=User.query.filter_by(username=user).first()
            if use:
                flash(u'用户已经存在')
                return render_template('add/add_user.html', wroks=wrok,projects=projects)
            emai=User.query.filter_by(user_email=email).first()
            if emai:
                flash(u'邮箱已经存在')
                return render_template('add/add_user.html', wroks=wrok,projects=projects)
            new_user=User(username=user,user_email=email)
            new_user.set_password(password)
            new_user.work_id=work
            db.session.add(new_user)
            try:
                db.session.commit()
                user_id=User.query.filter_by(username=user).first()
                for proj in usertype:
                    quanxian=Quanxian(project=proj,rose=1)
                    quanxian.user.append(user_id)
                    db.session.add(quanxian)
                db.session.commit()
                flash(u'添加成功')
                return redirect(url_for('home.adminuser'))
            except Exception as e:
                db.session.rollback()
                flash(u'添加过程那么不是快速')
                return redirect(url_for('home.adminuser'))
        return render_template('add/add_user.html', wroks=wrok,projects=projects)
class SetadView(View):#设置管理员
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if chckuserpermisson() == False:
            return jsonify({'code': 219, 'msg': '权限不足，不能设置管理员'})
        projec = request.get_json()
        try:
            username=projec['username']
            por=projec['url']
            if por=='':
                return jsonify({'code': 209,'msg': '请选择项目'})
            pan_user=User.query.filter_by(username=username).first()
            if not pan_user:
                return  jsonify({'code':202,'msg':'设置的用户不存在'})
            if pan_user.is_sper is True:
                return jsonify({'code': 2010,'msg': '超级管理员不用设置项目'})
            pand_por=Project.query.filter_by(project_name=por).first()
            if not  pand_por:
                return jsonify({'code': 203, 'msg': '设置的项目不存在'})
            pro_per=Quanxian.query.filter_by(project=pand_por.id).all()
            oneadmin=[]
            for i in pro_per:
                if i.rose==2:
                    oneadmin.append(i.user.all())
            if  [pan_user] in oneadmin:
                return jsonify({'code': 211,'msg': '你已经是项目管理员了，不需要再次设置'})
            if (len(oneadmin))>OneAdminCount:
                return jsonify({'code': 210, 'msg': '单个项目的管理员已经达到后台设置的个数限制'})
            for roses in pan_user.quanxians:
                if roses.project==pand_por.id:
                    roses.rose=2
            try:
                db.session.commit()
                return jsonify({'code': 200,'msg': '设置管理成功'})
            except:
                db.session.rollback()
                return jsonify({'code': 222,'msg': '设置管理失败'})
        except Exception as e:
            return  jsonify({'code':207,'msg':'设置过程目前存在异常'})
class DeladView(View):#取消管理员
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能取消管理员')
            return  redirect(request.headers.get('Referer'))
        new_ad=User.query.filter_by(id=id).first()
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
        if new_ad.status==1:
            flash(u'已经冻结')
            return redirect( url_for('home.adminuser'))
        if new_ad==user:
            flash(u'自己不能冻结自己')
            return redirect( url_for('home.adminuser'))
        new_ad.status=1
        db.session.commit()
        flash(u'已经冻结')
        return redirect( url_for('home.adminuser'))
class FrereView(View):#解冻
    methods=['GET']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能解冻用户')
            return  redirect(request.headers.get('Referer'))
        user=User.query.filter_by(username=session.get('username')).first()
        new_ad=User.query.filter_by(id=id).first()
        if new_ad.status==0:
            flash(u'已经解冻')
            return redirect(url_for('home.adminuser'))
        if new_ad==user:
            if new_ad.is_sper==1:
                new_ad.status = 0
                db.session.commit()
                flash(u'已经解冻')
                return redirect(url_for('home.adminuser'))
            flash(u'自己不能解冻自己')
            return redirect(url_for('home.adminuser'))
        new_ad.status=0
        db.session.commit()
        flash(u'已经解冻')
        return redirect(url_for('home.adminuser'))
class RedpassView(View):#重置密码
    methods=['GET']
    @login_required
    def dispatch_request(self,id):
        if chckuserpermisson() == False:
            flash('权限不足，不能重置密码')
            return  redirect(request.headers.get('Referer'))
        user=User.query.filter_by(username=session.get('username')).first()
        new_ad=User.query.filter_by(id=id).first()
        if new_ad==user:
            if new_ad.is_sper==1:
                new_ad.set_password = 111111
                db.session.commit()
                flash(u'已经重置！密码：111111')
                return redirect(url_for('home.adminuser'))
            flash(u'自己不能重置自己的密码')
            return redirect(url_for('home.adminuser'))
        new_ad.set_password=111111
        db.session.commit()
        flash(u'已经重置！密码：111111')
        return redirect(url_for('home.adminuser'))
class SeruserView(View):#查询用户
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if request.method=='POST':
            user=request.form.get('user')
            if user=='':
                flash(u'请输入您要查询的用户')
                return redirect(url_for('home.adminuser'))
            try:
                use=User.query.filter(User.username.like('%'+user+'%')).order_by('-id').all()
                if len(use)<=0:
                    flash(u'没有找到您输入的用户')
                    return redirect(url_for('home.adminuser'))
                return render_template('home/user_ser.html', users=use)
            except:
                flash(u'没有找到您输入的用户')
                return redirect(url_for('home.adminuser'))
        return redirect(url_for('home.adminuser'))
class Set_emaiView(MethodView):#设置发送测试报告的邮件的
    @login_required
    def get(self):
        user=User.query.filter_by(username=session.get('username')).first().id
        email_report=EmailReport.query.filter_by(email_re_user_id=user).all()
        if len(email_report)<=0:
            return render_template('home/set_send.html', errmessage=u'您还没有设置发送测试报告邮件')
        return render_template('home/set_send.html', email_reports=email_report)
class Add_emaiView(MethodView):#添加邮件
    @login_required
    def get(self):
        form=Set_email_Form()
        return render_template('add/add_emali.html', form=form)
    @login_required
    def post(self):
        form=Set_email_Form()
        if form.validate_on_submit():
            email=request.form.get('send_email')
            password=request.form.get('password')
            shi_f=request.form.get('checkbox')
            resv_email=request.form.get('email')
            resv_email=(str(resv_email).split(','))
            port=request.form.get('port')
            stmp_email=request.form.get('stmp_email')
            if email =='' or password=='' or resv_email=='' or port=='' or stmp_email =='':
                flash(u'请准确填写信息')
                return render_template('add/add_emali.html', form=form)
            user_id=current_user.id
            if shi_f =='on':
                shi_f=True
                user_is=EmailReport.query.filter_by(email_re_user_id=user_id,default_set=True).first()
                if user_is:
                    flash(u'只能有一个为默认设置')
                    return render_template('add/add_emali.html', form=form)
                email_new=EmailReport(email_re_user_id=int(user_id),send_email=str(email),send_email_password=str(password),to_email=str(resv_email),default_set=True,port=int(port),stmp_email=str(stmp_email))
                db.session.add(email_new)
                db.session.commit()
                flash(u'成功设置一个默认配置')
                return redirect(url_for('user.setting'))
            email_new=EmailReport(email_re_user_id=int(user_id),send_email=str(email),send_email_password=str(password),to_email=str(resv_email))
            db.session.add(email_new)
            try:
                db.session.commit()
                flash(u'成功设置一个配置')
                return redirect(url_for('user.setting'))
            except:
                db.session.rollback()
                flash(u'配置过程出现了异军突起')
                return redirect(url_for('user.setting'))
        return render_template('add/add_emali.html', form=form)
class DeleteView(View):#删除邮件
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        email_re=EmailReport.query.filter_by(id=id).first()
        user_id=current_user.id
        if email_re.email_re_user_id==int(user_id):
            email_re.status=True
            db.session.commit()
            flash(u'删除成功')
            return redirect(url_for('user.setting'))
        flash(u'您没有权限删除')
        return redirect(url_for('user.setting'))
class EditemailView(MethodView):#编辑邮件
    @login_required
    def get(self,id):
        emai=EmailReport.query.filter_by(id=id).first()
        return render_template('edit/edit_emali.html', emai=emai)
    @login_required
    def post(self,id):
        emai=EmailReport.query.filter_by(id=id).first()
        email=request.form.get('send_email')
        password=request.form.get('password')
        shi_f=request.form.get('checkbox')
        resv_email=request.form.get('email')
        resv_email=(str(resv_email).split(','))
        stmp_em=request.form.get('stmp')
        port=request.form.get('port')
        if email =='' or password=='' or resv_email=='' or stmp_em =='' or port =='':
            flash(u'请准确填写信息')
            return render_template('edit/edit_emali.html', emai=emai)
        user_id=current_user.id
        if shi_f =='on':
            user_is=EmailReport.query.filter_by(email_re_user_id=user_id,default_set=True).first()
            if user_is:
                flash(u'只能有一个为默认设置')
                return render_template('edit/edit_emali.html', emai=emai)
            emai.email_re_user_id=int(user_id)
            emai.send_email=str(email)
            emai.send_email_password=str(password)
            emai.to_email=str(resv_email)
            emai.stmp_email=str(stmp_em)
            emai.port=int(port)
            emai.default_set=True
            try:
                db.session.commit()
                flash(u'编辑成功')
                return redirect(url_for('user.setting'))
            except:
                db.session.rollback()
                flash(u'编辑过程中出现了小抑菌')
                return redirect(url_for('user.setting'))
        emai.email_re_user_id=int(user_id)
        emai.send_email=str(email)
        emai.send_email_password=str(password)
        emai.to_email=str(resv_email)
        emai.stmp_email=str(stmp_em)
        emai.port=int(port)
        try:
            db.session.commit()
            flash(u'编辑成功')
            return redirect(url_for('user.setting'))
        except:
            db.session.rollback()
            flash(u'编辑过程中出现了小抑菌')
            return redirect(url_for('user.setting'))
class QuzhiMoView(View):#取消默认
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        del_em=EmailReport.query.filter_by(id=id).first()
        if del_em:
            if int(current_user.id)==del_em.email_re_user_id:
                del_e=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True,status=True).all()
                if len(del_e)<=1:
                    flash(u'取消默认失败，用户必须有一个默认的邮箱！！')
                    return redirect(url_for('user.setting'))
                del_em.default_set=False
                db.session.commit()
                flash(u'取消默认成功')
                return redirect(url_for('user.setting'))
            flash(u'您没有权限来取消')
            return redirect(url_for('user.setting'))
        flash(u'你要取消的默认不存在')
        return redirect(url_for('user.setting'))
class ShezhiMoView(View):#设置默认
    methods=['GET','POST']
    @login_required
    def dispatch_request(self,id):
        shezi_em=EmailReport.query.filter_by(id=id).first()
        if shezi_em:
            if int(current_user.id)==shezi_em.email_re_user_id:
                del_e=EmailReport.query.filter_by(email_re_user_id=int(current_user.id),default_set=True,status=False).all()
                if len(del_e)>0:
                    flash(u'一个账户只能有一个默认设置')
                    return redirect(url_for('user.setting'))
                shezi_em.default_set=True
                db.session.commit()
                flash(u'设置默认成功')
                return redirect(url_for('user.setting'))
            flash(u'您没有权限来设置')
            return redirect(url_for('user.setting'))
        flash(u'你要设置的默认邮箱配置不存在')
        return redirect(url_for('user.setting'))
