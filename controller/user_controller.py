import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, __project_path)


from flask import Blueprint
from service.user_service import UserService
from controller.basic import *



class UserController(BaseController):

    blueprint = Blueprint('user', __name__, url_prefix='/user')

    API_CREATE = "/create"
    @blueprint.post(API_CREATE)
    @api_wrapper(need_login=True)
    def create_user():
        username = request.json.get("username")
        password = request.json.get("password")
        login_user = g.login_user
        UserService.create_user(username, password, login_user=login_user)
    

    API_LOGIN = "/login"
    @blueprint.post(API_LOGIN)
    @api_wrapper(need_login=False)
    def login():
        username = request.json.get("username")
        password = request.json.get("password")
        user_token = UserService.login(username, password)
        return {
            "token": user_token.token,
            "expiration_time": user_token.expire_time.isoformat()
        }