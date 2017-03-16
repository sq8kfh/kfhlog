from .helper import BaseHelper, EnumType, DatetimeType, IntType, FloatType, StrType
from kfhlog.models.dbtools import datatypes

class QsoHelper(BaseHelper):
    profile = IntType()
    group = IntType()

    call = StrType()

    datetime_on = DatetimeType()
    datetime_off = DatetimeType()
    rst_rcvd = StrType()
    rst_sent = StrType()

    band = IntType()
    band_rx = IntType()
    mode = IntType()
    mode_rx = IntType()

    freq = FloatType()
    freq_rx = FloatType()

    stx = IntType()
    srx = IntType()
    stx_string = StrType()
    srx_string = StrType()

    name = StrType()
    qth = StrType()

    gridsquare = StrType()

    dxcc = IntType()
    ituz = IntType()
    cqz = IntType()

    iota = StrType()
    sota_ref = StrType()

    state = StrType()
    cnty= StrType()

    tx_pwr = FloatType()

    lotw_qslrdate = DatetimeType()
    lotw_qslsdate = DatetimeType()
    lotw_qsl_rcvd = EnumType(datatypes.Rcvd_enum)
    lotw_qsl_sent = EnumType(datatypes.Send_enum)

    eqsl_qslrdate = DatetimeType()
    eqsl_qslsdate = DatetimeType()
    eqsl_qsl_rcvd = EnumType(datatypes.Rcvd_enum)
    eqsl_qsl_sent = EnumType(datatypes.Rcvd_enum)

    qslrdate = DatetimeType()
    qslsdate = DatetimeType()
    qsl_rcvd = EnumType(datatypes.Rcvd_enum)
    qsl_sent = EnumType(datatypes.Rcvd_enum)
    qsl_via = StrType()

    a_index = IntType()
    k_index = IntType()
    sfi = IntType()
    comment = StrType()
