import os
import uuid
import shutil
from hamtools import adif

from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from ..models import Qso, Band, Mode, Dxcc

def _adif2qso(adif, dbsession):
    mode_cache = {}
    band_cache = {}
    qsos = []
    for r in adif:
        qso_par = {}
        qso_par['qsoprofile'] = 0
        qso_par['qsogroup'] = 0
        if 'app_datetime_off' in r:
            qso_par['date_off'] = r['app_datetime_off']
        if 'app_datetime_on' in r:
            qso_par['date_on'] = r['app_datetime_on']
        if 'band' in r:
            tmp = r['band'].lower()
            print(tmp, band_cache)
            if tmp not in band_cache:
                band_cache[tmp] = dbsession.query(Band).filter_by(band=tmp).first().id
            qso_par['band'] = band_cache[tmp]
        elif 'freq' in r:
            freq = r['freq']
            qso_par['band'] = dbsession.query(Band).filter(Band.lowerfreq < freq, Band.upperfreq > freq).first().id
        if 'band_rx' in r:
            tmp = r['band_rx'].lower()
            if tmp not in band_cache:
                band_cache[tmp] = dbsession.query(Band).filter_by(band=tmp).first().id
            qso_par['band_rx'] = band_cache[tmp]
        elif 'freq_rx' in r:
            freq = r['freq_rx']
            qso_par['band'] = dbsession.query(Band).filter(Band.lowerfreq < freq, Band.upperfreq > freq).first().id
        if 'mode' in r:
            tmp = r['mode']
            if tmp not in mode_cache:
                mode_cache[tmp] = dbsession.query(Mode).filter_by(mode=tmp).first().id
            qso_par['mode'] = mode_cache[tmp]
        if 'mode_rx' in r:
            tmp = r['mode_rx']
            if tmp not in mode_cache:
                mode_cache[tmp] = dbsession.query(Mode).filter_by(mode=tmp).first().id
            qso_par['mode_rx'] = mode_cache[tmp]
        for v in ('call', 'rst_rcvd', 'rst_sent', 'freq', 'freq_rx', 'stx', 'srx', 'stx_string', 'srx_string', 'name', 'qth', 'gridsquare', 'dxcc', 'ituz', 'cqz', 'iota', 'sota_ref', 'state', 'cnty', 'tx_pwr', 'lotw_qslrdate', 'lotw_qslsdate', 'lotw_qsl_rcvd', 'lotw_qsl_sent', 'eqsl_qslrdate', 'eqsl_qslsdate', 'eqsl_qsl_rcvd', 'eqsl_qsl_sent', 'qslrdate', 'qslsdate', 'qsl_rcvd', 'qsl_sent', 'qsl_via', 'a_index', 'k_index', 'sfi', 'comment'):
            if v in r:
                qso_par[v] = r[v]

        qsos.append(qso_par)
    return qsos

@view_config(route_name='import', renderer='import.jinja2')
def import_view(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    if 'file' in request.params:
        file = request.params['file'].file

        tmp_file_path = os.path.join('/tmp', '%s' % uuid.uuid4())
        file.seek(0)
        with open(tmp_file_path, 'wb') as tmp_file:
            shutil.copyfileobj(file, tmp_file)

        with open(tmp_file_path, 'r') as adif_file:
            adif_data = adif.Reader(adif_file)
            dbsession = request.dbsession

            qsos = _adif2qso(adif_data, dbsession)
            for q in qsos:
                dbsession.add(Qso(**q))
            #dbsession.bulk_insert_mappings(Qso, qsos) #nie commituje tranzakcji - dlaczego?
            #dbsession.flush()
    return {}
