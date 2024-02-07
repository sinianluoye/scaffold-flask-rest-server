import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, __project_path)

import functools
from flask import jsonify, request, g
from utils.logger import logger
from service.user_service import UserService
from utils.exception import PredefinedException, Error
from config import TOKEN_NAME
import uuid

def __valide_login():
    token = request.cookies.get(TOKEN_NAME)
    if token == None:
        token = request.headers.get(TOKEN_NAME)
    if token == None:
        raise PredefinedException(Error.ERROR_USER_NOT_LOGIN)
    user = UserService.get_user_by_token(token)
    if user == None:
        raise PredefinedException(Error.ERROR_USER_NOT_LOGIN)
    return user

def __get_request_source_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ret = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ret = request.remote_addr
    return ret

def api_wrapper(need_login=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                g.login_user = None
                g.api_guid = uuid.uuid4()
                g.source_ip = __get_request_source_ip()
                if need_login:
                    g.login_user = __valide_login()

                logger.debug(api_guid=g.api_guid, method=request.method, url=request.url, login_user=g.login_user, status="ready", source_ip=g.source_ip)
                data = func(*args, **kwargs)
                logger.info(api_guid=g.api_guid, method=request.method, url=request.url, login_user=g.login_user, status="success", source_ip=g.source_ip)
                return jsonify(code=Error.SUCCESS.code, data=data, message=Error.SUCCESS.message)
            
            except (PredefinedException, Exception) as e:
                if isinstance(e, PredefinedException):
                    error_code = e.code
                    error_message = str(e)
                else:
                    error_code = Error.ERROR_SYSTEM_UNKNOWN.code
                    error_message = Error.ERROR_SYSTEM_UNKNOWN.message
                logger.error(api_guid=g.api_guid, 
                             method=request.method, 
                             url=request.url, 
                             login_user=g.login_user, 
                             status="error",
                             request_header=request.headers,
                             request_data=request.get_data(),
                             error_code=error_code,
                             error_message=error_message,
                             source_ip=__get_request_source_ip())
                logger.exception(e)
                return jsonify(code=error_code, message=error_message)
               
        return wrapper
    return decorator

class BaseController:

    @classmethod
    def get_api_full_path(cls, subpath: str):
        """get full path of api

        Args:
            subpath (str): the subpath of api in blueprint
        """
        if not subpath.startswith("/"):
            subpath = '/' + subpath
        return cls.blueprint.url_prefix + subpath