__all__ = ['tasks']

import subprocess
import os
from pyramid.config import Configurator
from pyramid.renderers import JSON

from datetime import datetime, date
from enum import Enum

from .models import Qso

__version__ = None  # http://semver.org/

def set_version():
    global __version__
    path = os.path.dirname(__file__)
    o = subprocess.check_output(['git', 'describe', '--long', '--dirty', '--always'], cwd=path).decode("utf-8").rstrip()
    __version__ = o

if not __version__:
    try:
        set_version()
    except subprocess.CalledProcessError as e:
        __version__ = '0.0.0'

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('kfhlog:templates')

    renderer = JSON()
    renderer.add_adapter(datetime, lambda obj, request: obj.isoformat()+'Z')
    renderer.add_adapter(date, lambda obj, request: obj.isoformat())
    renderer.add_adapter(Enum, lambda obj, request: obj.name)
    renderer.add_adapter(Qso, lambda obj, request: obj.ext_to_dict())
    config.add_renderer('extjson', renderer)

    config.include('pyramid_rpc.xmlrpc')
    config.add_settings({'redis.sessions.client_callable': 'kfhlog.redis.get_redis_client'})
    config.include('pyramid_redis_sessions')

    config.include('pyramid_celery')
    config.configure_celery(global_config['__file__'])

    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.include('.redis')
    config.include('.userconfig')
    config.scan()
    return config.make_wsgi_app()
