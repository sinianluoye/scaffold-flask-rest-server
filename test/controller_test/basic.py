import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, __project_path)

import subprocess
from config import *
from config.controller_test import *
import requests
import json
import time

def create_test_server():
    """create a test server for controller test

    Returns:
        Popen: the process of test server
    """
    cmd = [sys.executable, os.path.join(__project_path, "main.py"), "--env", ENV_CONTROLLER_TEST]
    return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.Popen(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    # time.sleep(5)

def __get_test_server_url(path: str):
    if not path.startswith("/"):
        path = "/" + path
    return f"http://{HOST}:{PORT}{path}"

def post_to_test_server(path, json=None, **kwargs):
    if json == None:
        json = kwargs
    resp = requests.post(__get_test_server_url(path), json=json)
    return resp.json()

def get_from_test_server(path, **kwargs):
    resp = requests.get(__get_test_server_url(path), params=kwargs)
    return resp.json()