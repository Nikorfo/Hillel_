import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 480_000
CHECK_WORD = "vault-ok"


def new_salt() -> bytes:
    return os.urandom(16)


def derive_key(master: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS
    )
    return base64.urlsafe_b64encode(kdf.derive(master.encode()))


def encrypt(key: bytes, text: str) -> bytes:
    return Fernet(key).encrypt(text.encode())


def decrypt(key: bytes, token: bytes) -> str:
    return Fernet(key).decrypt(token).decode()


def make_check(key: bytes) -> bytes:
    return encrypt(key, CHECK_WORD)


def verify_key(key: bytes, check_token: bytes) -> bool:
    try:
        return decrypt(key, check_token) == CHECK_WORD
    except InvalidToken:
        return False
    