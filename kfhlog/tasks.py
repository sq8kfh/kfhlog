from .models import Qso
from . import space_weather
import datetime


def update_sfi_kp(dbsession, redissession):
    if 'space_weather' in redissession:
        sp = redissession['space_weather']
    else:
        sp = space_weather.Space_weather()

    solar = sp.solar
    for qso in dbsession.query(Qso).filter(Qso.datetime_on >= solar[0]['date'], Qso.sfi == None):
        for s in solar:
            if qso.datetime_on.date() == s['date']:
                qso.sfi = s['sfi']
                break

    geo = sp.geomagnetic[:-1]
    for qso in dbsession.query(Qso).filter(Qso.datetime_on >= geo[0]['date'], Qso.k_index == None):
        for g in geo:
            if qso.datetime_on.date() == g['date']:
                qso.a_index = g['Ap']
                qso_time = qso.datetime_on.time()
                if qso_time <= datetime.time(3, 0, 0):
                    qso.k_index = g['Kp03']
                    break
                if qso_time <= datetime.time(6, 0, 0):
                    qso.k_index = g['Kp06']
                    break
                if qso_time <= datetime.time(9, 0, 0):
                    qso.k_index = g['Kp09']
                    break
                if qso_time <= datetime.time(12, 0, 0):
                    qso.k_index = g['Kp12']
                    break
                if qso_time <= datetime.time(15, 0, 0):
                    qso.k_index = g['Kp15']
                    break
                if qso_time <= datetime.time(18, 0, 0):
                    qso.k_index = g['Kp18']
                    break
                if qso_time <= datetime.time(21, 0, 0):
                    qso.k_index = g['Kp21']
                    break
                if qso_time <= datetime.time(24, 0, 0):
                    qso.k_index = g['Kp24']
                    break
