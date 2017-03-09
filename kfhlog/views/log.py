from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Qso

@view_config(route_name='log', renderer='log.jinja2')
def index_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    return {'qsos': request.dbsession.query(Qso).all()}
