import hashlib
import string
import random
from config import PASSWORD_HASH_SALT_LENGTH
def compute_md5(s: str):
    if s is None:
        s = ""
    md5_hash = hashlib.md5()
    md5_hash.update(s.encode('utf-8'))
    return md5_hash.hexdigest().lower()

def generate_random_password(length: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_token(length: int):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_salt(length: int=PASSWORD_HASH_SALT_LENGTH):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hash_password(password:str, salt:str):
    return compute_md5(salt + password)