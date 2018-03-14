# -*- coding: utf-8 -*-
# @Author  : lileilei
# @File    : views.py
# @Time    : 2017/12/7 12:11
from flask import  Blueprint
from  flask import  redirect,request,render_template,url_for,flash
from app.models import *
from flask.views import MethodView,View
from flask_login import current_user,login_required
from app import loginManager
from app.common.parsenei import get_to_data
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
mock = Blueprint('mock', __name__)
class AddmockViews(MethodView):#添加mock服务的详细内容
    @login_required
    def get(self):
        return  render_template('add/addmockserver.html')
    @login_required
    def post(self):
        name=request.form['name']
        desc=request.form['desc']
        path=request.form['path']
        methods=request.form['meth']
        types=request.form['type']
        headers=request.form['headers']
        parm=request.form['parm']
        back=request.form['back']
        is_check=request.form['checkout']
        is_headers=request.form['checkouheaders']
        kaiqi_is=request.form['kaiqi']
        if name =='':
            flash(u'接口名称不能为空')
            return render_template('add/addmockserver.html')
        if path =='':
            flash(u'项目路径不能为空')
            return render_template('add/addmockserver.html')
        if methods =='':
            flash(u'请求方式不能为空')
            return render_template('add/addmockserver.html')
        if types =='':
            flash(u'类型不能为空')
            return render_template('add/addmockserver.html')
        if parm =='':
            flash(u'参数不能为空')
            return render_template('add/addmockserver.html')
        if back =='':
            flash(u'返回不能为空')
            return render_template('add/addmockserver.html')
        is_path=Mockserver.query.filter_by(path=path).first()
        if is_path:
            flash(u'路径已经存在!')
            return render_template('add/addmockserver.html')
        name_is=Mockserver.query.filter_by(name=name).first()
        if name_is:
            flash(u'接口已经存在!')
            return render_template('add/addmockserver.html')
        if is_check ==u'是':
            is_check=True
        else:is_check=False
        if is_headers==u'是':
            is_headers=True
        else:is_headers=False
        if kaiqi_is==u'是':
            is_kaiqi=True
        else:is_kaiqi=False
        new_mock=Mockserver(name=name)
        new_mock.make_uers=current_user.id
        new_mock.path =path
        new_mock.methods =methods
        new_mock.headers =headers
        new_mock.description =desc
        new_mock.fanhui =back
        new_mock.params =parm
        new_mock.rebacktype =types
        new_mock.status =is_kaiqi
        new_mock.ischeck =is_check
        new_mock.is_headers =is_headers
        new_mock.update_time=datetime.datetime.now()
        db.session.add(new_mock)
        try:
            db.session.commit()
            flash(u'添加成功!!!')
            return  redirect(url_for('home.mockserver'))
        except:
            db.session.rollback()
            flash(u'添加出现错了，请从新添加')
            return  redirect(url_for('mock.addmock'))
class DeletemockViews(MethodView):#删除mock
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        ded=Mockserver.query.filter_by(id=id).first()
        if ded:
            ded.delete=True
            db.session.commit()
            flash(u'删除成功！')
            return  redirect(next or url_for('home.mockserver'))
        flash(u'删除异常！！')
        return redirect(next or url_for('home.mockserver'))
class EditmockserView(MethodView):#编辑mack服务
    @login_required
    def get(self,id):
        mock=Mockserver.query.filter_by(id=id).first()
        if not mock:
            flash(u'请重新选择编辑的mock')
            return redirect(url_for('home.mockserver'))
        return  render_template('edit/editmock.html', mock=mock)
    def post(self,id):
        mock = Mockserver.query.filter_by(id=id).first()
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
        if is_check ==u'是':
            is_check=True
        else:is_check=False
        if is_headers==u'是':
            is_headers=True
        else:is_headers=False
        if kaiqi_is==u'是':
            is_kaiqi=True
        else:is_kaiqi=False
        mock.make_uers = current_user.id
        mock.path = path
        mock.methods = methods
        mock.headers = headers
        mock.description = desc
        mock.fanhui = back
        mock.name=name
        mock.params = parm
        mock.rebacktype = types
        mock.status = is_kaiqi
        mock.ischeck = is_check
        mock.is_headers = is_headers
        mock.update_time = datetime.datetime.now()
        try:
            db.session.commit()
            flash(u'编辑成功！')
            return  redirect(url_for('home.mockserver'))
        except Exception as e:
            db.session.rollback()
            flash(u'编辑出现状况，请你看看,原因：%s'%e)
            return render_template('edit/editmock.html', mock=mock)
class MakemockserverView(MethodView):#做一个mock服务
    def get(self,path):#get请求方法
        data=get_to_data(path)
        return data
    def post(self,path):#post请求方法
        data = get_to_data(path)
        return data
    def put(self,path):#put请求方法
        data = get_to_data(path)
        return data
    def delete(self,path):#delete请求方法
        data = get_to_data(path)
        return data
class StartmockView(MethodView):#开启mock服务
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        start=Mockserver.query.filter_by(id=id).first()
        if start:
            start.status=True
            try:
                db.session.commit()
                flash(u'mock开启成功，可以正常使用')
                return  redirect(next or url_for('home.mockserver'))
            except:
                flash(u'mock开启失败，疑似库存遭到打击！！')
                return redirect(next or url_for('home.mockserver'))
        flash(u'mock的服务开启失败，因为不存在')
        return redirect(next or url_for('mockserver'))
class ClosemockView(MethodView):#关闭mock服务
    @login_required
    def get(self,id):
        next = request.headers.get('Referer')
        start=Mockserver.query.filter_by(id=id).first()
        if start:
            start.status=False
            try:
                db.session.commit()
                flash(u'mock关闭成功，可以正常使用')
                return  redirect(next or url_for('home.mockserver'))
            except:
                flash(u'mock关闭失败，疑似库存遭到打击！！')
                return redirect(next or url_for('home.mockserver'))
        flash(u'mock的服务关闭失败，因为不存在')
        return redirect(next or url_for('mockserver'))
class SermockView(View):#搜索mock接口
    methods=['GET','POST']
    @login_required
    def dispatch_request(self):
        if request.method=='POST':
            mock=request.form.get('mock')
            if mock=='':
                flash(u'请输入您要查询的mock')
                return redirect(url_for('home.mockserver'))
            try:
                use=Mockserver.query.filter(Mockserver.name.like('%'+mock+'%')).order_by('-id').all()
                if len(use)<=0:
                    flash(u'没有找到您输入的mock接口')
                    return redirect(url_for('home.mockserver'))
                return render_template('home/serch_mockserver.html', inte=use)
            except:
                flash(u'没有找到您输入的mock接口')
                return redirect(url_for('home.mockserver'))
        return redirect(url_for('home.mockserver'))