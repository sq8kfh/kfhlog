from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    Boolean,
)

from .meta import Base

class Mode(Base):
    """ The SQLAlchemy declarative model class for a Mode object. """
    __tablename__ = 'mode'
    id = Column(Integer, primary_key=True)
    mode = Column(CHAR(length=30), nullable=False, unique=True)
    hide =  Column(Boolean, nullable=False, default=False)
