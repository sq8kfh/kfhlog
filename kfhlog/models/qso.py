from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import class_mapper
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

import datetime
import dateutil.parser

from .meta import Base
from .dbtools import datatypes
from .dbtools import formatters


class Qso(Base):
    """ The SQLAlchemy declarative model class for a Qso object. """
    __tablename__ = 'qsos'
    id = Column(Integer, primary_key=True)
    profile = Column(ForeignKey('profiles.id'), nullable=False)
    profile_obj = relationship("Profile", foreign_keys=profile)
    group = Column(ForeignKey('groups.id'), nullable=False)
    group_obj = relationship("Group", foreign_keys=group)

    _call = Column('call', String(length=20), nullable=False)

    @hybrid_property
    def call(self):
        return self._call

    @call.setter
    def call(self, value):
        self._call = formatters.call_formatter(value)

    _datetime_on = Column('datetime_on', DateTime(timezone=False), nullable=False)

    @hybrid_property
    def datetime_on(self):
        return self._datetime_on

    @datetime_on.setter
    def datetime_on(self, value):
        if isinstance(value, datetime.datetime):
            self._datetime_on = value
        else:
            self._datetime_on = dateutil.parser.parse(value)

    _datetime_off = Column('datetime_off', DateTime(timezone=False), nullable=True)

    @hybrid_property
    def datetime_off(self):
        return self._datetime_off

    @datetime_off.setter
    def datetime_off(self, value):
        if isinstance(value, datetime.datetime):
            self._datetime_off = value
        else:
            self._datetime_off = dateutil.parser.parse(value)

    rst_rcvd = Column(String(length=10), nullable=False)
    rst_sent = Column(String(length=10), nullable=False)

    band = Column(ForeignKey('bands.id'), nullable=False)
    band_obj = relationship("Band", foreign_keys=band)
    band_rx = Column(ForeignKey('bands.id'), nullable=True)
    band_rx_obj = relationship("Band", foreign_keys=band_rx)
    mode = Column(ForeignKey('modes.id'), nullable=False)
    mode_obj = relationship("Mode", foreign_keys=mode)
    mode_rx = Column(ForeignKey('modes.id'), nullable=True)
    mode_rx_obj = relationship("Mode", foreign_keys=mode_rx)

    freq = Column(Float)  # MHz
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
    cont = Column(Enum(datatypes.ContinentEnum))

    iota = Column(String(length=10), nullable=False, server_default='')
    sota_ref = Column(String(length=10), nullable=False, server_default='')

    # Primary Administrative Subdivision (e.g. US State, JA Island, VE Province)
    state = Column(String(length=4), nullable=False, server_default='')
    # Secondary Administrative Subdivision of contacted station (e.g. US county, JA Gun)
    cnty = Column(String(length=4), nullable=False, server_default='')

    tx_pwr = Column(Float)

    _lotw_qslrdate = Column('lotw_qslrdate', DateTime(timezone=False))

    @hybrid_property
    def lotw_qslrdate(self):
        return self._lotw_qslrdate

    @lotw_qslrdate.setter
    def lotw_qslrdate(self, value):
        if isinstance(value, datetime.datetime):
            self._lotw_qslrdate = value
        else:
            self._lotw_qslrdate = dateutil.parser.parse(value)

    _lotw_qslsdate = Column('lotw_qslsdate', DateTime(timezone=False))

    @hybrid_property
    def lotw_qslsdate(self):
        return self._lotw_qslsdate

    @lotw_qslsdate.setter
    def lotw_qslsdate(self, value):
        if isinstance(value, datetime.datetime):
            self._lotw_qslsdate = value
        else:
            self._lotw_qslsdate = dateutil.parser.parse(value)

    lotw_qsl_rcvd = Column(Enum(datatypes.RcvdEnum), nullable=False, server_default='N')
    lotw_qsl_sent = Column(Enum(datatypes.SendEnum), nullable=False, server_default='N')

    _eqsl_qslrdate = Column('eqsl_qslrdate', DateTime(timezone=False))

    @hybrid_property
    def eqsl_qslrdate(self):
        return self._eqsl_qslrdate

    @eqsl_qslrdate.setter
    def eqsl_qslrdate(self, value):
        if isinstance(value, datetime.datetime):
            self._eqsl_qslrdate = value
        else:
            self._eqsl_qslrdate = dateutil.parser.parse(value)

    _eqsl_qslsdate = Column('eqsl_qslsdate', DateTime(timezone=False))

    @hybrid_property
    def eqsl_qslsdate(self):
        return self._eqsl_qslsdate

    @eqsl_qslsdate.setter
    def eqsl_qslsdate(self, value):
        if isinstance(value, datetime.datetime):
            self._eqsl_qslsdate = value
        else:
            self._eqsl_qslsdate = dateutil.parser.parse(value)

    eqsl_qsl_rcvd = Column(Enum(datatypes.RcvdEnum), nullable=False, server_default='N')
    eqsl_qsl_sent = Column(Enum(datatypes.SendEnum), nullable=False, server_default='N')

    _qslrdate = Column('qslrdate', DateTime(timezone=False))

    @hybrid_property
    def qslrdate(self):
        return self._qslrdate

    @qslrdate.setter
    def qslrdate(self, value):
        if isinstance(value, datetime.datetime):
            self._qslrdate = value
        else:
            self._qslrdate = dateutil.parser.parse(value)

    _qslsdate = Column('qslsdate', DateTime(timezone=False))

    @hybrid_property
    def qslsdate(self):
        return self._qslsdate

    @qslsdate.setter
    def qslsdate(self, value):
        if isinstance(value, datetime.datetime):
            self._qslsdate = value
        else:
            self._qslsdate = dateutil.parser.parse(value)

    qsl_rcvd = Column(Enum(datatypes.RcvdEnum), nullable=False, server_default='N')
    qsl_sent = Column(Enum(datatypes.SendEnum), nullable=False, server_default='N')
    qsl_via = Column(String(length=30), nullable=False, server_default='')

    a_index = Column(Integer)
    k_index = Column(Integer)
    sfi = Column(Integer)
    comment = Column(Text, nullable=False, server_default='')  # notes

    def to_dict(self):
        return dict((col.name, getattr(self, col.name)) for col in class_mapper(self.__class__).mapped_table.c)

    def ext_to_dict(self):
        tmp = self.to_dict()
        if self.band_obj:
            tmp['profile_name'] = self.profile_obj.name
        if self.mode_obj:
            tmp['group_name'] = self.group_obj.name
        if self.band_obj:
            tmp['band_name'] = self.band_obj.name
        if self.mode_obj:
            tmp['mode_name'] = self.mode_obj.name
        if self.band_rx_obj:
            tmp['band_rx_name'] = self.band_rx_obj.name
        if self.mode_rx_obj:
            tmp['mode_rx_name'] = self.mode_rx_obj.name
        if self.dxcc_obj:
            tmp['dxcc_name'] = self.dxcc_obj.name
        return tmp
