from sqlalchemy import (
    Column,
    Text,
)

from .meta import Base


class Setting(Base):
    """ The SQLAlchemy declarative model class for a Setting object. """
    __tablename__ = 'settings'
    key = Column(Text, primary_key=True)
    value = Column(Text, nullable=True)
