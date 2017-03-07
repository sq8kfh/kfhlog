from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    Text,
)

from .meta import Base

class Group(Base):
    """ The SQLAlchemy declarative model class for a Group object. """
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR(length=100), nullable=False)
    remarks = Column(Text, default='')
