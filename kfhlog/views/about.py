import os
from pyramid.view import view_config
from docutils.core import publish_parts
from kfhlog import __version__


@view_config(route_name='about', renderer='about.jinja2')
def about_view(request):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '../../CHANGES.rst')) as f:
        changes = f.read()
    # ReStructuredText 2 html
    return {'version': __version__, 'changes': publish_parts(changes, writer_name='html')['html_body']}
