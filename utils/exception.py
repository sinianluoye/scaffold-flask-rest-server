


class ErrorMessage:

    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def format(self, **kwargs):
        return f"Error {self.code}: {self.message.format(**kwargs)}"

class PredefinedException(Exception):
    def __init__(self, error: ErrorMessage, **kwargs):
        super().__init__(error.format(**kwargs))
        self.code = error.code

class Error:
    ERROR_SYSTEM_UNKNOWN = ErrorMessage(-1, "Unknown error")
    SUCCESS = ErrorMessage(0, "success")
    ERROR_USER_CREATE_DUP_USERNAME = ErrorMessage(1001, "Username {name} already exists")
    ERROR_USER_INVALID_USERNAME = ErrorMessage(1002, "Invalid username {name}")
    ERROR_USER_EMPTY_PASSWORD = ErrorMessage(1003, "Empty password")
    ERROR_USER_INVALID_TOKEN = ErrorMessage(1004, "Invalid token {token}")
    ERROR_USER_NOT_LOGIN = ErrorMessage(1005, "User not login")
    ERROR_USER_INVALID_USER_ID = ErrorMessage(1006, "Invalid user id {user_id}")
    ERROR_USER_ALREADY_DISABLEED_USER = ErrorMessage(1007, "User {user} already disabled")
    ERROR_USER_LOGIN_ERROR = ErrorMessage(1008, "Login error")
    
    ERROR_SYSTEM_HASHED_PASSWORD_FORMAT_ERROR = ErrorMessage(2001, "Hashed password {password} format error")

