import re
import hamutils.qrz

from pyramid.view import view_config

from ..models import Profile, Group, Mode, Band, Dxcc, State, Qso
from ..models.dbtools.datatypes import ContinentEnum

from .api import json_api_config

from ..tools import datahelpers


@json_api_config(name='get_state')
def _get_state(request, data):
    dbsession = request.dbsession
    if 'dxcc' in data and 'state' in data:
        dxcc = data['dxcc']
        code = data['state']
        state = dbsession.query(State).get((dxcc, code))
        if state:
            return {'status': 'ok', 'state': state.to_dict()}
    return {'status': 'error', 'response': 'dxcc/state not set'}


@json_api_config(name='addqso')
def _addqso(request, data):
    stx_string_org = None
    if 'stx_string' in data:
        stx_string_org = data['stx_string']
        data['stx_string'] = stx_string_org.replace("[", "").replace("]", "")
    qsoh = datahelpers.QsoHelper(data)

    vr = qsoh.validate()

    if vr['error']:
        return {'status': 'error', 'wrong_values': list(vr['error'].keys())}

    qn = qsoh.native()
    q = Qso(**qn)
    request.dbsession.add(q)

    preset = {}

    if 'profile' in qn:
        preset['profile'] = qn['profile']
    if 'group' in qn:
        preset['group'] = qn['group']
    if 'rst_rcvd' in qn:
        preset['rst_rcvd'] = qn['rst_rcvd']
    if 'rst_sent' in qn:
        preset['rst_sent'] = qn['rst_sent']
    if stx_string_org:
        stx_string_org = re.sub('\[([0-9]+)\]',
                                lambda x: ("[%0" + str(len(x.group(1))) + "d]") % (int(x.group(1)) + 1),
                                stx_string_org)
        preset['stx_string'] = stx_string_org
    if 'band' in qn:
        preset['band'] = qn['band']
    if 'mode' in qn:
        preset['mode'] = qn['mode']
    if 'freq' in qn:
        preset['freq'] = qn['freq']

    #print(request.session.new)
    # print(dir(request.session))

    request.session['newqso_preset'] = preset

    return {'status': 'ok', 'preset': preset}


@json_api_config(name='get_newqso_preset')
def _get_newqso_preset(request, data):
    preset = {}
    if 'newqso_preset' in request.session:
        preset = request.session['newqso_preset']
    return {'status': 'ok', 'preset': preset}


@json_api_config(name='reset_newqso_preset')
def _reset_newqso_preset(request, data):
    request.session['newqso_preset'] = {}
    return {'status': 'ok'}


@json_api_config(name='qrz_search')
def _qrz_search(request, data):
    user = request.user_config.get('qrzdotcom.username', None)
    password = request.user_config.getpassword('qrzdotcom.password', None)
    if user and password:
        qrz = hamutils.qrz.Qrz()
        call = data['call']

        try:
            qr = qrz.lookup(call, username=user, password=password)
        except hamutils.qrz.QrzException as e:
            return {'status': 'error', 'response': str(e)}

        res = {'status': 'ok'}

        if 'addr2' in qr:
            res['qth'] = qr['addr2']
        if 'state' in qr:
            res['state'] = qr['state']
        if 'fname' in qr:
            res['name'] = qr['fname']
        if 'name' in qr:
            if 'name' in res:
                res['name'] += ' '
                res['name'] += qr['name']
            else:
                res['name'] = qr['name']
        return res
    else:
        return {'status': 'error', 'response': "qrz.com user/password don't set"}


@view_config(route_name='newqso', renderer='newqso.jinja2', permission='authenticated')
def newqso_view(request):
    return {'profiles': request.dbsession.query(Profile).all(),
            'groups': request.dbsession.query(Group).all(),
            'modes': request.dbsession.query(Mode).filter(Mode.hide == False).all(),
            'bands': request.dbsession.query(Band).filter(Band.hide == False).all(),
            'conts': [a.name for a in ContinentEnum],
            'dxccs': request.dbsession.query(Dxcc.id, Dxcc.name).filter(Dxcc.deleted == False).order_by(Dxcc.name).all(),
            'mode_all': request.dbsession.query(Mode).all(),
            'band_all': request.dbsession.query(Band).all(),
            'dxcc_all': request.dbsession.query(Dxcc.id, Dxcc.name).order_by(Dxcc.name).all()}
