import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, __project_path)

from service.user_service import UserService
from utils.exception import Error, PredefinedException
from utils.security import compute_md5
from sqlalchemy import create_engine
import pytest
from model.user import User, UserToken
from model import basic as model_basic
from datetime import datetime
from utils.time import datetime_utcnow

class TestUserService:

    TEST_DB_URL = "sqlite:///:memory:?check_same_thread=False" 

    @pytest.fixture(autouse=True, scope='class')
    def class_warpper(self):
        _test_db_engine = create_engine(self.TEST_DB_URL, echo=False)
        from model import basic as model_basic
        model_basic._global_engine = _test_db_engine
        model_basic.ModelBase.metadata.create_all(_test_db_engine)
        yield

    @pytest.fixture(autouse=True, scope='function')
    def function_warpper(self):
        with model_basic.db_session() as session:
            session.query(User).delete()
            session.query(UserToken).delete()

    def test_create_user(self):
        
        admin_user = UserService.create_user("admin", "12345678")
        
        UserService.create_user("user1", "12345678")

        try:
            UserService.create_user("user1", "12345678")
            assert False, "should not create user with same username"
        except PredefinedException as e:
            assert e.code == 1001
        
        try:
            UserService.create_user("u", "12345678", login_user=admin_user)
            assert False, "username is too short"
        except PredefinedException as e:
            assert e.code == 1002

        try:
            UserService.create_user("user3", "", login_user=admin_user)
            assert False, "password can not be empty"
        except PredefinedException as e:
            assert e.code == 1003

    def test_get_user_count(self):
        assert UserService.get_user_count() == 0
        assert UserService.get_user_count(include_disable=True) == 0
        admin_user = UserService.create_user("admin", "12345678")
        assert UserService.get_user_count() == 1
        user1 = UserService.create_user("user1", "12345678")
        assert UserService.get_user_count() == 2
        UserService.disable_user(user1.id)
        assert UserService.get_user_count() == 1
        assert UserService.get_user_count(include_disable=True) == 2
    
    def test_disable_user(self):
        admin_user = UserService.create_user("admin", "12345678")
        user1 = UserService.create_user("user1", "12345678")
        UserService.disable_user(user1.id)
        assert UserService.get_user_count() == 1
    
    def test_create_token(self):
        admin_user = UserService.create_user("admin", "12345678")
        admin_user_token = UserService.create_user_token(admin_user.id)
        assert admin_user_token.status == UserToken.STATUS_VALID
        assert admin_user_token.expire_time > datetime_utcnow()
        admin_user_token_2 = UserService.create_user_token(admin_user.id)
        with model_basic.db_session(expunge_all=True) as session:
            admin_user_token = session.query(UserToken).filter(UserToken.id == admin_user_token.id).first()
        assert admin_user_token.status == UserToken.STATUS_EXPIRED
        assert admin_user_token_2.status == UserToken.STATUS_VALID
        assert admin_user_token_2.expire_time > datetime_utcnow()
    
    def test_login(self):
        admin_user = UserService.create_user("admin", "12345678")
        token = UserService.login("admin", "12345678")
        assert token.expire_time > datetime_utcnow()
        assert token.status == UserToken.STATUS_VALID
        token2 = UserService.login("admin", "12345678")
        with model_basic.db_session(expunge_all=True) as session:
            token = session.query(UserToken).filter(UserToken.id == token.id).first()
        assert token.status == UserToken.STATUS_EXPIRED

        try:
            UserService.login("admin", "12345678")
        except PredefinedException as e:
            assert e.code == Error.ERROR_USER_LOGIN_ERROR.code
        
        try:
            UserService.login("user1", "12345678")
        except PredefinedException as e:
            assert e.code == Error.ERROR_USER_LOGIN_ERROR.code