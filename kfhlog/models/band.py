from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    Float,
)

from .meta import Base

class Band(Base):
    """ The SQLAlchemy declarative model class for a Band object. """
    __tablename__ = 'band'
    id = Column(Integer, primary_key=True)
    band = Column(Text, nullable=False, unique=True)
    lowerfreq = Column(Float, nullable=False)
    upperfreq = Column(Float, nullable=False)
    hide =  Column(Boolean, nullable=False)
