from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from ..models import Qso, Band, Mode, Profile, dbtools


def _check(dbsession, call, profile=None):
    call = dbtools.formatters.call_formatter(call)
    tmp = None
    req_type = None
    addrowlink = False
    name = ''
    if profile:
        req_type = Mode
        name = dbsession.query(Profile).get(profile).name
        tmp = dbsession.query(Qso.mode, Qso.band).group_by(Qso.mode, Qso.band).\
            filter_by(call=call, profile=profile).all()
    else:
        req_type = Profile
        addrowlink = True
        tmp = dbsession.query(Qso.profile, Qso.band).group_by(Qso.profile, Qso.band).filter_by(call=call).all()
    if not tmp:
        return {'message': 'Call %s is not in the log...' % call}
    col = {x[1] for x in tmp}
    col = col.union([5, 7, 8, 9, 10, 11, 12, 13])  #always show 80m-10m band
    col = sorted(col)
    row = {x[0] for x in tmp}
    row = sorted(row)
    res = {}
    for r, c in tmp:
        res[(r, c)] = True

    rowh = {id: dbsession.query(req_type).get(id).name for id in row}
    colh = [dbsession.query(Band).get(id).name for id in col]
    return {'call': call, 'name': name, 'res': res, 'col': col, 'row': row,
            'rowh': rowh, 'colh': colh, 'addrowlink': addrowlink}


@view_config(route_name='checkwp', renderer='check.jinja2')
def checkwp_view(request):
    profile = request.matchdict['profile']
    tmp = request.dbsession.query(Profile).get(profile)
    if not tmp:
        raise HTTPNotFound()
    if 'call' in request.params:
        call = request.params['call']
        return _check(request.dbsession, call, profile)
    return {}


@view_config(route_name='check', renderer='check.jinja2')
def check_view(request):
    if 'call' in request.params:
        call = request.params['call']
        if 'profile' in request.params:
            profile = request.params['profile']
            return _check(request.dbsession, call, profile)
        return _check(request.dbsession, call)
    return {}
