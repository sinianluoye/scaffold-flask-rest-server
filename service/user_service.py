import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, __project_path)

from config import USERNAME_VALIDATE_PATTERN, PASSWORD_HASH_SALT_LENGTH, TOKEN_LENGTH, TOKEN_EXPIRATION_TIME, PASSWORD_VALIDATE_PARTERN
from model import User, UserToken, db_session
from utils.exception import PredefinedException, Error
from utils.security import compute_md5, generate_token, hash_password, generate_salt
from utils.time import datetime_utcnow
from typing import Union
from sqlalchemy import and_
import re
from datetime import datetime, timedelta

class UserService:
    
    @staticmethod
    def __valide_username_and_password(name: str, password: str) -> None:
        """validate user name and password

        Args:
            name (str): user name
            password (str): unhashed password

        Raises:
            ShowMyFileException: invalid user name or password
        """
        # valide username, parttern can be update at config file
        if not USERNAME_VALIDATE_PATTERN.match(name):
            raise PredefinedException(Error.ERROR_USER_INVALID_USERNAME, name=name)
        
        # check whether not hashed password is null
        if not PASSWORD_VALIDATE_PARTERN.match(password):
            raise PredefinedException(Error.ERROR_USER_EMPTY_PASSWORD)

    @classmethod
    def create_user(cls, name: str, password: str, login_user:Union[User,None]=None) -> User:
        """ create user by user name and hashed password

        Args:
            login_user (User): current login user, None means systeam created
            name (str): user name
            password (str): unhashed password

        Raises:
            ShowMyFileException: 
                1. if user name already exists
                2. invalid user name or password
        Returns:
            User: created user
        """
        cls.__valide_username_and_password(name, password)
        with db_session(expunge_all=True) as session:
            if session.query(User).filter(User.name == name).first() != None:
                raise PredefinedException(Error.ERROR_USER_CREATE_DUP_USERNAME, name=name)
            salt = generate_salt()
            user = User(name=name, password=hash_password(password, salt), salt=salt)
            session.add(user)
            return user
    
    @classmethod
    def get_user_by_token(cls, token) -> User:
        """get user by token

        Args:
            token (str): token

        Raises:
            ShowMyFileException: invalid token

        Returns:
            User: user
        """
        with db_session(rollback_on_error=False, expunge_all=True) as session:
            user_token = session.query(UserToken).filter(UserToken.token == token).first()

            if user_token == None or user_token.status == UserToken.STATUS_EXPIRED:
                raise PredefinedException(Error.ERROR_USER_INVALID_TOKEN, token=token)
            
            if datetime_utcnow() > user_token.expire_time:
                user_token.status = UserToken.STATUS_EXPIRED
                session.commit()
                raise PredefinedException(Error.ERROR_USER_INVALID_TOKEN, token=token)
            
            user = session.query(User).filter(User.id == user_token.user_id).first()

            if user == None or user.status == User.STATUS_DISABLE:
                raise PredefinedException(Error.ERROR_USER_INVALID_TOKEN, token=token)
            
            return user
    
    @classmethod
    def get_user_by_id(cls, user_id, session=None):
        with db_session(expunge_all=True, covered_session=session) as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                raise PredefinedException(Error.ERROR_USER_INVALID_USER_ID, user_id=user_id)
            return user

    @classmethod
    def create_user_token(cls, user_id: int) -> UserToken:
        """create user token

        Args:
            user_id (int): user id

        Returns:
            UserToken: user token (notice: the response is a UserToken instead of str)
        """
        with db_session(expunge_all=True) as session:
            user = cls.get_user_by_id(user_id, session=session)
            if user.status == User.STATUS_DISABLE:
                raise PredefinedException(Error.ERROR_USER_ALREADY_DISABLEED_USER, user=user)
            cls.disable_user_token(user_id=user.id)
            user_token = UserToken(
                user_id=user.id, 
                token=generate_token(TOKEN_LENGTH), 
                expire_time=datetime_utcnow() + TOKEN_EXPIRATION_TIME)
            session.add(user_token)
            return user_token

    @classmethod
    def disable_user_token(cls, user_id: int, session=None):
        """disable user token

        Args:
            user_id (int): user id
        """
        with db_session(covered_session=session) as session:
            user = cls.get_user_by_id(user_id, session=session)
            if user.status == User.STATUS_DISABLE:
                raise PredefinedException(Error.ERROR_USER_ALREADY_DISABLEED_USER, user=user)
            user_token = session.query(UserToken).filter(UserToken.user_id == user.id).first()
            if user_token:
                user_token.status = UserToken.STATUS_EXPIRED

    @classmethod
    def get_user_count(cls, include_disable=False) -> int:
        """return the count of users in the system

        Args:
            include_disable (bool, optional): does result include disabled user. Defaults to False.

        Returns:
            int: the numbers of users
        """
        with db_session() as session:
            ret = session.query(User)
            if not include_disable:
                ret = ret.filter(User.status == User.STATUS_ENABLE)
            return ret.count()

    @classmethod
    def disable_user(cls, user_id=None):
        """disable user

        Args:
            user_id (int, optional): user id. Defaults to None.
        """
        with db_session() as session:
            user = cls.get_user_by_id(user_id, session=session)
            if user.status == User.STATUS_DISABLE:
                raise PredefinedException(Error.ERROR_USER_ALREADY_DISABLEED_USER, user=user)
            user.status = User.STATUS_DISABLE
    
    @classmethod
    def login(cls, name: str, password: str) -> UserToken:
        """login

        Args:
            name (str): user name
            password (str): not hashed password

        Raises:
            ShowMyFileException: invalid user name or password

        Returns:
            UserToken: user token
        """
        cls.__valide_username_and_password(name, password)
        with db_session(expunge_all=True) as session:
            user = session.query(User).filter(and_(User.name == name)).first()
            if user == None or hash_password(password, user.salt) != user.password:
                raise PredefinedException(Error.ERROR_USER_LOGIN_ERROR)
            if user.status == User.STATUS_DISABLE:
                raise PredefinedException(Error.ERROR_USER_ALREADY_DISABLEED_USER, user=user)
            return cls.create_user_token(user.id)
