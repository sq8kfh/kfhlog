from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
import colander

from ..models import Mode, Band, Dxcc


class QsoSchema(colander.Schema):
    call = colander.SchemaNode(colander.String())
    dxcc = colander.SchemaNode(colander.Int(),
                               validator=colander.Range(1, 600)
    )

@view_config(route_name='newqso', renderer='newqso.jinja2')
def newqso_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    #item = request.dbsession.query(Qso).get(13)

    class Qso:
        call = ''
        dxcc = None

    a = Qso()

   # schema = QsoSchema()
    #print(schema.serialize(a))
    #if schema.to_python(item):
        #form.bind(item)
    #    print('valid')
        # persist model somewhere...
        #return HTTPFound(location="/")
    #print(form)
    #print(dir(form))
    #return dict(item=item, form=FormRenderer(form))
    return {'modes': request.dbsession.query(Mode).all(),
            'bands': request.dbsession.query(Band).all(),
            'dxccs': request.dbsession.query(Dxcc.id, Dxcc.name).filter(Dxcc.deleted == False).order_by(Dxcc.name).all()}


"""
@view_config(route_name='newqso', request_method='POST', renderer='json')
jQuery.ajax({type:'POST',
             url: 'http://localhost:6543/', // the pyramid server
             data: JSON.stringify({'a':1}),
             contentType: 'application/json; charset=utf-8'});
"""