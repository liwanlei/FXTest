# -*- coding: utf-8 -*-
# @Date    : 2017-08-14 20:58:13
# @Author  : lileilei
from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Permisson
def permission_required(permissions):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.can(permissions):
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
def admin_required(f):
    return permission_required(Permission.ADMINISTRATOR)(f)