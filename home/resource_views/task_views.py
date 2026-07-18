# -*- coding: utf-8 -*-
"""task_views 视图。"""
from flask import flash

from app import db
from app.home.resource_views._shared import *  # noqa: F401,F403

class TimingtasksView(MethodView):
    @login_required
    def get(self, page=1):
        if current_user.is_sper is True:
            task = []
            task.append(Task.query.filter_by(status=False).order_by(Task.id.desc()).all())
        else:
            task = []
            id = []
            for project in current_user.quanxians:
                if (project.projects.id in id) is False:
                    task.append(Task.query.filter_by(prject=project.projects.id,
                                                     status=False).all())
                    id.append(project.projects.id)
        old_yask = flatten_list(task)
        projects_list = fenye_list(Ob_list=old_yask, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        try:
            paged_data = projects_list[int(page) - 1]
            return render_template('home/timingtask.html', inte=paged_data, pages=pages)
        except Exception as e:
            logger.error(e)
            return redirect(url_for('home.timingtask'))

class GetProtestReportView(MethodView):
    @login_required
    def post(self):
        id = request.get_data('id')
        project = id.decode('utf-8')
        if not project:
            return response(message=MessageEnum.error_send_message.value[1],
                           code=MessageEnum.error_send_message.value[0], data='')
        project_is = Project.query.filter_by(project_name=project).first()
        if not project_is:
            return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0], data=[])
        testreport = TestResult.query.filter_by(projects_id=project_is.id,
                                                status=False).order_by(
            TestResult.id.desc()).all()
        testreportlist = []
        for test in testreport:
            testreportlist.append({'test_num': test.test_num, 'pass_num': test.pass_num,
                                   'fail_num': test.fail_num,
                                   'hour_time': str(test.hour_time),
                                   'test_rep': test.test_rep, 'test_log': test.test_log,
                                   'Exception_num': test.Exception_num,
                                   'can_num': test.can_num,
                                   'wei_num': test.wei_num,
                                   'test_time': str(test.test_time),
                                   'Test_user_id': test.users.username, 'id': test.id,
                                   'fenshu': test.pass_num / test.test_num})
        return response(message=MessageEnum.success.value[1], code=MessageEnum.success.value[0], data=(testreportlist))

class GenconfigView(MethodView):
    @login_required
    def get(self, page=1):
        genconfiglist = GeneralConfiguration.query.filter_by(status=False).order_by(
            GeneralConfiguration.id.desc()).all()
        projects_list = fenye_list(Ob_list=genconfiglist, split=PageShow)
        pages = range(1, len(projects_list) + 1)
        try:
            paged_data = projects_list[int(page) - 1]
            return render_template('home/genconfig.html', inte=paged_data, pages=pages)
        except Exception as e:
            logger.error(e)
            return redirect(url_for('home.genconfig'))

class DeleteGenconfigView(MethodView):
    @login_required
    def get(self, id):
        gencofigilist = GeneralConfiguration.query.filter_by(id=id, status=False).first()
        if not gencofigilist:
            flash(MessageEnum.config_not_exict.value[1])
        gencofigilist.status = True
        try:
            db.session.commit()
            flash(MessageEnum.success.value[1])
            return redirect(url_for('home.genconfig'))
        except Exception as e:
            logger.error('删除配置失败！原因：%s' % e)
            db.session.rollback()
            flash(MessageEnum.config_delete_error.value[1])
            return redirect(url_for('home.genconfig'))

