from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Enum,
    Text,
)

from .meta import Base
from .dbtools import datatypes
from .dbtools import formatters

class Qso(Base):
    """ The SQLAlchemy declarative model class for a Qso object. """
    __tablename__ = 'qso'
    id = Column(Integer, primary_key=True)
    profile = Column(ForeignKey('profile.id'), nullable=False)
    group = Column(ForeignKey('group.id'), nullable=False)

    _call = Column('call', String(length=20), nullable=False)

    @hybrid_property
    def call(self):
        return self._call

    @call.setter
    def call(self, value):
        self._call = formatters.call_formatter(value)

    datetime_on = Column(DateTime(timezone=False), nullable=False)
    datetime_off = Column(DateTime(timezone=False), nullable=True)
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
    stx_string = Column(String(length=10), nullable=False, server_default='')
    srx_string = Column(String(length=10), nullable=False, server_default='')

    name = Column(Text, nullable=False, server_default='')
    qth = Column(Text, nullable=False, server_default='')

    _gridsquare = Column('gridsquare', String(length=8), nullable=False, server_default='')

    @hybrid_property
    def gridsquare(self):
        return self._gridsquare

    @gridsquare.setter
    def gridsquare(self, value):
        self._gridsquare = formatters.gridsquare_formatter(value)

    dxcc = Column(ForeignKey('dxcc.id'), nullable=True)
    dxcc_obj = relationship("Dxcc", foreign_keys=dxcc)
    ituz = Column(Integer)
    cqz = Column(Integer)

    iota = Column(String(length=10), nullable=False, server_default='')
    sota_ref = Column(String(length=10), nullable=False, server_default='')

    state = Column(String(length=4), nullable=False, server_default='') #Primary Administrative Subdivision (e.g. US State, JA Island, VE Province)
    cnty= Column(String(length=4), nullable=False, server_default='') #Secondary Administrative Subdivision of contacted station (e.g. US county, JA Gun)

    tx_pwr = Column(Float)

    lotw_qslrdate = Column(DateTime(timezone=False))
    lotw_qslsdate = Column(DateTime(timezone=False))
    lotw_qsl_rcvd = Column(Enum(datatypes.Rcvd_enum), nullable=False, server_default='N')
    lotw_qsl_sent = Column(Enum(datatypes.Send_enum), nullable=False, server_default='N')

    eqsl_qslrdate = Column(DateTime(timezone=False))
    eqsl_qslsdate = Column(DateTime(timezone=False))
    eqsl_qsl_rcvd = Column(Enum(datatypes.Rcvd_enum), nullable=False, server_default='N')
    eqsl_qsl_sent = Column(Enum(datatypes.Send_enum), nullable=False, server_default='N')

    qslrdate = Column(DateTime(timezone=False))
    qslsdate = Column(DateTime(timezone=False))
    qsl_rcvd = Column(Enum(datatypes.Rcvd_enum), nullable=False, server_default='N')
    #qsl_rcvd_via
    qsl_sent = Column(Enum(datatypes.Send_enum), nullable=False, server_default='N')
    #qsl_sent_via
    qsl_via = Column(String(length=30), nullable=False, server_default='')

    a_index = Column(Integer)
    k_index = Column(Integer)
    sfi = Column(Integer)
    comment = Column(Text, nullable=False, server_default='') #notes