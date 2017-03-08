from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from .meta import Base

class Dxcc(Base):
    """ The SQLAlchemy declarative model class for a DXCC object. """
    __tablename__ = 'dxcc'
    id = Column(Integer, primary_key=True)
    pref = Column(String(length=10), nullable=False)
    name = Column(String(length=100), nullable=False)
    cont = Column(String(length=10), nullable=False)
    utc = Column(String(length=10), nullable=False)
    lat = Column(String(length=10), nullable=False)
    longit = Column(String(length=10), nullable=False)
    itu = Column(String(length=10), nullable=False)
    waz = Column(String(length=10), nullable=False)
    deleted = Column(Boolean, nullable=False)
