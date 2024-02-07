import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, __project_path)

from config import *

import pytest
import requests
import json
from test.controller_test.basic import *
from controller.user_controller import UserController
from utils.exception import Error

class TestUserController:

    @pytest.fixture(autouse=True, scope='function')
    def warpper(self):
        test_progress = create_test_server()
        yield
        test_progress.kill()
    
    def test_create_user(self):
        resp = post_to_test_server(UserController.get_api_full_path(UserController.API_CREATE), json={
            "username": "admin",
            "password": "1dabac7d5a9f495fa488f76840c4da7b"
        })
        assert resp["code"] == Error.ERROR_USER_NOT_LOGIN.code