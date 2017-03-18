from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
)

from .meta import Base


class Band(Base):
    """ The SQLAlchemy declarative model class for a Band object. """
    __tablename__ = 'band'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20), nullable=False, unique=True)
    lowerfreq = Column(Float, nullable=False)
    upperfreq = Column(Float, nullable=False)
    hide = Column(Boolean(name='ck_band_hide'), nullable=False, server_default='False')
