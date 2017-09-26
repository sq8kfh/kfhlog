import datetime
from pyramid.view import view_config
from .. import userconfig
from .api import json_api_config

@json_api_config(name='get_setting')
def _get_setting(request, data):
    set = data['name']
    if set in userconfig.settings_list:
        desc = userconfig.settings_list[set]['desc']
        if userconfig.settings_list[set]['password']:    #password
            tmp = request.user_config.getpassword('qrzdotcom.password', None)
            if tmp and tmp != '':
               return {'status': 'ok', 'name': set, 'value': '*****', 'desc': desc}
            else:
                return {'status': 'ok', 'name': set, 'value': None, 'desc': desc}
        else:
            return {'status': 'ok', 'name': set, 'value': request.user_config.get(set, None), 'desc': desc}
    else:
        return {'status': 'error', 'response': "setting not found"}


@json_api_config(name='set_setting')
def _set_setting(request, data):
    set = data['name']
    val = data['value']
    if set in userconfig.settings_list:
        if userconfig.settings_list[set]['ro']:  # read only
            return {'status': 'error', 'response': "read only setting"}
        if userconfig.settings_list[set]['password']:  # password
            request.user_config.setpassword(set, val)
            return {'status': 'ok'}
        else:
            request.user_config.set(set, val)
            return {'status': 'ok'}
    else:
        return {'status': 'error', 'response': "setting not found"}


@view_config(route_name='settings', renderer='settings.jinja2', permission='authenticated')
def serrings_view(request):
    settings_list = []
    for name in sorted(userconfig.settings_list.keys()):
        d = userconfig.settings_list[name]
        tmp = [name, None, d['ro'], d['password'], d['desc']]
        if d['password']:
            tmp[1] = '*****'
        else:
            tmp[1] = request.user_config.get(name, None)
            if name == 'kfhlog.db_create_date':
                t = datetime.datetime.strptime(tmp[1], "%Y-%m-%dT%H:%M:%S.%f")
                tmp[1] = t.strftime("%Y-%m-%d %H:%M:%S")
        settings_list.append(tmp)
    return {'settings_list': settings_list}
