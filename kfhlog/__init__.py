from pyramid.config import Configurator
from pyramid.renderers import JSON

from datetime import datetime
from enum import Enum

__version__ = "0.0.0"  # http://semver.org/


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('kfhlog:templates')

    renderer = JSON()
    renderer.add_adapter(datetime, lambda obj, request: obj.isoformat())
    renderer.add_adapter(Enum, lambda obj, request: obj.name)
    config.add_renderer('extjson', renderer)

    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
