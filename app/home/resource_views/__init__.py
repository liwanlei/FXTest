# -*- coding: utf-8 -*-
"""资源视图包，统一导出所有视图类。"""
from app.home.resource_views.interface_views import *  # noqa: F401,F403
from app.home.resource_views.project_views import *  # noqa: F401,F403
from app.home.resource_views.admin_views import *  # noqa: F401,F403
from app.home.resource_views.env_views import *  # noqa: F401,F403
from app.home.resource_views.task_views import *  # noqa: F401,F403

__all__ = [
    'InterfaceView',
    'CaseView',
    'ProjectView',
    'ModelView',
    'AdminUserView',
    'TestResultView',
    'TestenvironmentView',
    'MockViews',
    'TimingtasksView',
    'GetProtestReportView',
    'GenconfigView',
    'DeleteGenconfigView',
]
