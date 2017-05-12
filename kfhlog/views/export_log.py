import os
import uuid

from hamutils.adif import ADIWriter, ADXWriter
from pyramid.response import FileResponse
from pyramid.view import view_config

from ..models import Profile, Group, Qso


@view_config(route_name='export', request_method='GET', renderer='export.jinja2', permission='authenticated')
def export_view(request):
    return {'profiles': request.dbsession.query(Profile).all(), 'groups': request.dbsession.query(Group).all()}


@view_config(route_name='export', request_method='POST', permission='authenticated')
def export_postview(request):
    print(request.POST['adif_type'])
    if request.POST['adif_type'] == 'adi':
        ADIFWriter = ADIWriter
    else:
        ADIFWriter = ADXWriter

    tmp_file_path = os.path.join('/tmp', '%s' % uuid.uuid4())

    with open(tmp_file_path, 'wb') as tmp_file:
        from kfhlog import __version__ as kfhlog_version
        adif = ADIFWriter(tmp_file, 'kfhlog', kfhlog_version)
        qsos = request.dbsession.query(Qso).order_by(Qso.datetime_on)

        if 'profile' in request.POST and request.POST['profile'] !='':
            qsos = qsos.filter_by(profile=request.POST['profile'])
        if 'group' in request.POST and request.POST['group'] !='':
            qsos = qsos.filter_by(profile=request.POST['group'])

        for qso in qsos:
            tmp = qso.to_dict()
            del tmp['id']

            tmp['app_kfhlog_profile'] = tmp['profile']
            del tmp['profile']
            tmp['app_kfhlog_group'] = tmp['group']
            del tmp['group']

            prof = qso.profile_obj

            if prof.call:
                tmp['station_callsign'] = prof.call
            if prof.op_name:
                tmp['my_name'] = prof.op_name
            if prof.gridsquare:
                tmp['my_gridsquare'] = prof.gridsquare
            if prof.dxcc:
                tmp['my_dxcc'] = prof.dxcc
            if prof.ituz:
                tmp['my_itu_zone'] = prof.ituz
            if prof.cqz:
                tmp['my_cq_zone'] = prof.cqz
            if prof.iota:
                tmp['my_iota'] = prof.iota
            if prof.sota_ref:
                tmp['my_sota_ref'] = prof.sota_ref
            if prof.state:
                tmp['my_state'] = prof.state
            if prof.cnty:
                tmp['my_cnty'] = prof.cnty
            if prof.qth:
                tmp['my_city'] = prof.qth

            def test(data):
                if data is None:
                    return False
                elif isinstance(data, str) and data == '':
                    return False
                return True

            tmp = {k: v for k, v in tmp.items() if test(v)}
            if 'band' in tmp:
                tmp['band'] = qso.band_obj.name
            if 'band_rx' in tmp:
                tmp['band_rx'] = qso.band_rx_obj.name
            if 'mode' in tmp:
                tmp['mode'] = qso.mode_obj.name
            if 'mode_rx' in tmp:
                tmp['mode_rx'] = qso.mode_rx_obj.name
            adif.add_qso(**tmp)
        adif.close()
    response = FileResponse(tmp_file_path)
    if request.POST['adif_type'] == 'adi':
        response.content_type = 'text/plain'
        response.headers['Content-Disposition'] = "attachment; filename=export.adi"
    else:
        response.content_type = 'text/xml'
        response.headers['Content-Disposition'] = "attachment; filename=export.adx"
    return response
