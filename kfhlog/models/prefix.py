from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
)

from .meta import Base
from .dbtools import datatypes


class Prefix(Base):
    """ The SQLAlchemy declarative model class for a DXCC object. """
    __tablename__ = 'prefix'
    prefix = Column(String(length=20), primary_key=True)
    dxcc = Column(ForeignKey('dxcc.id'), nullable=True)
    # dxcc_obj = relationship("Dxcc", foreign_keys=dxcc)
    ituz = Column(Integer, nullable=False)
    cqz = Column(Integer, nullable=False)
    cont = Column(Enum(datatypes.ContinentEnum))
    comment = Column(String(length=100), nullable=False, server_default='')
