from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Enum,
)

from .meta import Base
from .dbtools import datatypes
from .dbtools import formatters


class Profile(Base):
    """ The SQLAlchemy declarative model class for a Profile object. """
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)

    _call = Column('call', String(length=20), nullable=False)

    @hybrid_property
    def call(self):
        return self._call

    @call.setter
    def call(self, value):
        self._call = formatters.call_formatter(value)

    op_name = Column(Text, nullable=False, server_default='')

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

    qth = Column(String(length=60), nullable=False, server_default='')
    rig = Column(String(length=250), nullable=False, server_default='')
    comment = Column(Text, nullable=False, server_default='')
