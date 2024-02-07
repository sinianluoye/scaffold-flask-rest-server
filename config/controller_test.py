from .basic import *

ENV = ENV_CONTROLLER_TEST
DB_CONNECT_URL = "sqlite:///:memory:?check_same_thread=False"
LOG_ENABLE = False

HOST = '127.0.0.1'
PORT = DEFAULT_SERVER_PORT + 1