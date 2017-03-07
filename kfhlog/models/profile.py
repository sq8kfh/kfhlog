from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    Text,
)

from .meta import Base

class Profile(Base):
    """ The SQLAlchemy declarative model class for a Profile object. """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR(length=100), nullable=False)
    callsign = Column(CHAR(length=20), nullable=False)
    locator = Column(CHAR(length=8), nullable=True)
    qth = Column(CHAR(length=60), nullable=True)
    rig = Column(CHAR(length=250), nullable=True)
    remarks = Column(Text, nullable=True, default='')
