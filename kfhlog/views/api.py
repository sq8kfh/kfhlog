from json.decoder import JSONDecodeError
from pyramid.view import view_config

from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text

from ..models import tools
from ..models import Qso, Mode, Band, Prefix

def _get_band(dbsession, data):
    freq = data['freq']
    band = dbsession.query(Band).filter(Band.lowerfreq <= freq, Band.upperfreq >= freq).first()
    if band:
        return {'status': 'ok', 'band': band.id}
    return {'status': 'error', 'response': 'band not found'}

def _get_previous(dbsession, data):
    call = tools.formatters.call_formatter(data['call'])
    qso = dbsession.query(Qso.date_on, Band.name, Mode.name)
    if 'profile' in data:
        qso = qso.filter_by(qsoprofile = data['profile'])
    if 'group' in data:
        qso = qso.filter_by(qsogroup = data['group'])
    qso = qso.filter_by(call = call).join(Band, Qso.band == Band.id).\
        join(Mode, Qso.mode == Mode.id).order_by(Qso.date_on).all()
    if qso:
        return {'status': 'ok', 'qso': qso}
    return {'status': 'ok', 'qso': []}

def _find_prefix(dbsession, data):
    call = tools.formatters.call_formatter(data['call'])
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

_function_dic = {
    'get_previous': _get_previous,
    'find_prefix': _find_prefix,
    'get_band': _get_band,
}

@view_config(route_name='api', request_method='POST', renderer='extjson')
def api_view(request):
    user = request.user
    if user is None:
        request.response.status = 401
        return {'status': 'error', 'message': 'unauthorized user'}
    api_func = request.matchdict['api_func']
    json_data = None
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
    json_data = None
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
