from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base

class Mode(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'mode'
    id = Column(Integer, primary_key=True)
    mode = Column(Text, nullable=False, unique=True)
    rst =  Column(Text, nullable=True)
