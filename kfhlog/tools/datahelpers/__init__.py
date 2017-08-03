from .helper import BaseHelper, DatetimeType, DateType, IntType, FloatType, StrType
from kfhlog.models.dbtools import formatters, dbhelpers, datatypes

def _dxcc_autocomplete(data, dbsession):
    if 'call' in data:
        return dbhelpers.dxcc_id_by_call(data['call'], dbsession)
    return None


def _band_autocomplete(data, dbsession):
    if 'freq' in data:
        return dbhelpers.band_id_by_freq(data['freq'], dbsession)
    return None


def _bandrx_autocomplete(data, dbsession):
    if 'freq_rx' in data:
        return dbhelpers.band_id_by_freq(data['freq_rx'], dbsession)
    return None


class QsoHelper(BaseHelper):
    profile = IntType(required=True, min_value=0)
    group = IntType(required=True, min_value=0)

    call = StrType(required=True, data_formatter=formatters.call_formatter)

    datetime_on = DatetimeType(required=True)
    datetime_off = DatetimeType()
    rst_rcvd = StrType(required=True)
    rst_sent = StrType(required=True)

    band = IntType(required=True, min_value=1, autocomplete_func=_band_autocomplete)
    band_rx = IntType(min_value=1, autocomplete_func=_bandrx_autocomplete)
    mode = IntType(required=True, min_value=1)
    mode_rx = IntType(min_value=1)

    freq = FloatType(min_value=0.000001)
    freq_rx = FloatType(min_value=0.000001)

    stx = IntType()
    srx = IntType()
    stx_string = StrType()
    srx_string = StrType()

    name = StrType()
    qth = StrType()

    gridsquare = StrType(min_length=2, max_length=8, data_formatter=formatters.gridsquare_formatter)

    dxcc = IntType(min_value=1, autocomplete_func=_dxcc_autocomplete)
    ituz = IntType(min_value=1, max_value=90)
    cqz = IntType(min_value=1, max_value=40)
    cont = StrType(one_of=[a.name for a in datatypes.ContinentEnum])

    iota = StrType(length=6)
    sota_ref = StrType(min_length=8, max_length=10)

    state = StrType()
    cnty = StrType()

    tx_pwr = FloatType(min_value=0.001)

    lotw_qslrdate = DateType()
    lotw_qslsdate = DateType()
    lotw_qsl_rcvd = StrType(one_of=[a.name for a in datatypes.RcvdEnum])
    lotw_qsl_sent = StrType(one_of=[a.name for a in datatypes.SentEnum])

    eqsl_qslrdate = DateType()
    eqsl_qslsdate = DateType()
    eqsl_qsl_rcvd = StrType(one_of=[a.name for a in datatypes.RcvdEnum])
    eqsl_qsl_sent = StrType(one_of=[a.name for a in datatypes.SentEnum])

    qslrdate = DateType()
    qslsdate = DateType()
    qsl_rcvd = StrType(one_of=[a.name for a in datatypes.RcvdEnum])
    qsl_sent = StrType(one_of=[a.name for a in datatypes.SentEnum])
    qsl_via = StrType()

    a_index = IntType(min_value=0)
    k_index = IntType(min_value=0, max_value=9)
    sfi = IntType(min_value=1)
    comment = StrType()
