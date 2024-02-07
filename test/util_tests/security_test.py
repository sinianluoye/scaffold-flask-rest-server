import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, __project_path)

from utils.security import *

def test_compute_md5_hash():
    assert compute_md5("123456") == "e10adc3949ba59abbe56e057f20f883e"
    assert compute_md5("") == "d41d8cd98f00b204e9800998ecf8427e"
    assert compute_md5(None) == "d41d8cd98f00b204e9800998ecf8427e"