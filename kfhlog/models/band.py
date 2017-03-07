from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    Boolean,
    Float,
)

from .meta import Base

class Band(Base):
    """ The SQLAlchemy declarative model class for a Band object. """
    __tablename__ = 'band'
    id = Column(Integer, primary_key=True)
    band = Column(CHAR(length=20), nullable=False, unique=True)
    lowerfreq = Column(Float, nullable=False)
    upperfreq = Column(Float, nullable=False)
    hide =  Column(Boolean, nullable=False, default=False)
