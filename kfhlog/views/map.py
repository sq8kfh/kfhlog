from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Qso
from .api import json_api_config


@json_api_config(name='made_itu')
def _made_itu(request, data):
    dbsession = request.dbsession
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']


    itu = dbsession.query(Qso.ituz).filter(Qso.ituz.isnot(None))
    if profile is not None:
        itu = itu.filter_by(profile=profile)
    if group is not None:
        itu = itu.filter_by(group=group)

    itu = itu.group_by(Qso.ituz).all()

    return {'status': 'ok', 'itu': itu}


@json_api_config(name='set_map_preset')
def _set_map_preset(request, data):
    if 'profile' in data:
        request.session['profile_preset'] = data['profile']
    if 'group' in data:
        request.session['group_preset'] = data['group']

    return {'status': 'ok'}


@view_config(route_name='map', renderer='map.jinja2', permission='authenticated')
def map_view(request):
    preset = {}
    if 'profile_preset' in request.session:
        preset['profile'] = request.session['profile_preset']
    if 'group_preset' in request.session:
        preset['group'] = request.session['group_preset']

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'preset': preset}
