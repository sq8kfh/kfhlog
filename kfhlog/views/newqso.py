from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Mode, Band, Dxcc, State
from ..models.dbtools.datatypes import ContinentEnum

from .api import json_api_config


@json_api_config(name='get_state')
def _get_state(dbsession, data):
    if 'dxcc' in data and 'state' in data:
        dxcc = data['dxcc']
        code = data['state']
        state = dbsession.query(State).get((dxcc, code))
        if state:
            return {'status': 'ok', 'state': state.to_dict()}
    return {'status': 'error', 'response': 'dxcc/state not set'}


@view_config(route_name='newqso', renderer='newqso.jinja2', permission='authenticated')
def newqso_view(request):
    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'modes': request.dbsession.query(Mode).filter(Mode.hide == False).all(),
            'bands': request.dbsession.query(Band).filter(Band.hide == False).all(),
            'conts': [a.name for a in ContinentEnum],
            'dxccs': request.dbsession.query(Dxcc.id, Dxcc.name).filter(Dxcc.deleted == False).order_by(Dxcc.name).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all()}
