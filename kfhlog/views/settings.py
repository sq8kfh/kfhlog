from pyramid.view import view_config
from .. import userconfig
from .api import json_api_config

@json_api_config(name='get_setting')
def _get_setting(request, data):
    set = data['name']
    if set in userconfig.settings_list:
        desc = userconfig.settings_list[set][-1]
        if userconfig.settings_list[set][1]:    #password
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
        if userconfig.settings_list[set][0]:  # read only
            return {'status': 'error', 'response': "read only setting"}
        if userconfig.settings_list[set][1]:  # password
            request.user_config.setpassword(set, val)
            return {'status': 'ok'}
        else:
            request.user_config.set(set, val)
            return {'status': 'ok'}
    else:
        return {'status': 'error', 'response': "setting not found"}


@view_config(route_name='settings', renderer='settings.jinja2', permission='authenticated')
def serrings_view(request):
    return {'settings_list': userconfig.settings_list}
