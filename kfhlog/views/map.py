from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Qso
from .api import json_api_config


@json_api_config(name='made_itu')
def _made_itu(dbsession, data):
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']


    itu = dbsession.query(Qso.ituz).filter(Qso.ituz.isnot(None))
    if profile:
        itu = itu.filter_by(profile=profile)
    if group:
        itu = itu.filter_by(group=group)

    itu = itu.group_by(Qso.ituz).all()

    return {'status': 'ok', 'itu': itu}


@view_config(route_name='map', renderer='map.jinja2', permission='authenticated')
def index_view(request):
    return {}
