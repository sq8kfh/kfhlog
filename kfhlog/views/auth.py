from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='login.jinja2')
def login_view(request):
    next_url = request.params.get('next')
    if not next_url:
        next_url = request.route_path('index')
    message = ''
    if 'login' in request.params and 'password' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).get(login)
        if user is not None and user.check_password(password):
            headers = remember(request, user.name)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'
    return {'message': message, 'next_url': next_url}


@view_config(route_name='logout')
def logout_view(request):
    request.session.invalidate()
    headers = forget(request)
    next_url = request.route_url('login', _scheme='https')
    return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url}, _scheme='https')
    return HTTPFound(location=next_url)
