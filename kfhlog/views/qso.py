from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Mode, Band, Dxcc, Qso
from ..models.dbtools.datatypes import ContinentEnum
from .api import json_api_config


@json_api_config(name='get_qso')
def _get_qso(dbsession, data):
    if 'id' in data:
        id = data['id']
        qso = dbsession.query(Qso).get(id)
        if qso:
            return {'status': 'ok', 'qso': qso.to_dict()}
        return {'status': 'error', 'response': 'qso #%s not found' % id}
    return {'status': 'error', 'response': 'qso id not set'}


@json_api_config(name='update_qso')
def _update_qso(dbsession, data):
    if 'id' in data:
        id = data.pop('id')
        qso = dbsession.query(Qso).get(id)
        if not qso:
            return {'status': 'error', 'response': 'qso #%s not found' % id}

        for k in data:
            setattr(qso, k, data[k])

        return {'status': 'ok', 'qso': qso.to_dict()}

    return {'status': 'error', 'response': 'qso id not set'}


@json_api_config(name='del_qso')
def _del_qso(dbsession, data):
    if 'id' in data:
        id = data['id']
        dbsession.query(Qso).filter_by(id=id).delete()
        return {'status': 'ok'}
    return {'status': 'error', 'response': 'qso id not set'}


@view_config(route_name='qso', renderer='qso.jinja2')
def qso_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    qsoid = request.matchdict['qsoid']

    return {'qsoid': qsoid,
            'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'conts': [a.name for a in ContinentEnum],
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all()}
