from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from ..space_weather import Space_weather


@view_config(route_name='index', renderer='index.jinja2', permission='authenticated')
def index_view(request):
    if 'space_weather' in request.redis:
        sp = request.redis['space_weather']
        pre = sp.predictions
        sol = sp.solar[-3:]
        geo = sp.geomagnetic[-3:]

        return {'predictions': pre,
                'solar': sol,
                'geomagnetic': geo}
    else:
        return {'predictions': [],
                'solar': [],
                'geomagnetic': []}

db_err_msg = """\
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'kfhlog'}
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_kfhlog_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""