import re

from json.decoder import JSONDecodeError
from pyramid.view import view_config

from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text

from ..models import dbtools
from ..models import Qso, Mode, Band, Prefix


_function_dic = {}


def json_api_config(*, name):
    def decorator(func):
        assert name not in _function_dic
        _function_dic[name] = func
        return func
    return decorator


@json_api_config(name='get_band')
def _get_band(request, data):
    dbsession = request.dbsession
    freq = data['freq']
    band = dbsession.query(Band).filter(Band.lowerfreq <= freq, Band.upperfreq >= freq).first()
    if band:
        return {'status': 'ok', 'band': band.id}
    return {'status': 'error', 'response': 'band not found'}


@json_api_config(name='get_previous')
def _get_previous(request, data):
    dbsession = request.dbsession
    call = dbtools.formatters.call_formatter(data['call'])
    qso = dbsession.query(Qso.id, Qso.datetime_on, Band.name, Mode.name)
    if 'profile' in data:
        qso = qso.filter_by(profile=data['profile'])
    if 'group' in data:
        qso = qso.filter_by(group=data['group'])
    qso = qso.filter_by(call=call).join(Band, Qso.band == Band.id).\
        join(Mode, Qso.mode == Mode.id).order_by(Qso.datetime_on).all()
    if qso:
        return {'status': 'ok', 'qso': qso}
    return {'status': 'ok', 'qso': []}


@json_api_config(name='find_prefix')
def _find_prefix(request, data):
    dbsession = request.dbsession
    call = dbtools.formatters.call_formatter(data['call'])
    prefix = dbsession.query(Prefix.dxcc, Prefix.ituz, Prefix.cqz, Prefix.cont).\
        filter(text(':param_call LIKE %s' % Prefix.prefix.name)).\
        params(param_call=call).order_by(func.length(Prefix.prefix).desc()).first()

    if prefix:
        return {'status': 'ok',
                'dxcc': prefix.dxcc,
                'ituz': prefix.ituz,
                'cqz': prefix.cqz,
                'cont': prefix.cont}
    return {'status': 'error', 'response': 'prefix not match'}


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
        return _function_dic[api_func](request, query_data)

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
            res[api_func] = _function_dic[api_func](request, query_data[api_func])
        else:
            res[api_func] = {'status': 'error', 'message': 'function not found'}

    return res
