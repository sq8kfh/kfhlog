from sqlalchemy.orm import class_mapper
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)

from .meta import Base


class State(Base):
    """ The SQLAlchemy declarative model class for a State object. """
    __tablename__ = 'states'
    dxcc = Column(ForeignKey('dxcc.id'), primary_key=True)
    code = Column(String(length=10), primary_key=True)
    name = Column(String, nullable=False)

    def to_dict(self):
        return dict((col.name, getattr(self, col.name)) for col in class_mapper(self.__class__).mapped_table.c)
