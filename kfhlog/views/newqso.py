from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Mode, Band, Dxcc

@view_config(route_name='newqso', renderer='newqso.jinja2')
def newqso_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'modes': request.dbsession.query(Mode).filter(Mode.hide == False).all(),
            'bands': request.dbsession.query(Band).filter(Band.hide == False).all(),
            'dxccs': request.dbsession.query(Dxcc.id, Dxcc.name).filter(Dxcc.deleted == False).order_by(Dxcc.name).all()}
