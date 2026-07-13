# -*- coding: utf-8 -*-
"""admin_views 视图。"""
from app.home.resource_views._shared import *  # noqa: F401,F403

class AdminUserView(MethodView):
    @login_required
    def get(self):
        wrok = Work.query.all()
        projects = Project.query.filter_by(status=False).all()
        if current_user.is_sper is True:
            pagination = (User.query.order_by(User.id.desc()).all())
        else:
            pagination = []
            id = []
            for projec in current_user.quanxians:
                if (projec.user.all() in id) is False:
                    pagination.append(projec.user.all())
                    id.append(projec.user.all())
            pagination = (flatten_list(pagination))
        pager_obj = Pagination(request.args.get("page", 1),
                               len(pagination), request.path, request.args,
                               per_page_count=PageShow)
        index_list = pagination[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('home/useradmin.html', users=index_list,
                               html=html, wroks=wrok, projects=projects)

    @login_required
    def post(self):
        data = request.get_json()
        name = data['name']
        password = data['password']
        work = data['work']
        project = data['project']
        email = data['email']
        use = User.query.filter_by(username=name).first()
        if use:
            return response(message=MessageEnum.user_is_exist.value[1],
                           code=MessageEnum.user_is_exist.value[0])
        emai = User.query.filter_by(user_email=str(email)).first()
        if emai:
            return response(message=MessageEnum.email_only_one.value[1],
                           code=MessageEnum.email_only_one.value[0])
        wrok = Work.query.filter_by(name=work).first()
        new_user = User(username=name, user_email=email)
        new_user.set_password(password)
        new_user.work_id = wrok.id
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(message=MessageEnum.model_edit_fail.value[1],
                           code=MessageEnum.model_edit_fail.value[0])
        if len(project) <= 0:
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        else:
            try:
                user_id = User.query.filter_by(username=name).first()
                for proj in project:
                    project_one = Project.query.filter_by(project_name=proj).first()
                    quanxian = Quanxian(project=project_one.id, rose=1)
                    quanxian.user.append(user_id)
                    db.session.add(quanxian)
                db.session.commit()
                return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                return response(message=MessageEnum.model_edit_fail.value[1], code=MessageEnum.model_edit_fail.value[0])

class TestResultView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            project = Project.query.filter_by(status=False).all()
        else:
            project = []
            for projec in current_user.quanxians:
                project.append(projec.projects)
        projects_list = fenye_list(Ob_list=project, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        try:
            paged_data = projects_list[int(page) - 1]
            return render_template('home/test_result.html', projects=paged_data, pages=pages)
        except Exception as e:
            logger.exception(e)
            return redirect(url_for('home.test_result'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        delTest = TestResult.query.filter_by(id=data, status=False).first()
        if not delTest:
            return response(message=MessageEnum.delete_report_not_exict.value[1], code=MessageEnum.delete_report_not_exict.value[0])
        delTest.status = True
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(message=MessageEnum.delete_report_fail.value[1], code=MessageEnum.delete_report_fail.value[0])

