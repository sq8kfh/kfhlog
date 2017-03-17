from kfhlog.models import Band, Mode, Prefix
from kfhlog.models.dbtools import formatters
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text


def band_id_by_name(name, dbsession):
    name = formatters.bandname_formatter(name)
    band = dbsession.query(Band.id).filter_by(name=name).first()
    if band:
        return band.id
    return None


def band_id_by_freq(freq, dbsession):
    freq = float(freq)
    band = dbsession.query(Band.id).filter(Band.lowerfreq <= freq, Band.upperfreq >= freq).first()
    if band:
        return band.id
    return None


def mode_id_by_name(name, dbsession):
    name = formatters.modename_formatter(name)
    mode = dbsession.query(Mode.id).filter_by(name=name).first()
    if mode:
        return mode.id
    return None


def dxcc_id_by_call(call, dbsession):
    call = formatters.call_formatter(call)
    prefix = dbsession.query(Prefix.dxcc).filter(text(':param_call LIKE %s' % Prefix.prefix.name)).\
        params(param_call=call).order_by(func.length(Prefix.prefix).desc()).first()
    if prefix:
        return prefix.dxcc
    return None
