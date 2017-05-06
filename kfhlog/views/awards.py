from collections import OrderedDict

from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models.dbtools.datatypes import RcvdEnum, ModeEnum, ContinentEnum
from ..models import Profile, Group, Band, Mode, Qso, Dxcc
from .api import json_api_config


@json_api_config(name='award_general')
def _award_general(request, data):
    dbsession = request.dbsession
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']

    _band_low = 4
    _band_high = 13

    qsl = dbsession.query(Qso.cont, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    url_query = {}
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
        url_query['profile'] = profile
    if group is not None:
        qsl = qsl.filter_by(group=group)
        url_query['group'] = group

    qsl = qsl.filter(Qso.cont.isnot(None), Qso.band <= _band_high, Qso.band >= _band_low).\
        group_by(Qso.cont, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()

    cont = [a.name for a in ContinentEnum]

    res = OrderedDict()

    for c in cont:
        res[c] = [None] * (_band_high - _band_low + 2 + 3)
        tq = url_query.copy()
        tq.update({'cont': c})
        res[c][0] = {'data': c, 'href': request.route_url('log', _query=tq)}


    for q in qsl:
        if q.cont.name not in res:
            continue
        tmp = res[q.cont.name][q.band - _band_low + 1]
        if not tmp:
            tq = url_query.copy()
            tq.update({'cont': q.cont.name, 'band': q.band})
            tmp = {'data': '', 'href': request.route_url('log', _query=tq)}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        res[q.cont.name][q.band - _band_low + 1] = tmp

    qsl = dbsession.query(Qso.cont, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
    if group is not None:
        qsl = qsl.filter_by(group=group)

    qsl = qsl.filter(Qso.cont.isnot(None), Qso.band <= _band_high, Qso.band >= _band_low).\
        join(Qso.mode_obj).group_by(Qso.cont, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()
    for q in qsl:
        if q.cont.name not in res:
            continue
        tmp = None
        if q.mode_cat == ModeEnum.CW:
            tmp = res[q.cont.name][-3]
        elif q.mode_cat == ModeEnum.PHONE:
            tmp = res[q.cont.name][-2]
        elif q.mode_cat == ModeEnum.DIGITAL:
            tmp = res[q.cont.name][-1]
        else:
            continue
        if not tmp:
            tmp = {'data': ''}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        if q.mode_cat == ModeEnum.CW:
            res[q.cont.name][-3] = tmp
        elif q.mode_cat == ModeEnum.PHONE:
            res[q.cont.name][-2] = tmp
        elif q.mode_cat == ModeEnum.DIGITAL:
            res[q.cont.name][-1] = tmp

    return {'status': 'ok', 'general': list(res.values())}


@json_api_config(name='award_dxcc')
def _award_dxcc(request, data):
    dbsession = request.dbsession
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']

    _band_low = 4
    _band_high = 13

    qsl = dbsession.query(Qso.dxcc, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd)
    url_query = {}
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
        url_query['profile'] = profile
    if group is not None:
        qsl = qsl.filter_by(group=group)
        url_query['group'] = group

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        group_by(Qso.dxcc, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd).all()
    dxcc = dbsession.query(Dxcc.id, Dxcc.name).filter_by(deleted=False).all()

    res = OrderedDict()

    for dx in dxcc:
        res[dx.id] = [None]*(_band_high-_band_low+3+3)
        tq = url_query.copy()
        tq.update({'dxcc': dx.id})
        res[dx.id][0] = {'data': dx.id, 'href': request.route_url('log', _query=tq)}
        res[dx.id][1] = {'data': dx.name, 'href': request.route_url('log', _query=tq)}

    for q in qsl:
        if q.dxcc not in res:
            continue
        tmp = res[q.dxcc][q.band-_band_low+2]
        if not tmp:
            tq = url_query.copy()
            tq.update({'dxcc': q.dxcc, 'band': q.band})
            tmp = {'data': '', 'href': request.route_url('log', _query=tq)}
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        res[q.dxcc][q.band - _band_low + 2] = tmp

    qsl = dbsession.query(Qso.dxcc, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd)
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
    if group is not None:
        qsl = qsl.filter_by(group=group)

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        join(Qso.mode_obj).group_by(Qso.dxcc, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd).all()
    for q in qsl:
        if q.dxcc not in res:
            continue
        tmp = None
        if q.mode_cat == ModeEnum.CW:
            tmp = res[q.dxcc][-3]
        elif q.mode_cat == ModeEnum.PHONE:
            tmp = res[q.dxcc][-2]
        elif q.mode_cat == ModeEnum.DIGITAL:
            tmp = res[q.dxcc][-1]
        else:
            continue
        if not tmp:
            tmp = {'data': ''}
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        if q.mode_cat == ModeEnum.CW:
            res[q.dxcc][-3] = tmp
        elif q.mode_cat == ModeEnum.PHONE:
            res[q.dxcc][-2] = tmp
        elif q.mode_cat == ModeEnum.DIGITAL:
            res[q.dxcc][-1] = tmp

    return {'status': 'ok', 'dxcc': list(res.values())}


@json_api_config(name='award_cq')
def _award_cq(request, data):
    dbsession = request.dbsession
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']

    _band_low = 4
    _band_high = 13

    qsl = dbsession.query(Qso.cqz, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    url_query = {}
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
        url_query['profile'] = profile
    if group is not None:
        qsl = qsl.filter_by(group=group)
        url_query['group'] = group

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        group_by(Qso.cqz, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()
    cqz = list(range(1, 41))

    res = OrderedDict()

    for cq in cqz:
        res[cq] = [None]*(_band_high-_band_low+2+3)
        tq = url_query.copy()
        tq.update({'cqz': cq})
        res[cq][0] = {'data': cq, 'href': request.route_url('log', _query=tq)}

    for q in qsl:
        if q.cqz not in res:
            continue
        tmp = res[q.cqz][q.band-_band_low+1]
        if not tmp:
            tq = url_query.copy()
            tq.update({'cqz': q.cqz, 'band': q.band})
            tmp = {'data': '', 'href': request.route_url('log', _query=tq)}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        res[q.cqz][q.band - _band_low + 1] = tmp

    qsl = dbsession.query(Qso.cqz, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
    if group is not None:
        qsl = qsl.filter_by(group=group)

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        join(Qso.mode_obj).group_by(Qso.cqz, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()
    for q in qsl:
        if q.cqz not in res:
            continue
        tmp = None
        if q.mode_cat == ModeEnum.CW:
            tmp = res[q.cqz][-3]
        elif q.mode_cat == ModeEnum.PHONE:
            tmp = res[q.cqz][-2]
        elif q.mode_cat == ModeEnum.DIGITAL:
            tmp = res[q.cqz][-1]
        else:
            continue
        if not tmp:
            tmp = {'data': ''}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        if q.mode_cat == ModeEnum.CW:
            res[q.cqz][-3] = tmp
        elif q.mode_cat == ModeEnum.PHONE:
            res[q.cqz][-2] = tmp
        elif q.mode_cat == ModeEnum.DIGITAL:
            res[q.cqz][-1] = tmp

    return {'status': 'ok', 'cq': list(res.values())}


@json_api_config(name='award_itu')
def _award_itu(request, data):
    dbsession = request.dbsession
    profile = None
    group = None
    if 'profile' in data:
        profile = data['profile']
    if 'group' in data:
        group = data['group']

    _band_low = 4
    _band_high = 13

    qsl = dbsession.query(Qso.ituz, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    url_query = {}
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
        url_query['profile'] = profile
    if group is not None:
        qsl = qsl.filter_by(group=group)
        url_query['group'] = group

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        group_by(Qso.ituz, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()
    ituz = list(range(1, 91))

    res = OrderedDict()

    for itu in ituz:
        res[itu] = [None]*(_band_high-_band_low+2+3)
        tq = url_query.copy()
        tq.update({'ituz': itu})
        res[itu][0] = {'data': itu, 'href': request.route_url('log', _query=tq)}
    for q in qsl:
        if q.ituz not in res:
            continue
        tmp = res[q.ituz][q.band-_band_low+1]
        if not tmp:
            tq = url_query.copy()
            tq.update({'ituz': q.ituz, 'band': q.band})
            tmp = {'data': '', 'href': request.route_url('log', _query=tq)}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        res[q.ituz][q.band - _band_low + 1] = tmp

    qsl = dbsession.query(Qso.ituz, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd)
    if profile is not None:
        qsl = qsl.filter_by(profile=profile)
    if group is not None:
        qsl = qsl.filter_by(group=group)

    qsl = qsl.filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        join(Qso.mode_obj).group_by(Qso.ituz, Mode.mode_cat, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd, Qso.eqsl_qsl_rcvd).all()
    for q in qsl:
        if q.ituz not in res:
            continue
        tmp = None
        if q.mode_cat == ModeEnum.CW:
            tmp = res[q.ituz][-3]
        elif q.mode_cat == ModeEnum.PHONE:
            tmp = res[q.ituz][-2]
        elif q.mode_cat == ModeEnum.DIGITAL:
            tmp = res[q.ituz][-1]
        else:
            continue
        if not tmp:
            tmp = {'data': ''}
        if 'e' not in tmp['data']:
            if q.eqsl_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'e'
        if 'q' not in tmp['data']:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'q'
        if 'l' not in tmp['data']:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp['data'] += 'l'
        if q.mode_cat == ModeEnum.CW:
            res[q.ituz][-3] = tmp
        elif q.mode_cat == ModeEnum.PHONE:
            res[q.ituz][-2] = tmp
        elif q.mode_cat == ModeEnum.DIGITAL:
            res[q.ituz][-1] = tmp

    return {'status': 'ok', 'itu': list(res.values())}


@json_api_config(name='set_awards_preset')
def _set_awards_preset(request, data):
    if 'profile' in data:
        request.session['profile_preset'] = data['profile']
    if 'group' in data:
        request.session['group_preset'] = data['group']

    return {'status': 'ok'}


@view_config(route_name='awards', renderer='awards.jinja2', permission='authenticated')
def awards_view(request):
    _band_low = 4
    _band_high = 13

    qsl = request.dbsession.query(Qso.dxcc, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd).\
        filter(Qso.band <= _band_high, Qso.band >= _band_low).\
        group_by(Qso.dxcc, Qso.band, Qso.lotw_qsl_rcvd, Qso.qsl_rcvd).all()
    dxcc = request.dbsession.query(Dxcc.id, Dxcc.name).filter_by(deleted=False).all()

    res = OrderedDict()

    for dx in dxcc:
        res[dx.id] = [0]*(_band_high-_band_low+3)
        res[dx.id][0] = dx.id
        res[dx.id][1] = dx.name

    for q in qsl:
        if q.dxcc not in res:
            continue
        tmp = res[q.dxcc][q.band-_band_low+2]
        if tmp == 0:
            tmp = 1
        if tmp == 1 or tmp == 5:
            if q.qsl_rcvd == RcvdEnum.Y:
                tmp += 2
        if tmp < 5:
            if q.lotw_qsl_rcvd == RcvdEnum.Y:
                tmp += 4
        res[q.dxcc][q.band - _band_low + 2] = tmp

    preset = {}
    if 'profile_preset' in request.session:
        preset['profile'] = request.session['profile_preset']
    if 'group_preset' in request.session:
        preset['group'] = request.session['group_preset']

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'bands': request.dbsession.query(Band.name).filter(Band.id <= _band_high, Band.id >= _band_low).all(),
            'preset': preset}
