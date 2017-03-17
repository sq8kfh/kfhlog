import os
import uuid
import shutil
from hamtools import adif

from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Qso, Profile, Group
from ..models.dbtools import dbhelpers
import kfhlog.tools.datahelpers

import logging
log = logging.getLogger(__name__)


def _adif2qso(qsoprofile, qsogroup, adif, dbsession):
    qsos = []
    wqso = []
    for r in adif:
        data = dict(r)
        if 'band' in r:
            data['band'] = dbhelpers.band_id_by_name(r['band'], dbsession)
        if 'band_rx' in r:
            data['band_rx'] = dbhelpers.band_id_by_name(r['band_rx'], dbsession)
        if 'mode' in r:
            data['mode'] = dbhelpers.mode_id_by_name(r['mode'], dbsession)
        if 'mode_rx' in r:
            data['mode_rx'] = dbhelpers.mode_id_by_name(r['mode_rx'], dbsession)
        qh = kfhlog.tools.datahelpers.QsoHelper(data,
                                                profile=qsoprofile,
                                                group=qsogroup,
                                                datetime_on=r['app_datetime_on'],
                                                datetime_off=r['app_datetime_off'])
        res = qh.validate(delete_incorrect=True)
        qh.autocomplete(dbsession)
        if res['error']:
            wqso.append((qh.native(), res['error']))
            log.error("Import error %s, %s - %s", qh.native()['call'], qh.native()['datetime_on'], res['error'])
        else:
            if res['warning']:
                log.warning("Import %s, %s - %s", qh.native()['call'], qh.native()['datetime_on'], res['warning'])
            print(qh.native())
            qsos.append(Qso(**qh.native()))
    return qsos, wqso


@view_config(route_name='import', renderer='import.jinja2')
def import_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    if 'profile' in request.params and 'group' in request.params and 'file' in request.params:
        file = request.params['file'].file

        tmp_file_path = os.path.join('/tmp', '%s' % uuid.uuid4())
        file.seek(0)
        with open(tmp_file_path, 'wb') as tmp_file:
            shutil.copyfileobj(file, tmp_file)

        with open(tmp_file_path, 'r', encoding="cp1250") as adif_file:
            adif_data = adif.Reader(adif_file)
            dbsession = request.dbsession

            qsos = _adif2qso(request.params['profile'], request.params['group'], adif_data, dbsession)

            dbsession.add_all(qsos[0])
            # dbsession.bulk_insert_mappings(Qso, qsos) #nie commituje tranzakcji - dlaczego?
            # dbsession.flush()
        return {'message': qsos[1], 'profiles': request.dbsession.query(Profile).all(),
                'groups': request.dbsession.query(Group).all()}
    return {'profiles': request.dbsession.query(Profile).all(), 'groups': request.dbsession.query(Group).all()}
