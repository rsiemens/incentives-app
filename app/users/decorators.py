from functools import wraps
from flask import g, redirect, url_for, request

from app.users.models import User, Incentive


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role == 0:
            return f(*args, **kwargs)
        return redirect(url_for('users.home', next=request.path))
    return decorated_function


def requires_staff(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role == 0 or g.user.role == 1:
            return f(*args, **kwargs)
        return redirect(url_for('users.home', next=request.path))
    return decorated_function


def get_incentives(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        incentives = g.user.incentives.all()
        if g.incentives is None:
            g.incentives = incentives[::-1]
        return f(*args, **kwargs)
    return decorated_function


def get_all_incentives(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (g.user.role == 0 or g.user.role == 1) and g.incentives is None:
            g.incentives = Incentive.query.all()[::-1]
            return f(*args, **kwargs)
    return decorated_function


def get_all_need_approval_incentives(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (g.user.role == 0 or g.user.role == 1) and g.incentives is None:
            g.incentives = Incentive.query.filter_by(approved=False).all()[::-1]
            return f(*args, **kwargs)
    return decorated_function


def get_users(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role == 0 and g.allusers is None:
            g.allusers = User.query.all()[::-1]
        return f(*args, **kwargs)
    return decorated_function
