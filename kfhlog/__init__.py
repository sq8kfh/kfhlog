from pyramid.config import Configurator
from pyramid.renderers import JSON

from datetime import datetime, date
from enum import Enum

from .models import Qso

__version__ = "0.0.0"  # http://semver.org/


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('kfhlog:templates')

    renderer = JSON()
    renderer.add_adapter(datetime, lambda obj, request: obj.isoformat())
    renderer.add_adapter(date, lambda obj, request: obj.isoformat())
    renderer.add_adapter(Enum, lambda obj, request: obj.name)
    renderer.add_adapter(Qso, lambda obj, request: obj.ext_to_dict())
    config.add_renderer('extjson', renderer)

    config.include('pyramid_rpc.xmlrpc')
    config.add_settings({'redis.sessions.client_callable': 'kfhlog.redis.get_redis_client'})
    config.include('pyramid_redis_sessions')

    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.include('.redis')
    config.include('.userconfig')
    config.scan()
    return config.make_wsgi_app()
