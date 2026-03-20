from base64 import urlsafe_b64encode
from hashlib import sha256

from cryptography.fernet import Fernet

from app.core.config import get_settings


def _fernet() -> Fernet:
    raw_key = get_settings().token_encryption_key.encode("utf-8")
    digest = sha256(raw_key).digest()
    return Fernet(urlsafe_b64encode(digest))


def encrypt_value(value: str) -> str:
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")
