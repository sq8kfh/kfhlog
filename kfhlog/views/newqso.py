from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Profile, Group, Mode, Band, Dxcc
from ..models.dbtools.datatypes import ContinentEnum

@view_config(route_name='newqso', renderer='newqso.jinja2')
def newqso_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'modes': request.dbsession.query(Mode).filter(Mode.hide == False).all(),
            'bands': request.dbsession.query(Band).filter(Band.hide == False).all(),
            'conts': [a.name for a in ContinentEnum],
            'dxccs': request.dbsession.query(Dxcc.id, Dxcc.name).filter(Dxcc.deleted == False).order_by(Dxcc.name).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all()}
