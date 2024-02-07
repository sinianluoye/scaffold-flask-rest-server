
import re
from datetime import datetime, timedelta
import string
# ------ basic env config ------ #
RPOJECT_NAME = "show-my-files server"

# env enums
ENV_DEBUG:str = 'debug'
ENV_PROD:str = 'prod'
ENV_CONTROLLER_TEST:str = 'controller_test'
ENV_ALL = frozenset([ENV_DEBUG, ENV_PROD, ENV_CONTROLLER_TEST])
# default server port
DEFAULT_SERVER_PORT = 18750

# environment 
ENV = ENV_DEBUG

# host and port deploy the server
HOST = '127.0.0.1'
PORT = DEFAULT_SERVER_PORT

# whether enable debug mode
DEBUG_MODE = False


# ------ log config ------ #
LOG_ENABLE = True

# log level enums
LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_ALL = frozenset([LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR])

# defaul log level
LOG_LEVEL = LOG_LEVEL_INFO

# log file path
LOG_FILE_PATH = 'logs/'

# log expiration (days)
LOG_EXPIRATION = 7

# ------ Database Config ------ #

DB_TYPE_SQLITE = "sqlite"
DB_TYPE_POSTGRESQL = "postgreSql"

DB_TYPE = DB_TYPE_SQLITE

# for postgre sql
DB_HOST = None
DB_PORT = None
DB_USER = None
DB_PASSWORD = None
DB_DATABASE = None

DB_PATH = "server.db"

def __generate_db_connect_url(db_type:str, db_host:str, db_port:int, db_user:str, db_password:str, db_database:str, db_path:str):
    if db_type == DB_TYPE_SQLITE:
        return f"sqlite:///{db_path}?check_same_thread=False"
    elif db_type == DB_TYPE_POSTGRESQL:
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    else:
        raise Exception(f"Unknown db type: {db_type}")

DB_CONNECT_URL = __generate_db_connect_url(DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PATH)

# Whether echo executed sql to log/console
DB_ENGINE_ECHO = False

# Whether create table if database/tables do not exist
CREATE_DB_IF_NOT_EXISTS = True

# username must be 4-20 characters, only contains a-z, A-Z, 0-9 and _
USERNAME_VALIDATE_PATTERN = re.compile(r'^[a-zA-Z0-9_]{4,20}$')
# 8~32 printable characters
PASSWORD_VALIDATE_PARTERN = re.compile( r'^[\x20-\x7E]{4,32}$')

TOKEN_LENGTH = 32
TOKEN_EXPIRATION_TIME = timedelta(days=1)
TOKEN_NAME = 'user-token'

DEFAULT_ADMIN_USER_NAME = 'admin'
DEFAULT_ADMIN_PASSWORD_LENGTH = 12

PASSWORD_HASH_SALT_LENGTH = 16