from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
)

from .meta import Base
from .dbtools import datatypes


class Dxcc(Base):
    """ The SQLAlchemy declarative model class for a DXCC object. """
    __tablename__ = 'dxcc'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    prefix = Column(String(length=20), nullable=False, server_default='')
    deleted = Column(Boolean(name='ck_dxcc_deleted'), nullable=False)
    continent = Column(Enum(datatypes.ContinentEnum))
    # utc = Column(String(length=10), nullable=False)
    # lat = Column(String(length=10), nullable=False)
    # longit = Column(String(length=10), nullable=False)
    ituz = Column(Integer)
    cqz = Column(Integer)
    comment = Column(String(length=100), nullable=False, server_default='')
