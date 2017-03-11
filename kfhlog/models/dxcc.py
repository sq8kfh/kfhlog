import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
)

from .meta import Base


class Continent_enum(enum.Enum):
    NA = 1
    SA = 2
    EU = 3
    AF = 4
    OC = 5
    AS = 6
    AN = 7

class Dxcc(Base):
    """ The SQLAlchemy declarative model class for a DXCC object. """
    __tablename__ = 'dxcc'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    prefix = Column(String(length=20), nullable=False, server_default='')
    deleted = Column(Boolean, nullable=False)
    continent = Column(Enum(Continent_enum))
    #utc = Column(String(length=10), nullable=False)
    #lat = Column(String(length=10), nullable=False)
    #longit = Column(String(length=10), nullable=False)
    ituz = Column(Integer)
    cqz = Column(Integer)
    comment = Column(String(length=100), nullable=False, server_default='')
