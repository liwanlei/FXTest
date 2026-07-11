# -*- coding: utf-8 -*-
"""env_views 视图。"""
from app.home.resource_views._shared import *  # noqa: F401,F403

class TestenvironmentView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            events = []
            events.append(Interfacehuan.query.filter_by(status=False).order_by(
                Interfacehuan.id.desc()).all())
        else:
            events = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) is False:
                    events.append(
                        Interfacehuan.query.filter_by(project=project.projects.id,
                                                      status=False).order_by(
                            Interfacehuan.id.desc()).all())
                    id.append(project.projects.id)
        projects_list = fenye_list(Ob_list=events, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        if current_user.is_sper is True:
            projects = Project.query.filter_by(status=False).order_by(
                Project.id.desc()).all()
        else:
            projects = get_user_projects()
        try:
            test_events_page = projects_list[int(page) - 1]
            return render_template('home/events.html', events=test_events_page,
                                   pages=pages,
                                   projects=projects)
        except Exception as e:
            logger.exception(e)
            return redirect(url_for('home.testenvironment'))

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        event = Interfacehuan.query.filter_by(id=data).first()
        event.status = True
        try:
            db.session.commit()
            return response(
                code=MessageEnum.success.value[0]
                , message=MessageEnum.success.value[1]
            )
        except Exception as e:
            logger.error(e)
            return response(message=MessageEnum.delete_fail.value[1],
                           code=MessageEnum.delete_fail.value[0])

    @login_required
    def post(self):
        data = request.get_json()
        json_data = data
        project = json_data['project']
        url = json_data['url']
        desc = json_data['desc']
        name = json_data['name']
        host = json_data['host']
        port = json_data['port']
        usernmae = json_data['username']
        password = json_data['password']
        url_old = Interfacehuan.query.filter_by(url=str(url)).first()
        if url_old:
            return response(message=MessageEnum.test_environment_must_be_independent.value[1],
                           code=MessageEnum.test_environment_must_be_independent.value[0], data='')
        prkcyt = Project.query.filter_by(project_name=project).first()
        testevent = Interfacehuan(url=url, desc=desc, project=prkcyt.id,
                                  database=name,
                                  databaseuser=usernmae, databasepassword=password,
                                  dbhost=host,
                                  dbport=port, make_user=current_user.id)
        db.session.add(testevent)
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(message=MessageEnum.add_case_error, code=211)

    @login_required
    def put(self):
        data = request.get_json()
        json_data = data
        project = json_data['project']
        id = json_data['id']
        url = json_data['url']
        desc = json_data['desc']
        name = json_data['name']
        host = json_data['host']
        port = json_data['port']
        usernmae = json_data['username']
        password = json_data['password']
        project = Project.query.filter_by(project_name=project).first()
        event = Interfacehuan.query.filter_by(id=id).first()
        if not event:
            newevent = Interfacehuan(url=url, desc=desc, project=project.id,
                                     database=name,
                                     databaseuser=usernmae,
                                     databasepassword=password, dbhost=host,

                                     dbport=port, make_user=current_user.id)
            db.session.add(newevent)
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        event.url = url
        event.desc = desc
        event.database = name
        event.databaseuser = usernmae
        event.datebasepassword = password
        event.dbhost = host
        event.dbport = port
        event.project = project.id
        event.make_user = current_user.id
        try:
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return response(message=MessageEnum.edit_mock_error.value[1],
                           code=MessageEnum.edit_mock_error.value[0])

class MockViews(MethodView):
    @login_required
    def get(self, page=1):
        mock = Mockserver.query.filter_by(delete=False).order_by(
            Mockserver.id.desc()).paginate(page,
                                           per_page=int(PageShow),
                                           error_out=False)
        inter = mock.items
        return render_template('home/mockserver.html', inte=inter, pagination=mock)

    @login_required
    def post(self):
        data_post = request.get_json()
        name_exict = Mockserver.query.filter_by(name=data_post['name']).first()
        if name_exict:
            return response(code=MessageEnum.mock_name_only_one.value[0],
                           message=MessageEnum.mock_name_only_one.value[1])
        if data_post['checkout'] == u'是':
            is_check = True
        else:
            is_check = False
        if data_post['checkouheaders'] == u'是':
            is_headers = True
        else:
            is_headers = False
        if data_post['kaiqi'] == u'是':
            is_kaiqi = True
        else:
            is_kaiqi = False
        new_mock = Mockserver(name=data_post['name'])
        new_mock.make_uers = current_user.id
        new_mock.path = data_post['path']
        new_mock.methods = data_post['meth']
        new_mock.headers = data_post['headers']
        new_mock.description = data_post['desc']
        new_mock.fanhui = data_post['back']
        new_mock.params = data_post['parm']
        new_mock.rebacktype = data_post['type']
        new_mock.status = is_kaiqi
        new_mock.ischeck = is_check
        new_mock.is_headers = is_headers
        new_mock.update_time = datetime.datetime.now()
        db.session.add(new_mock)
        try:
            db.session.commit()
            return response(code=MessageEnum.success.value[0],
                           message=MessageEnum.success.value[1])
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return response(code=MessageEnum.create_mock_error.value[0],
                           message=MessageEnum.create_mock_error.value[1])

    @login_required
    def delete(self):
        data = request.data.decode('utf-8')
        ded = Mockserver.query.filter_by(id=data, status=False).first()
        if ded:
            ded.delete = True
            db.session.commit()
            return response(message=MessageEnum.success.value[1],
                           code=MessageEnum.success.value[0])
        return response(message=MessageEnum.delete_mock_error.value[1],
                       code=MessageEnum.delete_mock_error.value[0])

