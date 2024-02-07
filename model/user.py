from .basic import *
from sqlalchemy import Column, Integer, String

class User(ModelBase):

    STATUS_ENABLE = 'enanble'
    STATUS_DISABLE = 'disable'

    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column('name', String(50), nullable=False, unique=True)
    status = Column('status', String(32), default=STATUS_ENABLE, nullable=False)
    salt = Column('salt', String(16), default="", nullable=False)
    password = Column('password', String(32), default="", nullable=False, comment="MD5(salt+password).lower()")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, status={self.status})"


class UserToken(ModelBase):
    __tablename__ = 'user_token'

    STATUS_VALID = 'valid'
    STATUS_EXPIRED = 'expired'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column('user_id', Integer, nullable=False)
    token = Column('token', String(32), nullable=False, unique=True)
    expire_time = Column('expire_time', ISODatetime, nullable=False)
    status = Column('status', String(32), default=STATUS_VALID, nullable=False)

    def __repr__(self):
        return f"UserToken(id={self.id}, user_id={self.user_id}, token={self.token}, expire_time={self.expire_time}, status={self.status})"

