from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
)

from .meta import Base
from .dbtools import datatypes


class Mode(Base):
    """ The SQLAlchemy declarative model class for a Mode object. """
    __tablename__ = 'mode'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=30), nullable=False, unique=True)
    hide = Column(Boolean(name='ck_mode_hide'), nullable=False, server_default='False')
    mode_cat = Column(Enum(datatypes.ModeEnum), nullable=False, server_default='DIGITAL')
    def_rst = Column(String(length=10), nullable=False, server_default='')
