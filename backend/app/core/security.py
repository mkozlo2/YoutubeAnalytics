from base64 import urlsafe_b64encode
from datetime import datetime, timedelta, timezone
from hashlib import sha256

from cryptography.fernet import Fernet
from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.config import get_settings


def _fernet() -> Fernet:
    raw_key = get_settings().token_encryption_key.encode("utf-8")
    digest = sha256(raw_key).digest()
    return Fernet(urlsafe_b64encode(digest))


def encrypt_value(value: str) -> str:
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")


def create_session_token(user_id: int) -> str:
    settings = get_settings()
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, settings.app_secret_key, algorithm="HS256")


def decode_session_token(token: str) -> int:
    try:
        payload = jwt.decode(token, get_settings().app_secret_key, algorithms=["HS256"])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid session.") from exc
