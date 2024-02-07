import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, __project_path)

import contextlib
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, DateTime, func as sql_func
import config
from datetime import datetime
from utils.time import datetime_utcnow, ISODatetime

_global_engine = create_engine(config.DB_CONNECT_URL, echo=config.DB_ENGINE_ECHO)

def is_db_exist():
    """check if database exist

    Returns:
        bool: True if exist, False if not exist
    """
    return inspect(_global_engine).has_table(_global_engine, 'user')


ModelBase = declarative_base()
ModelBase.update_time = Column('create_time', ISODatetime, default=datetime_utcnow, onupdate=datetime_utcnow)
ModelBase.create_time = Column('update_time', ISODatetime, default=datetime_utcnow)
ModelBase.__repr__ = lambda self: f"{self.__class__.__name__}({', '.join([f'{c.name}={getattr(self, c.name)}' for c in self.__table__.columns])})"

def to_dict(model):
    if hasattr(model, "to_dict"):
        return model.to_dict()
    else:
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}

def init_databse():
    ModelBase.metadata.create_all(_global_engine)

@contextlib.contextmanager
def db_session(rollback_on_error=True, expunge_all=False, covered_session=None):
    """contextmanager for session of database

    Args:
        rollback_on_error (bool, optional): whether rollback when error. Defaults to True.
        expunge_all (bool, optional): whether expunge all items from session, 
            notice: it should be True when item in the session want to be used out of session. Defaults to False.
        covered_session (Session, optional): if already have a session, use it. Defaults to None.
    """
    if covered_session:
        yield covered_session
    else:
        session = sessionmaker(bind=_global_engine)()
        try:
            yield session
            
            if expunge_all:
                session.flush()
                session.expunge_all()
            session.commit()
        except:
            if rollback_on_error:
                session.rollback()
            raise
        finally:
            session.close()
