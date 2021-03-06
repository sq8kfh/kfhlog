from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from .meta import Base


class Group(Base):
    """ The SQLAlchemy declarative model class for a Group object. """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    comment = Column(Text, nullable=False, server_default='')
