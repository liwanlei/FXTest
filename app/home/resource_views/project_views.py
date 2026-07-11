# -*- coding: utf-8 -*-
"""project_views 视图。"""
from app.home.resource_views._shared import *  # noqa: F401,F403

class ProjectView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = get_user_projects()
        projects_list = fenye_list(Ob_list=projects, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        try:
            paged_data = projects_list[int(page) - 1]
            return render_template('home/project.html', projects=paged_data, pages=pages)
        except Exception:
            return redirect(url_for('home.project'))

    @login_required
    def post(self):
        name = request.data.decode('utf-8')
        if current_user.is_sper == False:
            return response(message=MessageEnum.user_not_permision.value[1],
                           code=MessageEnum.user_not_permision.value[0])
        if name == '':
            return response(code=MessageEnum.project_cannot_empty.value[0], message=MessageEnum.project_cannot_empty.value[1])

        projec = Project.query.filter_by(project_name=name, status=False).first()
        if projec:
            return response(code=MessageEnum.project_only_one.value[0], message=MessageEnum.project_only_one.value[1])
        new_moel = Project(project_name=name, project_user_id=current_user.id)
        try:
            db.session.add(new_moel)
            db.session.commit()
            db.session.commit()
            return response(code=MessageEnum.success.value[0], message=MessageEnum.success.value[1])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(code=MessageEnum.project_add_error.value[0], message=MessageEnum.project_add_error.value[1] )

    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        prohect = Project.query.filter_by(id=id).first()
        if not prohect:
            new = Project(project_name=name, project_user_id=current_user.id)
            db.session.add(new)
            db.session.commit()
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
        prohect.project_name = name
        try:
            db.session.commit()
            return response(code=MessageEnum.success.value[0],
                           message=MessageEnum.success.value[1])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(code=MessageEnum.edit_exception.value[0],
                           message=MessageEnum.edit_exception.value[1])

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        proje = Project.query.filter_by(id=data, status=False).first()
        if not proje:
            return response(message=MessageEnum.project_not_exist.value[1], code=MessageEnum.project_not_exist.value[0])
        proje.status = True
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(message=MessageEnum.delete_fail.value[1], code=MessageEnum.delete_fail.value[0])

class ModelView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            project_list = Project.query.filter_by(status=False).all()
        else:
            project_list = []
            for projec in current_user.quanxians:
                project_list.append(projec.projects)
        models = Model.query.filter_by(status=False).all()
        projects_list = fenye_list(Ob_list=models, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        paged_data = projects_list[int(page) - 1]
        return render_template('home/model.html', projects=paged_data, pages=pages,
                               project_list=project_list)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        model = Model.query.filter_by(id=data, status=False).first()
        if not model:
            return response(message=MessageEnum.model_not_exist.value[1], code=MessageEnum.model_not_exist.value[0])
        model.status = True
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(message=MessageEnum.delete_fail.value[1], code=MessageEnum.delete_fail.value[0])

    @login_required
    def post(self):
        data = request.get_json()
        models = Model.query.filter_by(model_name=data['name']).first()
        if data['project'] == '请选择':
            project_one = None
        else:
            project_one = Project.query.filter_by(project_name=data['project']).first().id
        if models:
            return response(code=MessageEnum.model_only_one.value[0], message=MessageEnum.model_only_one.value[1])

        new_moel = Model(model_name=data['name'], model_user_id=current_user.id,
                         project=project_one)
        db.session.add(new_moel)

        try:
            db.session.commit()
            return response(code=MessageEnum.success.value[0],
                           message=MessageEnum.success.value[1])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(code=MessageEnum.model_edit_fial.value[0], message=MessageEnum.model_edit_fial.value[1])

    @login_required
    def put(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        id = json_data['id']
        name = json_data['name']
        projec = json_data['project']
        edit_mode = Model.query.filter_by(id=id, status=False).first()
        if projec == '请选择':
            project_one = None
        else:
            project_one = Project.query.filter_by(status=False, project_name=projec).first().id
        if not edit_mode:
            mew = Model(model_name=name, model_user_id=current_user.id)
            db.session.add(mew)
            db.session.commit()
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
        edit_mode.model_name = name
        edit_mode.project = project_one
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(message=MessageEnum.edit_model_error.value[1], code=MessageEnum.edit_model_error.value[0])

