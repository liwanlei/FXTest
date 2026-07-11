# -*- coding: utf-8 -*-
"""
公共辅助函数，消除各视图模块中重复的项目权限过滤等逻辑。
"""
from flask_login import current_user
from app.models import Project, Model


def get_user_projects():
    """根据当前登录用户的权限返回可见的 Project 列表。

    超级管理员返回全部未删除项目；普通用户返回其权限范围内未删除项目。
    """
    if current_user.is_sper is True:
        return Project.query.filter_by(status=False).all()
    projects = []
    seen = []
    for q in current_user.quanxians:
        if q.projects in seen:
            continue
        if q.projects.status is False:
            projects.append(q.projects)
            seen.append(q.projects)
    return projects


def get_project_model():
    """返回全部未删除的 Project、Model 列表，供表单渲染使用。"""
    projects = Project.query.filter_by(status=False).all()
    models = Model.query.filter_by(status=False).all()
    return projects, models
