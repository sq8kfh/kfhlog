from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from .meta import Base

class Profile(Base):
    """ The SQLAlchemy declarative model class for a Profile object. """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    callsign = Column(String(length=20), nullable=False)
    locator = Column(String(length=8), nullable=False, server_default='')
    qth = Column(String(length=60), nullable=False, server_default='')
    rig = Column(String(length=250), nullable=False, server_default='')
    comment = Column(Text, nullable=False, server_default='')
