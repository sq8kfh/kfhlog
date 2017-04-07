import math
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from sqlalchemy import func

from ..models import Profile, Group, Qso, Mode, Band, Dxcc
from ..models.dbtools.datatypes import RcvdEnum, ModeEnum, ContinentEnum

from .api import json_api_config


@json_api_config(name='get_log')
def _get_log(dbsession, data):
    qsos = dbsession.query(Qso)
    count = dbsession.query(func.count(Qso.id))
    if 'call_filter' in data:
        qsos = qsos.filter(Qso.call.like(data['call_filter'] + '%'))
        count = count.filter(Qso.call.like(data['call_filter'] + '%'))
    if 'profile' in data:
        profile = data['profile']
        qsos = qsos.filter_by(profile=profile)
        count = count.filter_by(profile=profile)
    if 'group' in data:
        group = data['group']
        qsos = qsos.filter_by(group=group)
        count = count.filter_by(group=group)

    # if 'datetime_off_filter' in data:
    #    qsos = qsos.filter_by(call=data['call_filter'])

    if 'band_filter' in data:
        qsos = qsos.filter_by(band=data['band_filter'])
        count = count.filter_by(band=data['band_filter'])

    if 'mode_filter' in data:
        qsos = qsos.filter_by(mode=data['mode_filter'])
        count = count.filter_by(mode=data['mode_filter'])

    if 'dxcc_filter' in data:
        qsos = qsos.filter_by(dxcc=data['dxcc_filter'])
        count = count.filter_by(dxcc=data['dxcc_filter'])

    if 'cont_filter' in data:
        qsos = qsos.filter_by(cont=data['cont_filter'])
        count = count.filter_by(cont=data['cont_filter'])

    if 'ituz_filter' in data:
        qsos = qsos.filter_by(ituz=data['ituz_filter'])
        count = count.filter_by(ituz=data['ituz_filter'])

    if 'cqz_filter' in data:
        qsos = qsos.filter_by(cqz=data['cqz_filter'])
        count = count.filter_by(cqz=data['cqz_filter'])

    if 'sortby' in data:
        tmp = data['sortby']
        order_map = {
            'call': Qso.call,
            '-call': Qso.call.desc(),
            'datetime_on': Qso.datetime_off,
            '-datetime_on': Qso.datetime_off.desc(),
            'datetime_off': Qso.datetime_off,
            '-datetime_off': Qso.datetime_off.desc(),
            'band': Qso.band,
            '-band': Qso.band.desc(),
            'mode': Qso.mode,
            '-mode': Qso.mode.desc(),
            'dxcc': Qso.dxcc,
            '-dxcc': Qso.dxcc.desc(),
            'cont': Qso.cont,
            '-cont': Qso.cont.desc(),
            'ituz': Qso.ituz,
            '-ituz': Qso.ituz.desc(),
            'cqz': Qso.cqz,
            '-cqz': Qso.cqz.desc(),
        }
        if tmp in order_map:
            qsos = qsos.order_by(order_map[tmp])

    count = count.scalar()
    pagesize = 1
    if 'pagesize' in data:
        try:
            pagesize = int(data['pagesize'])
            qsos = qsos.limit(pagesize)
            if 'page' in data:
                page = int(data['page'])
                qsos = qsos.offset((page-1)*pagesize)
        except ValueError as e:
            return {'status': 'error', 'response': 'ValueError'}
    return {'status': 'ok', 'log': qsos.all(), 'count': count, 'pagecount': math.ceil(count/pagesize)}


@view_config(route_name='log', renderer='log.jinja2', permission='authenticated')
def log_view(request):
    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all(),
            'cont_all': [a.name for a in ContinentEnum]}
