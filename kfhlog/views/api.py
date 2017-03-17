import re

from json.decoder import JSONDecodeError
from pyramid.view import view_config

from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text

from ..models import dbtools
from ..models import Qso, Mode, Band, Prefix

from ..tools import datahelpers


def _get_band(dbsession, data):
    freq = data['freq']
    band = dbsession.query(Band).filter(Band.lowerfreq <= freq, Band.upperfreq >= freq).first()
    if band:
        return {'status': 'ok', 'band': band.id}
    return {'status': 'error', 'response': 'band not found'}


def _get_previous(dbsession, data):
    call = dbtools.formatters.call_formatter(data['call'])
    qso = dbsession.query(Qso.datetime_on, Band.name, Mode.name)
    if 'profile' in data:
        qso = qso.filter_by(profile=data['profile'])
    if 'group' in data:
        qso = qso.filter_by(group=data['group'])
    qso = qso.filter_by(call=call).join(Band, Qso.band == Band.id).\
        join(Mode, Qso.mode == Mode.id).order_by(Qso.datetime_on).all()
    if qso:
        return {'status': 'ok', 'qso': qso}
    return {'status': 'ok', 'qso': []}


def _find_prefix(dbsession, data):
    call = dbtools.formatters.call_formatter(data['call'])
    prefix = dbsession.query(Prefix.dxcc, Prefix.ituz, Prefix.cqz, Prefix.continent).\
        filter(text(':param_call LIKE %s' % Prefix.prefix.name)).\
        params(param_call=call).order_by(func.length(Prefix.prefix).desc()).first()

    if prefix:
        return {'status': 'ok',
                'dxcc': prefix.dxcc,
                'ituz': prefix.ituz,
                'cqz': prefix.cqz,
                'continent': prefix.continent}
    return {'status': 'error', 'response': 'prefix not match'}


def _addqso(dbsession, data):
    stx_string_org = None
    if 'stx_string' in data:
        stx_string_org = data['stx_string']
        data['stx_string'] = stx_string_org.replace("[", "").replace("]", "")
    qsoh = datahelpers.QsoHelper(data)

    vr = qsoh.validate()

    if vr['error']:
        print(vr)
        return {'status': 'error', 'wrong_values': list(vr.keys())}

    qn = qsoh.native()
    q = Qso(**qn)
    dbsession.add(q)

    preset = {}

    if 'profile' in qn:
        preset['profile'] = qn['profile']
    if 'group' in qn:
        preset['group'] = qn['group']
    if 'rst_rcvd' in qn:
        preset['rst_rcvd'] = qn['rst_rcvd']
    if 'rst_sent' in qn:
        preset['rst_sent'] = qn['rst_sent']
    if stx_string_org:
        stx_string_org = re.sub('\[([0-9]+)\]',
                                lambda x: ("[%0" + str(len(x.group(1))) + "d]") % (int(x.group(1)) + 1),
                                stx_string_org)
        preset['stx_string'] = stx_string_org
    if 'band' in qn:
        preset['band'] = qn['band']
    if 'mode' in qn:
        preset['mode'] = qn['mode']
    if 'freq' in qn:
        preset['freq'] = qn['freq']

    return {'status': 'ok', 'preset': preset}

_function_dic = {
    'get_band': _get_band,
    'get_previous': _get_previous,
    'find_prefix': _find_prefix,
    'addqso': _addqso,
}


@view_config(route_name='api', request_method='POST', renderer='extjson')
def api_view(request):
    user = request.user
    if user is None:
        request.response.status = 401
        return {'status': 'error', 'message': 'unauthorized user'}
    api_func = request.matchdict['api_func']
    try:
        query_data = request.json_body
    except JSONDecodeError as e:
        request.response.status = 400
        return {'status': 'error', 'message': e.msg}

    if api_func in _function_dic:
        return _function_dic[api_func](request.dbsession, query_data)

    request.response.status = 404
    return {'status': 'error', 'message': 'function not found'}


@view_config(route_name='mapi', request_method='POST', renderer='extjson')
def mapi_view(request):
    user = request.user
    if user is None:
        request.response.status = 401
        return {'status': 'error', 'message': 'unauthorized user'}

    try:
        query_data = request.json_body
    except JSONDecodeError as e:
        request.response.status = 400
        return {'status': 'error', 'message': e.msg}

    res = {'status': 'ok'}
    for api_func in query_data:
        if api_func in _function_dic:
            res[api_func] = _function_dic[api_func](request.dbsession, query_data[api_func])
        else:
            res[api_func] = {'status': 'error', 'message': 'function not found'}

    return res
