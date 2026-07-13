# -*- coding: utf-8 -*-
"""interface_views 视图。"""
from app.home.resource_views._shared import *  # noqa: F401,F403

class InterfaceView(MethodView):
    @login_required
    def get(self):
        models = Model.query.filter_by(status=False).all()
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = []
            for pros in current_user.quanxians:
                projects.append(pros.projects)
        return render_template('home/interface.html', projects=projects,
                               models=models)

    @login_required
    def post(self):
        data = request.get_json()
        project = data['project']
        model = data['model']
        name = data['name']
        url = data['url']
        headers = data['headers']
        xieyi = data['xieyi']
        meth = data['meth']
        project_id = Project.query.filter_by(project_name=project).first().id
        models_id = Model.query.filter_by(model_name=model).first().id
        try:
            new_interface = Interface(model_id=models_id,
                                      projects_id=project_id,
                                      Interface_name=name,
                                      Interface_url=url,
                                      Interface_meth=meth,
                                      Interface_user_id=current_user.id,
                                      Interface_headers=headers,
                                      interfacetype=xieyi)
            db.session.add(new_interface)
            db.session.commit()
            return response(message=MessageEnum.interface_add_success.value[1],
                           code=MessageEnum.interface_add_success.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(
                message=MessageEnum.interface_add_error.value[1], code=MessageEnum.interface_add_erroe.value[0],
                data='')

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        interface = Interface.query.filter_by(id=data, status=False).first()
        if not interface:
            return response(
                message=MessageEnum.interface_add_not.value[1],
                code=MessageEnum.interface_add_not.value[0])

        interface.status = True
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        except Exception as e:
            logger.info(e)
            db.session.rollback()
            return response(message=MessageEnum.delete_interface_error.value[1],
                           code=MessageEnum.delete_interface_error.value[0])

class CaseView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).all()
        else:
            projects = get_user_projects()
        return render_template('home/interface_case.html', projects=projects)

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        testcase = InterfaceTest.query.filter_by(id=data).first()
        if not testcase:
            return response(data=MessageEnum.case_not_exist.value[1],
                           code=MessageEnum.case_not_exist.value[0])
        try:
            testcase.status = True
            db.session.commit()
            return response(data=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(
                data=MessageEnum.delete_case_error.value[1],
                code=MessageEnum.delete_case_error.value[0])

