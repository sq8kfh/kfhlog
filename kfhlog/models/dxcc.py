from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    Boolean,
)

from .meta import Base

class Dxcc(Base):
    """ The SQLAlchemy declarative model class for a DXCC object. """
    __tablename__ = 'dxcc'
    id = Column(Integer, primary_key=True)
    pref = Column(CHAR(length=10), nullable=False)
    name = Column(CHAR(length=100), nullable=False)
    cont = Column(CHAR(length=10), nullable=False)
    utc = Column(CHAR(length=10), nullable=False)
    lat = Column(CHAR(length=10), nullable=False)
    longit = Column(CHAR(length=10), nullable=False)
    itu = Column(CHAR(length=10), nullable=False)
    waz = Column(CHAR(length=10), nullable=False)
    deleted = Column(Boolean, nullable=False)
