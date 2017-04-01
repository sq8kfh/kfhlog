from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Qso, Mode, Band, Dxcc

from .api import json_api_config


@json_api_config(name='get_log')
def _get_log(dbsession, data):
    qsos = dbsession.query(Qso)
    if 'call_filter' in data:
        qsos = qsos.filter(Qso.call.like(data['call_filter'] + '%'))

    # if 'datetime_off_filter' in data:
    #    qsos = qsos.filter_by(call=data['call_filter'])

    if 'band_filter' in data:
        qsos = qsos.filter_by(band=data['band_filter'])

    if 'mode_filter' in data:
        qsos = qsos.filter_by(mode=data['mode_filter'])

    if 'dxcc_filter' in data:
        qsos = qsos.filter_by(dxcc=data['dxcc_filter'])

    if 'sortby' in data:
        tmp = data['sortby']
        order_map = {
            'call': Qso.call,
            '-call': Qso.call.desc(),
            'datetime_off': Qso.datetime_off,
            '-datetime_off': Qso.datetime_off.desc(),
            'band': Qso.band,
            '-band': Qso.band.desc(),
            'mode': Qso.mode,
            '-mode': Qso.mode.desc(),
            'dxcc': Qso.dxcc,
            '-dxcc': Qso.dxcc.desc(),
        }
        if tmp in order_map:
            qsos = qsos.order_by(order_map[tmp])

    if 'pagesize' in data:
        try:
            pagesize = int(data['pagesize'])
            qsos = qsos.limit(pagesize)
            if 'page' in data:
                page = int(data['page'])
                qsos = qsos.offset((page-1)*pagesize)
        except ValueError as e:
            return {'status': 'error', 'response': 'ValueError'}
    return {'status': 'ok', 'log': qsos.all()}


@view_config(route_name='log', renderer='log.jinja2')
def log_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all()}
