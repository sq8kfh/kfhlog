from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from .meta import Base
from .dbtools import formatters

class Profile(Base):
    """ The SQLAlchemy declarative model class for a Profile object. """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)

    _call = Column('call', String(length=20), nullable=False)

    @hybrid_property
    def call(self):
        return self._call

    @call.setter
    def call(self, value):
        self._call = formatters.call_formatter(value)

    _gridsquare = Column('gridsquare', String(length=8), nullable=False, server_default='')

    @hybrid_property
    def gridsquare(self):
        return self._gridsquare

    @gridsquare.setter
    def gridsquare(self, value):
        self._gridsquare = formatters.gridsquare_formatter(value)

    qth = Column(String(length=60), nullable=False, server_default='')
    rig = Column(String(length=250), nullable=False, server_default='')
    comment = Column(Text, nullable=False, server_default='')
