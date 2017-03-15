import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base

class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'user'
    #id = Column(Integer, primary_key=True)
    name = Column(String(length=50), primary_key=True)
    password_hash = Column(String(length=70), nullable=False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False