import enum

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Enum,
)

from .meta import Base


class Rcvd_enum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    I = 4
    V = 5


class Send_enum(enum.Enum):
    Y = 1
    N = 2
    R = 3
    Q = 4
    I = 5

class Qso(Base):
    """ The SQLAlchemy declarative model class for a Qso object. """
    __tablename__ = 'qso'
    id = Column(Integer, primary_key=True)
    qsoprofile = Column(ForeignKey('profile.id'), nullable=False)
    qsogroup = Column(ForeignKey('group.id'), nullable=False)

    call = Column(String(length=20), nullable=False)
    date_on = Column(DateTime(timezone=False), nullable=True)
    date_off = Column(DateTime(timezone=False), nullable=False)
    rst_rcvd = Column(String(length=10), nullable=False)
    rst_sent = Column(String(length=10), nullable=False)

    band = Column(ForeignKey('band.id'), nullable=False)
    band_obj = relationship("Band", foreign_keys=band)
    band_rx = Column(ForeignKey('band.id'), nullable=True)
    band_rx_obj = relationship("Band", foreign_keys=band_rx)
    mode = Column(ForeignKey('mode.id'), nullable=False)
    mode_obj = relationship("Mode", foreign_keys=mode)
    mode_rx = Column(ForeignKey('mode.id'), nullable=True)
    band_rx_obj = relationship("Mode", foreign_keys=mode_rx)

    freq = Column(Float) #MHz
    freq_rx = Column(Float)

    stx = Column(Integer)
    srx = Column(Integer)
    stx_string = Column(String(length=10))
    srx_string = Column(String(length=10))

    name = Column(String(length=40))
    qth = Column(String(length=60))
    gridsquare = Column(String(length=8))

    dxcc = Column(ForeignKey('dxcc.id'))
    dxcc_obj = relationship("Dxcc", foreign_keys=dxcc)
    ituz = Column(Integer)
    cqz = Column(Integer)

    iota = Column(String(length=10))
    sota_ref = Column(String(length=10))

    state = Column(String(length=4)) #Primary Administrative Subdivision (e.g. US State, JA Island, VE Province)
    cnty= Column(String(length=4)) #Secondary Administrative Subdivision of contacted station (e.g. US county, JA Gun)

    tx_pwr = Column(Float)

    lotw_qslrdate = Column(DateTime(timezone=False))
    lotw_qslsdate = Column(DateTime(timezone=False))
    lotw_qsl_rcvd = Column(Enum(Rcvd_enum))
    lotw_qsl_sent = Column(Enum(Send_enum))

    eqsl_qslrdate = Column(DateTime(timezone=False))
    eqsl_qslsdate = Column(DateTime(timezone=False))
    eqsl_qsl_rcvd = Column(Enum(Rcvd_enum))
    eqsl_qsl_sent = Column(Enum(Send_enum))

    qslrdate = Column(DateTime(timezone=False))
    qslsdate = Column(DateTime(timezone=False))
    qsl_rcvd = Column(Enum(Rcvd_enum))
    #qsl_rcvd_via
    qsl_sent = Column(Enum(Send_enum))
    #qsl_sent_via
    qsl_via = Column(String(length=30))

    a_index = Column(Integer)
    k_index = Column(Integer)
    sfi = Column(Integer)
    comment = Column(String(length=200)) #notes