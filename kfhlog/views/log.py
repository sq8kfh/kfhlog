import math
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from sqlalchemy import func

from ..models import Profile, Group, Qso, Mode, Band, Dxcc
from ..models.dbtools.datatypes import RcvdEnum, ModeEnum, ContinentEnum

from .api import json_api_config


@json_api_config(name='get_log')
def _get_log(request, data):
    dbsession = request.dbsession
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

    if 'freq_filter' in data:
        qsos = qsos.filter_by(freq=data['freq_filter'])
        count = count.filter_by(freq=data['freq_filter'])

    if 'name_filter' in data:
        qsos = qsos.filter(Qso.name.like(data['name_filter'] + '%'))
        count = count.filter(Qso.name.like(data['name_filter'] + '%'))

    if 'qth_filter' in data:
        qsos = qsos.filter(Qso.qth.like(data['qth_filter'] + '%'))
        count = count.filter(Qso.qth.like(data['qth_filter'] + '%'))

    if 'gridsquare_filter' in data:
        qsos = qsos.filter(Qso.gridsquare.like(data['gridsquare_filter'] + '%'))
        count = count.filter(Qso.gridsquare.like(data['gridsquare_filter'] + '%'))

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

    if 'iota_filter' in data:
        qsos = qsos.filter(Qso.iota.like(data['iota_filter'] + '%'))
        count = count.filter(Qso.iota.like(data['iota_filter'] + '%'))

    if 'sota_ref_filter' in data:
        qsos = qsos.filter(Qso.sota_ref.like(data['sota_ref_filter'] + '%'))
        count = count.filter(Qso.sota_ref.like(data['sota_ref_filter'] + '%'))

    if 'state_filter' in data:
        qsos = qsos.filter(Qso.state.like(data['state_filter'] + '%'))
        count = count.filter(Qso.state.like(data['state_filter'] + '%'))

    if 'cnty_filter' in data:
        qsos = qsos.filter(Qso.cnty.like(data['cnty_filter'] + '%'))
        count = count.filter(Qso.cnty.like(data['cnty_filter'] + '%'))

    if 'a_index_filter' in data:
        qsos = qsos.filter_by(a_index=data['a_index_filter'])
        count = count.filter_by(a_index=data['a_index_filter'])

    if 'k_index_filter' in data:
        qsos = qsos.filter_by(k_index=data['k_index_filter'])
        count = count.filter_by(k_index=data['k_index_filter'])

    if 'sfi_filter' in data:
        qsos = qsos.filter_by(sfi=data['sfi_filter'])
        count = count.filter_by(sfi=data['sfi_filter'])

    if 'lotw_qsl_rcvd_filter' in data:
        qsos = qsos.filter_by(lotw_qsl_rcvd=data['lotw_qsl_rcvd_filter'])
        count = count.filter_by(lotw_qsl_rcvd=data['lotw_qsl_rcvd_filter'])

    if 'eqsl_qsl_rcvd_filter' in data:
        qsos = qsos.filter_by(eqsl_qsl_rcvd=data['eqsl_qsl_rcvd_filter'])
        count = count.filter_by(eqsl_qsl_rcvd=data['eqsl_qsl_rcvd_filter'])

    if 'qsl_rcvd_filter' in data:
        qsos = qsos.filter_by(qsl_rcvd=data['qsl_rcvd_filter'])
        count = count.filter_by(qsl_rcvd=data['qsl_rcvd_filter'])

    if 'sortby' in data:
        tmp = data['sortby']
        order_map = {
            'profile': Qso.profile,
            '-profile': Qso.profile.desc(),
            'group': Qso.group,
            '-group': Qso.group.desc(),
            'call': Qso.call,
            '-call': Qso.call.desc(),
            'datetime_on': Qso.datetime_on,
            '-datetime_on': Qso.datetime_on.desc(),
            'datetime_off': Qso.datetime_off,
            '-datetime_off': Qso.datetime_off.desc(),
            'band': Qso.band,
            '-band': Qso.band.desc(),
            'mode': Qso.mode,
            '-mode': Qso.mode.desc(),
            'freq': Qso.freq,
            '-freq': Qso.freq.desc(),
            'name': Qso.name,
            '-name': Qso.name.desc(),
            'qth': Qso.qth,
            '-qth': Qso.qth.desc(),
            'gridsquare': Qso.gridsquare,
            '-gridsquare': Qso.gridsquare.desc(),
            'dxcc': Qso.dxcc,
            '-dxcc': Qso.dxcc.desc(),
            'cont': Qso.cont,
            '-cont': Qso.cont.desc(),
            'ituz': Qso.ituz,
            '-ituz': Qso.ituz.desc(),
            'cqz': Qso.cqz,
            '-cqz': Qso.cqz.desc(),
            'iota': Qso.iota,
            '-iota': Qso.iota.desc(),
            'sota_ref': Qso.sota_ref,
            '-sota_ref': Qso.sota_ref.desc(),
            'state': Qso.state,
            '-state': Qso.state.desc(),
            'cnty': Qso.cnty,
            '-cnty': Qso.cnty.desc(),
            'a_index': Qso.a_index,
            '-a_index': Qso.a_index.desc(),
            'k_index': Qso.k_index,
            '-k_index': Qso.k_index.desc(),
            'sfi': Qso.sfi,
            '-sfi': Qso.sfi.desc(),
            'lotw_qsl_rcvd': Qso.lotw_qsl_rcvd,
            '-lotw_qsl_rcvd': Qso.lotw_qsl_rcvd.desc(),
            'eqsl_qsl_rcvd': Qso.eqsl_qsl_rcvd,
            '-eqsl_qsl_rcvd': Qso.eqsl_qsl_rcvd.desc(),
            'qsl_rcvd': Qso.qsl_rcvd,
            '-qsl_rcvd': Qso.qsl_rcvd.desc(),
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


@json_api_config(name='set_log_preset')
def _set_log_preset(request, data):
    preset = {}
    if 'profile' in data:
        request.session['profile_preset'] = data['profile']
    if 'group' in data:
        request.session['group_preset'] = data['group']

    if 'show_profile' in data:
        preset['show_profile'] = data['show_profile']
    if 'show_group' in data:
        preset['show_group'] = data['show_group']
    if 'show_datetime_off' in data:
        preset['show_datetime_off'] = data['show_datetime_off']
    if 'show_band' in data:
        preset['show_band'] = data['show_band']
    if 'show_mode' in data:
        preset['show_mode'] = data['show_mode']
    if 'show_freq' in data:
        preset['show_freq'] = data['show_freq']
    if 'show_rst_rcvd' in data:
        preset['show_rst_rcvd'] = data['show_rst_rcvd']
    if 'show_rst_send' in data:
        preset['show_rst_send'] = data['show_rst_send']
    if 'show_name' in data:
        preset['show_name'] = data['show_name']
    if 'show_qth' in data:
        preset['show_qth'] = data['show_qth']
    if 'show_gridsquare' in data:
        preset['show_gridsquare'] = data['show_gridsquare']
    if 'show_dxcc' in data:
        preset['show_dxcc'] = data['show_dxcc']
    if 'show_cont' in data:
        preset['show_cont'] = data['show_cont']
    if 'show_ituz' in data:
        preset['show_ituz'] = data['show_ituz']
    if 'show_cqz' in data:
        preset['show_cqz'] = data['show_cqz']
    if 'show_iota' in data:
        preset['show_iota'] = data['show_iota']
    if 'show_sota_ref' in data:
        preset['show_sota_ref'] = data['show_sota_ref']
    if 'show_state' in data:
        preset['show_state'] = data['show_state']
    if 'show_cnty' in data:
        preset['show_cnty'] = data['show_cnty']
    if 'show_a_index' in data:
        preset['show_a_index'] = data['show_a_index']
    if 'show_k_index' in data:
        preset['show_k_index'] = data['show_k_index']
    if 'show_sfi' in data:
        preset['show_sfi'] = data['show_sfi']
    if 'show_lotw_qsl_rcvd' in data:
        preset['show_lotw_qsl_rcvd'] = data['show_lotw_qsl_rcvd']
    if 'show_eqsl_qsl_rcvd' in data:
        preset['show_eqsl_qsl_rcvd'] = data['show_eqsl_qsl_rcvd']
    if 'show_qsl_rcvd' in data:
        preset['show_qsl_rcvd'] = data['show_qsl_rcvd']

    request.session['log_preset'] = preset
    return {'status': 'ok'}


@view_config(route_name='log', renderer='log.jinja2', permission='authenticated')
def log_view(request):
    preset = {
        'show_profile': False,
        'show_group': False,
        'show_datetime_off': False,
        'show_band': True,
        'show_mode': True,
        'show_freq': False,
        'show_rst_rcvd': True,
        'show_rst_send': True,
        'show_name': False,
        'show_qth': False,
        'show_gridsquare': False,
        'show_dxcc': True,
        'show_cont': False,
        'show_ituz': False,
        'show_cqz': False,
        'show_iota': False,
        'show_sota_ref': False,
        'show_state': False,
        'show_cnty': False,
        'show_a_index': False,
        'show_k_index': False,
        'show_sfi': False,
        'show_lotw_qsl_rcvd': False,
        'show_eqsl_qsl_rcvd': False,
        'show_qsl_rcvd': False,
    }
    if 'log_preset' in request.session:
        preset.update(request.session['log_preset'])

    if 'profile' in request.GET:
        preset['profile'] = int(request.GET['profile'])
    elif 'profile_preset' in request.session:
        preset['profile'] = request.session['profile_preset']
    if 'group' in request.GET:
        preset['group'] = int(request.GET['group'])
    elif 'group_preset' in request.session:
        preset['group'] = request.session['group_preset']

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all(),
            'cont_all': [a.name for a in ContinentEnum],
            'preset': preset}
